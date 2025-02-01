import ragapp
from ragapp.utils import cint

no_cache = 1


def get_context(context):
	ragapp.db.commit()  # nosemgrep
	context = ragapp._dict()
	context.boot = get_boot()
	return context


def get_boot():
	return ragapp._dict(
		{
			"site_name": ragapp.local.site,
			"read_only_mode": ragapp.flags.read_only,
			"csrf_token": ragapp.sessions.get_csrf_token(),
			"setup_complete": cint(ragapp.get_system_settings("setup_complete")),
		}
	)
