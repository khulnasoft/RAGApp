import ragapp
from ragapp.model.rename_doc import rename_doc


def execute():
	if ragapp.db.exists("DocType", "Client Script"):
		return

	ragapp.flags.ignore_route_conflict_validation = True
	rename_doc("DocType", "Custom Script", "Client Script")
	ragapp.flags.ignore_route_conflict_validation = False

	ragapp.reload_doctype("Client Script", force=True)
