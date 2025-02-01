import ragapp


def execute():
	"""Remove stale docfields from legacy version"""
	ragapp.db.delete("DocField", {"options": "Data Import", "parent": "Data Import Legacy"})
