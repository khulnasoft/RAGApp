import ragapp
from ragapp.cache_manager import clear_defaults_cache


def execute():
	ragapp.db.set_default(
		"suspend_email_queue",
		ragapp.db.get_default("hold_queue", "Administrator") or 0,
		parent="__default",
	)

	ragapp.db.delete("DefaultValue", {"defkey": "hold_queue"})
	clear_defaults_cache()
