import ragapp


def execute():
	if ragapp.db.db_type == "mariadb":
		ragapp.db.sql_ddl("alter table `tabSingles` modify column `value` longtext")
