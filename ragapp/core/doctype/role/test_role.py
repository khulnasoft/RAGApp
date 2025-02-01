# Copyright (c) 2025, KhulnaSoft, Ltd and Contributors
# License: MIT. See LICENSE

import ragapp
from ragapp.core.doctype.role.role import get_info_based_on_role
from ragapp.tests import IntegrationTestCase, UnitTestCase


class UnitTestRole(UnitTestCase):
	"""
	Unit tests for Role.
	Use this class for testing individual functions and methods.
	"""

	pass


class TestUser(IntegrationTestCase):
	def test_disable_role(self):
		ragapp.get_doc("User", "test@example.com").add_roles("_Test Role 3")

		role = ragapp.get_doc("Role", "_Test Role 3")
		role.disabled = 1
		role.save()

		self.assertTrue("_Test Role 3" not in ragapp.get_roles("test@example.com"))

		role = ragapp.get_doc("Role", "_Test Role 3")
		role.disabled = 0
		role.save()

		ragapp.get_doc("User", "test@example.com").add_roles("_Test Role 3")
		self.assertTrue("_Test Role 3" in ragapp.get_roles("test@example.com"))

	def test_change_desk_access(self):
		"""if we change desk acecss from role, remove from user"""
		ragapp.delete_doc_if_exists("User", "test-user-for-desk-access@example.com")
		ragapp.delete_doc_if_exists("Role", "desk-access-test")
		user = ragapp.get_doc(
			doctype="User", email="test-user-for-desk-access@example.com", first_name="test"
		).insert()
		role = ragapp.get_doc(doctype="Role", role_name="desk-access-test", desk_access=0).insert()
		user.add_roles(role.name)
		user.save()
		self.assertTrue(user.user_type == "Website User")
		role.desk_access = 1
		role.save()
		user.reload()
		self.assertTrue(user.user_type == "System User")
		role.desk_access = 0
		role.save()
		user.reload()
		self.assertTrue(user.user_type == "Website User")

	def test_get_users_by_role(self):
		role = "System Manager"
		sys_managers = get_info_based_on_role(role, field="name")

		for user in sys_managers:
			self.assertIn(role, ragapp.get_roles(user))
