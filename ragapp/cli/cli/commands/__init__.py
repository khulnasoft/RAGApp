# imports - third party imports
import click

# imports - module imports
from cli.utils.cli import (
	MultiCommandGroup,
	print_cli_version,
	use_experimental_feature,
	setup_verbosity,
)


@click.group(cls=MultiCommandGroup)
@click.option(
	"--version",
	is_flag=True,
	is_eager=True,
	callback=print_cli_version,
	expose_value=False,
)
@click.option(
	"--use-feature",
	is_eager=True,
	callback=use_experimental_feature,
	expose_value=False,
)
@click.option(
	"-v",
	"--verbose",
	is_flag=True,
	callback=setup_verbosity,
	expose_value=False,
)
def cli_command(cli_path="."):
	import cli

	cli.set_ragapp_version(cli_path=cli_path)


from cli.commands.make import (
	drop,
	exclude_app_for_update,
	get_app,
	include_app_for_update,
	init,
	new_app,
	pip,
	remove_app,
	validate_dependencies,
)

cli_command.add_command(init)
cli_command.add_command(drop)
cli_command.add_command(get_app)
cli_command.add_command(new_app)
cli_command.add_command(remove_app)
cli_command.add_command(exclude_app_for_update)
cli_command.add_command(include_app_for_update)
cli_command.add_command(pip)
cli_command.add_command(validate_dependencies)


from cli.commands.update import (
	retry_upgrade,
	switch_to_branch,
	switch_to_develop,
	update,
)

cli_command.add_command(update)
cli_command.add_command(retry_upgrade)
cli_command.add_command(switch_to_branch)
cli_command.add_command(switch_to_develop)


from cli.commands.utils import (
	app_cache_helper,
	backup_all_sites,
	cli_src,
	disable_production,
	download_translations,
	find_clies,
	migrate_env,
	renew_lets_encrypt,
	restart,
	set_mariadb_host,
	set_nginx_port,
	set_redis_cache_host,
	set_redis_queue_host,
	set_redis_socketio_host,
	set_ssl_certificate,
	set_ssl_certificate_key,
	set_url_root,
	start,
)

cli_command.add_command(start)
cli_command.add_command(restart)
cli_command.add_command(set_nginx_port)
cli_command.add_command(set_ssl_certificate)
cli_command.add_command(set_ssl_certificate_key)
cli_command.add_command(set_url_root)
cli_command.add_command(set_mariadb_host)
cli_command.add_command(set_redis_cache_host)
cli_command.add_command(set_redis_queue_host)
cli_command.add_command(set_redis_socketio_host)
cli_command.add_command(download_translations)
cli_command.add_command(backup_all_sites)
cli_command.add_command(renew_lets_encrypt)
cli_command.add_command(disable_production)
cli_command.add_command(cli_src)
cli_command.add_command(find_clies)
cli_command.add_command(migrate_env)
cli_command.add_command(app_cache_helper)

from cli.commands.setup import setup

cli_command.add_command(setup)


from cli.commands.config import config

cli_command.add_command(config)

from cli.commands.git import remote_reset_url, remote_set_url, remote_urls

cli_command.add_command(remote_set_url)
cli_command.add_command(remote_reset_url)
cli_command.add_command(remote_urls)

from cli.commands.install import install

cli_command.add_command(install)
