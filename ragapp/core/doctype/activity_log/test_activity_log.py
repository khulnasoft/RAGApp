# Copyright (c) 2015, Ragapp Technologies and Contributors
# License: MIT. See LICENSE
import time

import ragapp
from ragapp.auth import CookieManager, LoginManager
from ragapp.tests import IntegrationTestCase, UnitTestCase


class UnitTestActivityLog(UnitTestCase):
	"""
	Unit tests for ActivityLog.
	Use this class for testing individual functions and methods.
	"""

	pass


class TestActivityLog(IntegrationTestCase):
	def setUp(self) -> None:
		ragapp.set_user("Administrator")

	def test_activity_log(self):
		# test user login log
		ragapp.local.form_dict = ragapp._dict(
			{
				"cmd": "login",
				"sid": "Guest",
				"pwd": self.ADMIN_PASSWORD or "admin",
				"usr": "Administrator",
			}
		)

		ragapp.local.request_ip = "127.0.0.1"
		ragapp.local.cookie_manager = CookieManager()
		ragapp.local.login_manager = LoginManager()

		auth_log = self.get_auth_log()
		self.assertFalse(ragapp.form_dict.pwd)
		self.assertEqual(auth_log.status, "Success")

		# test user logout log
		ragapp.local.login_manager.logout()
		auth_log = self.get_auth_log(operation="Logout")
		self.assertEqual(auth_log.status, "Success")

		# test invalid login
		ragapp.form_dict.update({"pwd": "password"})
		self.assertRaises(ragapp.AuthenticationError, LoginManager)
		auth_log = self.get_auth_log()
		self.assertEqual(auth_log.status, "Failed")

		ragapp.local.form_dict = ragapp._dict()

	def get_auth_log(self, operation="Login"):
		names = ragapp.get_all(
			"Activity Log",
			filters={
				"user": "Administrator",
				"operation": operation,
			},
			order_by="`creation` DESC",
		)

		name = names[0]
		return ragapp.get_doc("Activity Log", name)

	def test_brute_security(self):
		update_system_settings({"allow_consecutive_login_attempts": 3, "allow_login_after_fail": 5})

		ragapp.local.form_dict = ragapp._dict(
			{"cmd": "login", "sid": "Guest", "pwd": self.ADMIN_PASSWORD, "usr": "Administrator"}
		)

		ragapp.local.request_ip = "127.0.0.1"
		ragapp.local.cookie_manager = CookieManager()
		ragapp.local.login_manager = LoginManager()

		auth_log = self.get_auth_log()
		self.assertEqual(auth_log.status, "Success")

		# test user logout log
		ragapp.local.login_manager.logout()
		auth_log = self.get_auth_log(operation="Logout")
		self.assertEqual(auth_log.status, "Success")

		# test invalid login
		ragapp.form_dict.update({"pwd": "password"})
		self.assertRaises(ragapp.AuthenticationError, LoginManager)
		self.assertRaises(ragapp.AuthenticationError, LoginManager)
		self.assertRaises(ragapp.AuthenticationError, LoginManager)

		# REMOVE ME: current logic allows allow_consecutive_login_attempts+1 attempts
		# before raising security exception, remove below line when that is fixed.
		self.assertRaises(ragapp.AuthenticationError, LoginManager)
		self.assertRaises(ragapp.SecurityException, LoginManager)
		time.sleep(5)
		self.assertRaises(ragapp.AuthenticationError, LoginManager)

		ragapp.local.form_dict = ragapp._dict()


def update_system_settings(args):
	doc = ragapp.get_doc("System Settings")
	doc.update(args)
	doc.flags.ignore_mandatory = 1
	doc.save()
