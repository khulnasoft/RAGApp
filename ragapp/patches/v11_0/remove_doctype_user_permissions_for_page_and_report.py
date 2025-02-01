# Copyright (c) 2025, KhulnaSoft, Ltd and Contributors
# License: MIT. See LICENSE

import ragapp


def execute():
	ragapp.delete_doc_if_exists("DocType", "User Permission for Page and Report")
