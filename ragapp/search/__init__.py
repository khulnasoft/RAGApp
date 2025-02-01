# Copyright (c) 2020, Ragapp Technologies Pvt. Ltd. and Contributors
# License: MIT. See LICENSE

import ragapp
from ragapp.search.full_text_search import FullTextSearch
from ragapp.search.website_search import WebsiteSearch
from ragapp.utils import cint


@ragapp.whitelist(allow_guest=True)
def web_search(query, scope=None, limit=20):
	limit = cint(limit)
	ws = WebsiteSearch(index_name="web_routes")
	return ws.search(query, scope, limit)
