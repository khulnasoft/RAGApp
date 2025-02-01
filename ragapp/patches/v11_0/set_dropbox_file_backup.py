import ragapp
from ragapp.utils import cint


def execute():
	ragapp.reload_doctype("Dropbox Settings")
	check_dropbox_enabled = cint(ragapp.db.get_single_value("Dropbox Settings", "enabled"))
	if check_dropbox_enabled == 1:
		ragapp.db.set_single_value("Dropbox Settings", "file_backup", 1)
