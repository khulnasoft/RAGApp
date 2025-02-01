# Copyright (c) 2025, KhulnaSoft, Ltd and Contributors
# License: MIT. See LICENSE

# pre loaded

import ragapp
from ragapp.tests import IntegrationTestCase, UnitTestCase


class UnitTestCurrency(UnitTestCase):
	"""
	Unit tests for Currency.
	Use this class for testing individual functions and methods.
	"""

	pass


class TestUser(IntegrationTestCase):
	def test_default_currency_on_setup(self):
		usd = ragapp.get_doc("Currency", "USD")
		self.assertDocumentEqual({"enabled": 1, "fraction": "Cent"}, usd)
