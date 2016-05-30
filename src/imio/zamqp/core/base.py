# encoding: utf-8

from App.config import getConfiguration


def get_config(key):
    config = getattr(getConfiguration(), 'product_config', {})
    package_config = config.get('imio.zamqp.core')
    if package_config is None:
        raise ValueError('The config for the package is missing')
    return package_config.get(key, '')


class MessageAdapter(object):

    def __init__(self, context):
        self.context = context

    def __getattr__(self, key):
        try:
            return self.__getattribute__(key)
        except AttributeError:
            return getattr(self.context, key)

    @property
    def metadata(self):
        return {
            'id': self.context.external_id,
            'file_title': self.context.file_metadata.get('filename'),
            'mail_type': self.context.mail_type,
            'scan_id': self.context.external_id,
            'pages_number': self.context.file_metadata.get('pages_number'),
            'scan_date': self.context.scan_date,
            'scan_user': self.context.file_metadata.get('user'),
            'scanner': self.context.file_metadata.get('pc'),
        }


class DMSConsumer(object):

    @property
    def queue(self):
        client_id = get_config('client_id')
        return self.queuename.format(client_id)

    @property
    def routing_key(self):
        return get_config('routing_key')


class DMSProducer(object):

    @property
    def queue(self):
        client_id = get_config('client_id')
        return self.queuename.format(client_id)

    @property
    def routing_key(self):
        return get_config('routing_key')
