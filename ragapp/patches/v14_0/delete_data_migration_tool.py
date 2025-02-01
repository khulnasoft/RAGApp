# Copyright (c) 2022, Ragapp Technologies Pvt. Ltd. and Contributors
# MIT License. See license.txt

import ragapp


def execute():
	doctypes = ragapp.get_all("DocType", {"module": "Data Migration", "custom": 0}, pluck="name")
	for doctype in doctypes:
		ragapp.delete_doc("DocType", doctype, ignore_missing=True)

	ragapp.delete_doc("Module Def", "Data Migration", ignore_missing=True, force=True)
