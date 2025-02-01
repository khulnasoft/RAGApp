# Copyright (c) 2024, Ragapp Technologies and Contributors
# See license.txt

import ragapp
from ragapp.tests import IntegrationTestCase, UnitTestCase


class UnitTestSystemHealthReport(UnitTestCase):
	"""
	Unit tests for SystemHealthReport.
	Use this class for testing individual functions and methods.
	"""

	pass


class TestSystemHealthReport(IntegrationTestCase):
	def test_it_works(self):
		ragapp.get_doc("System Health Report")
