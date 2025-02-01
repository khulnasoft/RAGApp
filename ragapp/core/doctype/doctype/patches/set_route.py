import ragapp
from ragapp.desk.utils import slug


def execute():
	for doctype in ragapp.get_all("DocType", ["name", "route"], dict(istable=0)):
		if not doctype.route:
			ragapp.db.set_value("DocType", doctype.name, "route", slug(doctype.name), update_modified=False)
