# encoding: utf-8

from requests.auth import HTTPBasicAuth
import cPickle
import hashlib
import requests
import transaction

from zope.component.hooks import getSite
from zope.globalrequest import getRequest

from plone import api
from plone.dexterity.utils import createContentInContainer
from plone.namedfile.file import NamedBlobFile
from imio.zamqp.core import base

import logging
log = logging.getLogger('imio.zamqp.core')


def consume(consumer_class, folder, document_type, message):
    """ """
    doc = consumer_class(folder, document_type, message)
    doc.create_or_update()
    transaction.commit()
    message.ack()


class Dummy(object):

    def __init__(self, context, request):
        self.context = context
        self.request = request


class DMSMainFile(object):

    def __init__(self, folder, document_type, message):
        self.folder = self.site.unrestrictedTraverse(folder)
        self.document_type = document_type
        self.obj = base.MessageAdapter(cPickle.loads(message.body))
        self.metadata = self.obj.metadata.copy()
        self.context = Dummy(self.folder, getRequest())
        self.scan_fields = {'scan_id': '',
                            'pages_number': '',
                            'scan_date': '',
                            'scan_user': '',
                            'scanner': ''}
        self.scan_fields['version'] = self.obj.version
        keys = self.metadata.keys()
        for key in keys:
            if key in self.scan_fields:
                self.scan_fields[key] = self.metadata.pop(key)

    @property
    def site(self):
        return getSite()

    @property
    def file_portal_types(self):
        return ['dmsmainfile']

    @property
    def creation_file_portal_type(self):
        return self.file_portal_types[0]

    @property
    def existing_file(self):
        result = self.site.portal_catalog(
            portal_type=self.file_portal_types,
            scan_id=self.scan_fields.get('scan_id'),
        )
        if result:
            return result[0].getObject()

    @property
    def file_content(self):
        url = '%s/file/%s/%s/%s' % (base.get_config('ws_url'),
                                    self.obj.client_id,
                                    self.obj.external_id,
                                    self.obj.version)
        r = requests.get(url, auth=self.http_auth)
        if r.status_code != 200:
            raise ValueError("HTTP error : %s on '%s'" % (r.status_code, url))
        if hashlib.md5(r.content).hexdigest() != self.obj.file_md5:
            raise ValueError("MD5 doesn't match")
        return r.content

    @property
    def http_auth(self):
        return HTTPBasicAuth(base.get_config('ws_login'),
                             base.get_config('ws_password'))

    @property
    def obj_file(self):
        return NamedBlobFile(self.file_content, filename=self.obj.filename)

    def create_or_update(self):
        obj_file = self.obj_file
        the_file = self.existing_file
        if the_file:
            self.update(the_file, obj_file)
        else:
            self.create(obj_file)

    def set_scan_attr(self, main_file):
        for key, value in self.scan_fields.items():
            if value:
                setattr(main_file, key, value)
        main_file.reindexObject(idxs=('scan_id', 'signed'))

    def update(self, the_file, obj_file):
        if self.obj.version < getattr(the_file, 'version', 1):
            log.info("file not updated due to an oldest version (scan_id: {0})".format(the_file.scan_id))
            return
        container = the_file.aq_parent
        api.content.delete(obj=the_file)
        self._updateContainer(container)
        new_file = self._upload_file(container, obj_file)
        self.set_scan_attr(new_file)
        container.reindexObject()
        log.info("file has been updated (scan_id: {0})".format(new_file.scan_id))

    def _updateContainer(self, container):
        """Update container if necessary."""
        return

    def _upload_file(self, document, obj_file):
        extra_data = self._upload_file_extra_data()
        new_file = createContentInContainer(
            document,
            self.creation_file_portal_type,
            title=self.metadata.get('file_title'),
            file=obj_file,
            **extra_data
        )
        return new_file

    def _upload_file_extra_data(self):
        """ """
        return {}

    def create(self, obj_file):
        raise NotImplementedError
