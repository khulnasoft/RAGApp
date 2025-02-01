import ragapp


def execute():
	ragapp.reload_doc("website", "doctype", "web_page_view", force=True)
	ragapp.db.sql("""UPDATE `tabWeb Page View` set path='/' where path=''""")
