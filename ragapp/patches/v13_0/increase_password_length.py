import ragapp


def execute():
	ragapp.db.change_column_type("__Auth", column="password", type="TEXT")
