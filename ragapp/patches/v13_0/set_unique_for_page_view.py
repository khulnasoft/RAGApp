import ragapp


def execute():
	ragapp.reload_doc("website", "doctype", "web_page_view", force=True)
	site_url = ragapp.utils.get_site_url(ragapp.local.site)
	ragapp.db.sql(f"""UPDATE `tabWeb Page View` set is_unique=1 where referrer LIKE '%{site_url}%'""")
