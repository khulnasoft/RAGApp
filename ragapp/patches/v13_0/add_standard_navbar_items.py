import ragapp
from ragapp.utils.install import add_standard_navbar_items


def execute():
	# Add standard navbar items for NxERP in Navbar Settings
	ragapp.reload_doc("core", "doctype", "navbar_settings")
	ragapp.reload_doc("core", "doctype", "navbar_item")
	add_standard_navbar_items()
