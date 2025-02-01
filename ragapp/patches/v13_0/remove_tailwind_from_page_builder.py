# Copyright (c) 2020, Ragapp Technologies Pvt. Ltd. and Contributors
# License: MIT. See LICENSE

import ragapp


def execute():
	ragapp.reload_doc("website", "doctype", "web_page_block")
	# remove unused templates
	ragapp.delete_doc("Web Template", "Navbar with Links on Right", force=1)
	ragapp.delete_doc("Web Template", "Footer Horizontal", force=1)
