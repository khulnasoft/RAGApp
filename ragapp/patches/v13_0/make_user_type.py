import ragapp
from ragapp.utils.install import create_user_type


def execute():
	ragapp.reload_doc("core", "doctype", "role")
	ragapp.reload_doc("core", "doctype", "user_document_type")
	ragapp.reload_doc("core", "doctype", "user_type_module")
	ragapp.reload_doc("core", "doctype", "user_select_document_type")
	ragapp.reload_doc("core", "doctype", "user_type")

	create_user_type()
