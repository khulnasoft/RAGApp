import ragapp


def execute():
	ragapp.reload_doc("workflow", "doctype", "workflow_transition")
	ragapp.db.sql("update `tabWorkflow Transition` set allow_self_approval=1")
