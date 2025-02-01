import ragapp


def execute():
	ragapp.delete_doc_if_exists("DocType", "Post")
	ragapp.delete_doc_if_exists("DocType", "Post Comment")
