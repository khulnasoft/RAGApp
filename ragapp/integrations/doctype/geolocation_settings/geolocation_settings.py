# Copyright (c) 2024, Ragapp Technologies and contributors
# For license information, please see license.txt

import ragapp
from ragapp import _
from ragapp.model.document import Document
from ragapp.utils import get_url

from .providers.geoapify import Geoapify
from .providers.here import Here
from .providers.nomatim import Nomatim


class GeolocationSettings(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from ragapp.types import DF

		api_key: DF.Password | None
		base_url: DF.Data | None
		enable_address_autocompletion: DF.Check
		provider: DF.Literal["Geoapify", "Nomatim", "HERE"]
	# end: auto-generated types

	pass


@ragapp.whitelist()
def autocomplete(txt: str) -> list[dict]:
	if not txt:
		return []

	settings = ragapp.get_single("Geolocation Settings")
	if not settings.enable_address_autocompletion:
		return []

	if settings.provider == "Geoapify":
		provider = Geoapify(settings.get_password("api_key"), ragapp.local.lang)
	elif settings.provider == "Nomatim":
		provider = Nomatim(
			base_url=settings.base_url,
			referer=get_url(),
			lang=ragapp.local.lang,
		)
	elif settings.provider == "HERE":
		provider = Here(settings.get_password("api_key"), ragapp.local.lang)
	else:
		ragapp.throw(_("This geolocation provider is not supported yet."))

	return list(provider.autocomplete(txt))
