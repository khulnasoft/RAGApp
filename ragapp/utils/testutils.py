# Copyright (c) 2025, KhulnaSoft, Ltd and Contributors
# License: MIT. See LICENSE
import ragapp


def add_custom_field(doctype, fieldname, fieldtype="Data", options=None):
	ragapp.get_doc(
		{
			"doctype": "Custom Field",
			"dt": doctype,
			"fieldname": fieldname,
			"fieldtype": fieldtype,
			"options": options,
		}
	).insert()


def clear_custom_fields(doctype):
	ragapp.db.delete("Custom Field", {"dt": doctype})
	ragapp.clear_cache(doctype=doctype)
