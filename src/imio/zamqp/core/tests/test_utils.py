# -*- coding: utf-8 -*-
from imio.zamqp.core.testing import IMIO_ZAMQP_CORE_INTEGRATION_TESTING
from imio.zamqp.core.utils import next_scan_id
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID

import unittest


class TestUtils(unittest.TestCase):

    layer = IMIO_ZAMQP_CORE_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.tt1 = api.content.create(container=self.portal, type='testingtype', id='tt1', title='tt1')
        self.pc = self.portal.portal_catalog

    def test_next_scan_id(self):
        # no scan_id found
        self.assertEqual(next_scan_id(file_portal_types=['testingtype']), '013999900000001')
        # scan_id found
        self.tt1.scan_id = '013999900000008'
        self.tt1.reindexObject()
        self.assertEqual(next_scan_id(file_portal_types=['testingtype']), '013999900000009')
        # scan_id found with another type
        self.assertRaises(ValueError, next_scan_id, file_portal_types=['testingtype'], scan_type=2)
