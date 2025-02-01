# Copyright (c) 2015, Ragapp Technologies and Contributors
# License: MIT. See LICENSE
import ragapp
from ragapp.contacts.doctype.address_template.address_template import get_default_address_template
from ragapp.tests import IntegrationTestCase, UnitTestCase
from ragapp.utils.jinja import validate_template


class UnitTestAddressTemplate(UnitTestCase):
	"""
	Unit tests for AddressTemplate.
	Use this class for testing individual functions and methods.
	"""

	pass


class TestAddressTemplate(IntegrationTestCase):
	def setUp(self) -> None:
		ragapp.db.delete("Address Template", {"country": "India"})
		ragapp.db.delete("Address Template", {"country": "Brazil"})

	def test_default_address_template(self):
		validate_template(get_default_address_template())

	def test_default_is_unset(self):
		ragapp.get_doc({"doctype": "Address Template", "country": "India", "is_default": 1}).insert()

		self.assertEqual(ragapp.db.get_value("Address Template", "India", "is_default"), 1)

		ragapp.get_doc({"doctype": "Address Template", "country": "Brazil", "is_default": 1}).insert()

		self.assertEqual(ragapp.db.get_value("Address Template", "India", "is_default"), 0)
		self.assertEqual(ragapp.db.get_value("Address Template", "Brazil", "is_default"), 1)

	def test_delete_address_template(self):
		india = ragapp.get_doc({"doctype": "Address Template", "country": "India", "is_default": 0}).insert()

		brazil = ragapp.get_doc(
			{"doctype": "Address Template", "country": "Brazil", "is_default": 1}
		).insert()

		india.reload()  # might have been modified by the second template
		india.delete()  # should not raise an error

		self.assertRaises(ragapp.ValidationError, brazil.delete)
