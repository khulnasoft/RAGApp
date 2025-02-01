# Copyright (c) 2020, Ragapp Technologies Pvt. Ltd. and Contributors
# License: MIT. See LICENSE

import ragapp


def execute():
	if ragapp.db.exists("DocType", "Onboarding"):
		ragapp.rename_doc("DocType", "Onboarding", "Module Onboarding", ignore_if_exists=True)
