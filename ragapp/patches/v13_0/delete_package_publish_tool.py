# Copyright (c) 2020, Ragapp Technologies Pvt. Ltd. and Contributors
# License: MIT. See LICENSE

import ragapp


def execute():
	ragapp.delete_doc("DocType", "Package Publish Tool", ignore_missing=True)
	ragapp.delete_doc("DocType", "Package Document Type", ignore_missing=True)
	ragapp.delete_doc("DocType", "Package Publish Target", ignore_missing=True)
