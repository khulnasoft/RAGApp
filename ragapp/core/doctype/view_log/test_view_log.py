# Copyright (c) 2018, Ragapp Technologies and Contributors
# License: MIT. See LICENSE
import ragapp
from ragapp.tests import IntegrationTestCase, UnitTestCase


class UnitTestViewLog(UnitTestCase):
	"""
	Unit tests for ViewLog.
	Use this class for testing individual functions and methods.
	"""

	pass


class TestViewLog(IntegrationTestCase):
	def tearDown(self):
		ragapp.set_user("Administrator")

	def test_if_user_is_added(self):
		ev = ragapp.get_doc(
			{
				"doctype": "Event",
				"subject": "test event for view logs",
				"starts_on": "2018-06-04 14:11:00",
				"event_type": "Public",
			}
		).insert()

		ragapp.set_user("test@example.com")

		from ragapp.desk.form.load import getdoc

		# load the form
		getdoc("Event", ev.name)
		a = ragapp.get_value(
			doctype="View Log",
			filters={"reference_doctype": "Event", "reference_name": ev.name},
			fieldname=["viewed_by"],
		)

		self.assertEqual("test@example.com", a)
		self.assertNotEqual("test1@example.com", a)
