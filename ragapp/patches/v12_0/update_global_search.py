import ragapp
from ragapp.desk.page.setup_wizard.install_fixtures import update_global_search_doctypes


def execute():
	ragapp.reload_doc("desk", "doctype", "global_search_doctype")
	ragapp.reload_doc("desk", "doctype", "global_search_settings")
	update_global_search_doctypes()
