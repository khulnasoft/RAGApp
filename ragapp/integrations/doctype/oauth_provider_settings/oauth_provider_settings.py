# Copyright (c) 2015, Ragapp Technologies and contributors
# License: MIT. See LICENSE

import ragapp
from ragapp import _
from ragapp.model.document import Document


class OAuthProviderSettings(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from ragapp.types import DF

		skip_authorization: DF.Literal["Force", "Auto"]
	# end: auto-generated types

	pass


def get_oauth_settings():
	"""Return OAuth settings."""
	return ragapp._dict(
		{"skip_authorization": ragapp.db.get_single_value("OAuth Provider Settings", "skip_authorization")}
	)
