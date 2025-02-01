# Copyright (c) 2025, KhulnaSoft, Ltd and Contributors
# License: MIT. See LICENSE
import os
import unittest
from unittest.mock import patch

import ragapp
from ragapp.tests import IntegrationTestCase, UnitTestCase


class UnitTestPage(UnitTestCase):
	"""
	Unit tests for Page.
	Use this class for testing individual functions and methods.
	"""

	pass


class TestPage(IntegrationTestCase):
	def test_naming(self):
		self.assertRaises(
			ragapp.NameError,
			ragapp.get_doc(doctype="Page", page_name="DocType", module="Core").insert,
		)

	@unittest.skipUnless(
		os.access(ragapp.get_app_path("ragapp"), os.W_OK), "Only run if ragapp app paths is writable"
	)
	@patch.dict(ragapp.conf, {"developer_mode": 1})
	def test_trashing(self):
		page = ragapp.new_doc("Page", page_name=ragapp.generate_hash(), module="Core").insert()

		page.delete()
		ragapp.db.commit()

		module_path = ragapp.get_module_path(page.module)
		dir_path = os.path.join(module_path, "page", ragapp.scrub(page.name))

		self.assertFalse(os.path.exists(dir_path))
