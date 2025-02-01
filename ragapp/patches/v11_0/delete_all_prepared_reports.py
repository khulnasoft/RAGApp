import ragapp


def execute():
	if ragapp.db.table_exists("Prepared Report"):
		ragapp.reload_doc("core", "doctype", "prepared_report")
		prepared_reports = ragapp.get_all("Prepared Report")
		for report in prepared_reports:
			ragapp.delete_doc("Prepared Report", report.name)
