# -*- coding: utf-8 -*-

from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import TEST_USER_ID
from plone.app.testing import applyProfile
from plone.app.testing import setRoles

import imio.zamqp.core
from Products.CMFPlone.utils import base_hasattr
from zope.globalrequest import setLocal


class ImioZamqpCoreLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        import plone.app.dexterity
        self.loadZCML(package=plone.app.dexterity)
        self.loadZCML(package=imio.zamqp.core, name="testing.zcml")
        from App.config import _config
        if not base_hasattr(_config, 'product_config'):
            _config.product_config = {'imio.zamqp.core': {'ws_url': 'http://localhost:6543', 'ws_password': 'test',
                                                          'ws_login': 'testuser', 'routing_key': '019999',
                                                          'client_id': '019999'}}

    def setUpPloneSite(self, portal):
        setLocal('request', portal.REQUEST)  # set request for fingerpointing
        applyProfile(portal, "imio.zamqp.core:testing")
        setRoles(portal, TEST_USER_ID, ["Manager"])


IMIO_ZAMQP_CORE_FIXTURE = ImioZamqpCoreLayer()


IMIO_ZAMQP_CORE_INTEGRATION_TESTING = IntegrationTesting(
    bases=(IMIO_ZAMQP_CORE_FIXTURE,),
    name="ImioZamqpCoreLayer:IntegrationTesting",
)


IMIO_ZAMQP_CORE_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(IMIO_ZAMQP_CORE_FIXTURE,),
    name="ImioZamqpCoreLayer:FunctionalTesting",
)
