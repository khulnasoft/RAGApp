# Copyright (c) 2025, KhulnaSoft, Ltd and Contributors
# License: MIT. See LICENSE

import ragapp

sitemap = 1


def get_context(context):
	context.doc = ragapp.get_cached_doc("About Us Settings")

	return context
