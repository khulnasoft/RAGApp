# Copyright (c) 2020, Ragapp Technologies Pvt. Ltd. and Contributors
# License: MIT. See LICENSE

import ragapp


def execute():
	"""Enable all the existing Client script"""

	ragapp.db.sql(
		"""
		UPDATE `tabClient Script` SET enabled=1
	"""
	)
