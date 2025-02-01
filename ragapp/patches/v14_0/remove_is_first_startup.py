import ragapp


def execute():
	singles = ragapp.qb.Table("tabSingles")
	ragapp.qb.from_(singles).delete().where(
		(singles.doctype == "System Settings") & (singles.field == "is_first_startup")
	).run()
