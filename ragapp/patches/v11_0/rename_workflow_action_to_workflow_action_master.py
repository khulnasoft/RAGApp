import ragapp
from ragapp.model.rename_doc import rename_doc


def execute():
	if ragapp.db.table_exists("Workflow Action") and not ragapp.db.table_exists("Workflow Action Master"):
		rename_doc("DocType", "Workflow Action", "Workflow Action Master")
		ragapp.reload_doc("workflow", "doctype", "workflow_action_master")
