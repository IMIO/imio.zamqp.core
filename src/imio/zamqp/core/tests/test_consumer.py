# -*- coding: utf-8 -*-
from imio.esign.utils import get_session_annotation
from imio.zamqp.core.consumer import DMSMainFile
from imio.zamqp.core.testing import IMIO_ZAMQP_CORE_INTEGRATION_TESTING
from persistent.list import PersistentList
from persistent.mapping import PersistentMapping
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID

import unittest


class TestUpdateEsignSession(unittest.TestCase):

    layer = IMIO_ZAMQP_CORE_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.consumer = DMSMainFile.__new__(DMSMainFile)

    @staticmethod
    def _make_session(sessions, num_files):
        """Set up sessions annotation with a new session containing num_files files.

        :param sessions: the annotation dict returned by get_session_annotation()
        :param num_files: number of files to create in the session
        :return: (session_id, [uid1, uid2, ...])
        """
        session_id = u"session-{}".format(len(sessions["sessions"]) + 1)
        uids = [u"uid-{}-{}".format(session_id, i) for i in range(num_files)]
        files = PersistentList([PersistentMapping({"uid": uid, "status": ""}) for uid in uids])
        sessions["sessions"][session_id] = PersistentMapping({"state": "draft", "files": files})
        for uid in uids:
            sessions["uids"][uid] = session_id
        return session_id, uids

    def test_update_esign_session(self):
        sessions = get_session_annotation()

        # 1. Unknown uid — not in sessions["uids"] → returns False
        self.assertFalse(self.consumer._update_esign_session(u"unknown-uid"))

        # 2. uid in uids but session_id missing from sessions → returns False
        sessions["uids"][u"missing-session-uid"] = u"session-missing"
        self.assertFalse(self.consumer._update_esign_session(u"missing-session-uid"))

        # 3. uid in uids but absent from session files → returns False
        session_id = u"session-broken"
        sessions["sessions"][session_id] = PersistentMapping(
            {"state": "draft", "files": PersistentList()}
        )
        sessions["uids"][u"orphan-uid"] = session_id
        self.assertFalse(self.consumer._update_esign_session(u"orphan-uid"))

        # 4. Single-file session → file status "received", state "finalized", returns True
        sid1, uids1 = self._make_session(sessions, 1)
        self.assertTrue(self.consumer._update_esign_session(uids1[0]))
        self.assertEqual(sessions["sessions"][sid1]["files"][0]["status"], "received")
        self.assertEqual(sessions["sessions"][sid1]["state"], "finalized")

        # 5. Multi-file session, partial — call with first uid → first file "received",
        #    second still "", state stays "draft", returns True
        sid2, uids2 = self._make_session(sessions, 2)
        self.assertTrue(self.consumer._update_esign_session(uids2[0]))
        self.assertEqual(sessions["sessions"][sid2]["files"][0]["status"], "received")
        self.assertEqual(sessions["sessions"][sid2]["files"][1]["status"], "")
        self.assertEqual(sessions["sessions"][sid2]["state"], "draft")

        # 6. Multi-file session, all received — call with second uid → both "received",
        #    state becomes "finalized", returns True
        self.assertTrue(self.consumer._update_esign_session(uids2[1]))
        self.assertEqual(sessions["sessions"][sid2]["files"][0]["status"], "received")
        self.assertEqual(sessions["sessions"][sid2]["files"][1]["status"], "received")
        self.assertEqual(sessions["sessions"][sid2]["state"], "finalized")
