# Copyright (c) 2025, KhulnaSoft, Ltd and Contributors
# License: MIT. See LICENSE

import ragapp
from ragapp.desk.form.linked_with import get_linked_docs, get_linked_doctypes
from ragapp.tests import IntegrationTestCase


class TestForm(IntegrationTestCase):
	def test_linked_with(self):
		results = get_linked_docs("Role", "System Manager", linkinfo=get_linked_doctypes("Role"))
		self.assertTrue("User" in results)
		self.assertTrue("DocType" in results)
