# Copyright (c) 2022, Ragapp Technologies Pvt. Ltd. and Contributors
# License: MIT. See LICENSE
import ragapp
from ragapp.tests import IntegrationTestCase
from ragapp.utils.modules import get_modules_from_all_apps_for_user


class TestConfig(IntegrationTestCase):
	def test_get_modules(self):
		ragapp_modules = ragapp.get_all("Module Def", filters={"app_name": "ragapp"}, pluck="name")
		all_modules_data = get_modules_from_all_apps_for_user()
		all_modules = [x["module_name"] for x in all_modules_data]
		self.assertIsInstance(all_modules_data, list)
		self.assertFalse([x for x in ragapp_modules if x not in all_modules])
