import ragapp


def execute():
	ragapp.delete_doc_if_exists("DocType", "Web View")
	ragapp.delete_doc_if_exists("DocType", "Web View Component")
	ragapp.delete_doc_if_exists("DocType", "CSS Class")
