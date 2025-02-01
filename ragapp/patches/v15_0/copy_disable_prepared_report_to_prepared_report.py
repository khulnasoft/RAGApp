import ragapp


def execute():
	table = ragapp.qb.DocType("Report")
	ragapp.qb.update(table).set(table.prepared_report, 0).where(table.disable_prepared_report == 1)
