import ragapp
from ragapp.model.utils.rename_field import rename_field


def execute():
	if not ragapp.db.table_exists("Dashboard Chart"):
		return

	ragapp.reload_doc("desk", "doctype", "dashboard_chart")

	if ragapp.db.has_column("Dashboard Chart", "is_custom"):
		rename_field("Dashboard Chart", "is_custom", "use_report_chart")
