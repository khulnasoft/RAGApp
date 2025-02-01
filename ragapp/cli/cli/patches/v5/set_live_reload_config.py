from cli.config.common_site_config import update_config


def execute(cli_path):
	update_config({"live_reload": True}, cli_path)
