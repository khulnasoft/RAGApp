# Copyright (c) 2022, Ragapp and Contributors
# License: MIT. See LICENSE


import ragapp
from ragapp.model import data_field_options


def execute():
	custom_field = ragapp.qb.DocType("Custom Field")
	(
		ragapp.qb.update(custom_field)
		.set(custom_field.options, None)
		.where((custom_field.fieldtype == "Data") & (custom_field.options.notin(data_field_options)))
	).run()
