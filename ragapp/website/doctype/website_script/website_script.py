# Copyright (c) 2025, KhulnaSoft, Ltd and Contributors
# License: MIT. See LICENSE

# License: MIT. See LICENSE

import ragapp
from ragapp.model.document import Document


class WebsiteScript(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from ragapp.types import DF

		javascript: DF.Code | None
	# end: auto-generated types

	def on_update(self):
		"""clear cache"""
		ragapp.clear_cache(user="Guest")

		from ragapp.website.utils import clear_cache

		clear_cache()
