import ragapp

RAGAPP_CLOUD_DOMAINS = ("ragapp.cloud", "erpnext.com", "ragapphr.com")


def on_ragappcloud() -> bool:
	"""Returns true if running on Ragapp Cloud.


	Useful for modifying few features for better UX."""
	return ragapp.local.site.endswith(RAGAPP_CLOUD_DOMAINS)
