VERSION = "5.0.0-dev"
PROJECT_NAME = "ragapp-cli"
RAGAPP_VERSION = None
current_path = None
updated_path = None
LOG_BUFFER = []


def set_ragapp_version(cli_path="."):
	from .utils.app import get_current_ragapp_version

	global RAGAPP_VERSION
	if not RAGAPP_VERSION:
		RAGAPP_VERSION = get_current_ragapp_version(cli_path=cli_path)
