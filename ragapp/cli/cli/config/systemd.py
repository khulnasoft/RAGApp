# imports - standard imports
import getpass
import os

# imports - third partyimports
import click

# imports - module imports
import cli
from cli.app import use_rq
from cli.cli import Cli
from cli.config.common_site_config import (
	get_gunicorn_workers,
	update_config,
	get_default_max_requests,
	compute_max_requests_jitter,
)
from cli.utils import exec_cmd, which, get_cli_name


def generate_systemd_config(
	cli_path,
	user=None,
	yes=False,
	stop=False,
	create_symlinks=False,
	delete_symlinks=False,
):

	if not user:
		user = getpass.getuser()

	config = Cli(cli_path).conf

	cli_dir = os.path.abspath(cli_path)
	cli_name = get_cli_name(cli_path)

	if stop:
		exec_cmd(
			f"sudo systemctl stop -- $(systemctl show -p Requires {cli_name}.target | cut -d= -f2)"
		)
		return

	if create_symlinks:
		_create_symlinks(cli_path)
		return

	if delete_symlinks:
		_delete_symlinks(cli_path)
		return

	number_of_workers = config.get("background_workers") or 1
	background_workers = []
	for i in range(number_of_workers):
		background_workers.append(
			get_cli_name(cli_path) + "-ragapp-default-worker@" + str(i + 1) + ".service"
		)

	for i in range(number_of_workers):
		background_workers.append(
			get_cli_name(cli_path) + "-ragapp-short-worker@" + str(i + 1) + ".service"
		)

	for i in range(number_of_workers):
		background_workers.append(
			get_cli_name(cli_path) + "-ragapp-long-worker@" + str(i + 1) + ".service"
		)

	web_worker_count = config.get(
		"gunicorn_workers", get_gunicorn_workers()["gunicorn_workers"]
	)
	max_requests = config.get(
		"gunicorn_max_requests", get_default_max_requests(web_worker_count)
	)

	cli_info = {
		"cli_dir": cli_dir,
		"sites_dir": os.path.join(cli_dir, "sites"),
		"user": user,
		"use_rq": use_rq(cli_path),
		"http_timeout": config.get("http_timeout", 120),
		"redis_server": which("redis-server"),
		"node": which("node") or which("nodejs"),
		"redis_cache_config": os.path.join(cli_dir, "config", "redis_cache.conf"),
		"redis_queue_config": os.path.join(cli_dir, "config", "redis_queue.conf"),
		"webserver_port": config.get("webserver_port", 8000),
		"gunicorn_workers": web_worker_count,
		"gunicorn_max_requests": max_requests,
		"gunicorn_max_requests_jitter": compute_max_requests_jitter(max_requests),
		"cli_name": get_cli_name(cli_path),
		"worker_target_wants": " ".join(background_workers),
		"cli_cmd": which("cli"),
	}

	if not yes:
		click.confirm(
			"current systemd configuration will be overwritten. Do you want to continue?",
			abort=True,
		)

	setup_systemd_directory(cli_path)
	setup_main_config(cli_info, cli_path)
	setup_workers_config(cli_info, cli_path)
	setup_web_config(cli_info, cli_path)
	setup_redis_config(cli_info, cli_path)

	update_config({"restart_systemd_on_update": False}, cli_path=cli_path)
	update_config({"restart_supervisor_on_update": False}, cli_path=cli_path)


def setup_systemd_directory(cli_path):
	if not os.path.exists(os.path.join(cli_path, "config", "systemd")):
		os.makedirs(os.path.join(cli_path, "config", "systemd"))


def setup_main_config(cli_info, cli_path):
	# Main config
	cli_template = cli.config.env().get_template("systemd/ragapp-cli.target")
	cli_config = cli_template.render(**cli_info)
	cli_config_path = os.path.join(
		cli_path, "config", "systemd", cli_info.get("cli_name") + ".target"
	)

	with open(cli_config_path, "w") as f:
		f.write(cli_config)


def setup_workers_config(cli_info, cli_path):
	# Worker Group
	cli_workers_target_template = cli.config.env().get_template(
		"systemd/ragapp-cli-workers.target"
	)
	cli_default_worker_template = cli.config.env().get_template(
		"systemd/ragapp-cli-ragapp-default-worker.service"
	)
	cli_short_worker_template = cli.config.env().get_template(
		"systemd/ragapp-cli-ragapp-short-worker.service"
	)
	cli_long_worker_template = cli.config.env().get_template(
		"systemd/ragapp-cli-ragapp-long-worker.service"
	)
	cli_schedule_worker_template = cli.config.env().get_template(
		"systemd/ragapp-cli-ragapp-schedule.service"
	)

	cli_workers_target_config = cli_workers_target_template.render(**cli_info)
	cli_default_worker_config = cli_default_worker_template.render(**cli_info)
	cli_short_worker_config = cli_short_worker_template.render(**cli_info)
	cli_long_worker_config = cli_long_worker_template.render(**cli_info)
	cli_schedule_worker_config = cli_schedule_worker_template.render(**cli_info)

	cli_workers_target_config_path = os.path.join(
		cli_path, "config", "systemd", cli_info.get("cli_name") + "-workers.target"
	)
	cli_default_worker_config_path = os.path.join(
		cli_path,
		"config",
		"systemd",
		cli_info.get("cli_name") + "-ragapp-default-worker@.service",
	)
	cli_short_worker_config_path = os.path.join(
		cli_path,
		"config",
		"systemd",
		cli_info.get("cli_name") + "-ragapp-short-worker@.service",
	)
	cli_long_worker_config_path = os.path.join(
		cli_path,
		"config",
		"systemd",
		cli_info.get("cli_name") + "-ragapp-long-worker@.service",
	)
	cli_schedule_worker_config_path = os.path.join(
		cli_path,
		"config",
		"systemd",
		cli_info.get("cli_name") + "-ragapp-schedule.service",
	)

	with open(cli_workers_target_config_path, "w") as f:
		f.write(cli_workers_target_config)

	with open(cli_default_worker_config_path, "w") as f:
		f.write(cli_default_worker_config)

	with open(cli_short_worker_config_path, "w") as f:
		f.write(cli_short_worker_config)

	with open(cli_long_worker_config_path, "w") as f:
		f.write(cli_long_worker_config)

	with open(cli_schedule_worker_config_path, "w") as f:
		f.write(cli_schedule_worker_config)


def setup_web_config(cli_info, cli_path):
	# Web Group
	cli_web_target_template = cli.config.env().get_template(
		"systemd/ragapp-cli-web.target"
	)
	cli_web_service_template = cli.config.env().get_template(
		"systemd/ragapp-cli-ragapp-web.service"
	)
	cli_node_socketio_template = cli.config.env().get_template(
		"systemd/ragapp-cli-node-socketio.service"
	)

	cli_web_target_config = cli_web_target_template.render(**cli_info)
	cli_web_service_config = cli_web_service_template.render(**cli_info)
	cli_node_socketio_config = cli_node_socketio_template.render(**cli_info)

	cli_web_target_config_path = os.path.join(
		cli_path, "config", "systemd", cli_info.get("cli_name") + "-web.target"
	)
	cli_web_service_config_path = os.path.join(
		cli_path, "config", "systemd", cli_info.get("cli_name") + "-ragapp-web.service"
	)
	cli_node_socketio_config_path = os.path.join(
		cli_path,
		"config",
		"systemd",
		cli_info.get("cli_name") + "-node-socketio.service",
	)

	with open(cli_web_target_config_path, "w") as f:
		f.write(cli_web_target_config)

	with open(cli_web_service_config_path, "w") as f:
		f.write(cli_web_service_config)

	with open(cli_node_socketio_config_path, "w") as f:
		f.write(cli_node_socketio_config)


def setup_redis_config(cli_info, cli_path):
	# Redis Group
	cli_redis_target_template = cli.config.env().get_template(
		"systemd/ragapp-cli-redis.target"
	)
	cli_redis_cache_template = cli.config.env().get_template(
		"systemd/ragapp-cli-redis-cache.service"
	)
	cli_redis_queue_template = cli.config.env().get_template(
		"systemd/ragapp-cli-redis-queue.service"
	)

	cli_redis_target_config = cli_redis_target_template.render(**cli_info)
	cli_redis_cache_config = cli_redis_cache_template.render(**cli_info)
	cli_redis_queue_config = cli_redis_queue_template.render(**cli_info)

	cli_redis_target_config_path = os.path.join(
		cli_path, "config", "systemd", cli_info.get("cli_name") + "-redis.target"
	)
	cli_redis_cache_config_path = os.path.join(
		cli_path, "config", "systemd", cli_info.get("cli_name") + "-redis-cache.service"
	)
	cli_redis_queue_config_path = os.path.join(
		cli_path, "config", "systemd", cli_info.get("cli_name") + "-redis-queue.service"
	)

	with open(cli_redis_target_config_path, "w") as f:
		f.write(cli_redis_target_config)

	with open(cli_redis_cache_config_path, "w") as f:
		f.write(cli_redis_cache_config)

	with open(cli_redis_queue_config_path, "w") as f:
		f.write(cli_redis_queue_config)


def _create_symlinks(cli_path):
	cli_dir = os.path.abspath(cli_path)
	etc_systemd_system = os.path.join("/", "etc", "systemd", "system")
	config_path = os.path.join(cli_dir, "config", "systemd")
	unit_files = get_unit_files(cli_dir)
	for unit_file in unit_files:
		filename = "".join(unit_file)
		exec_cmd(
			f'sudo ln -s {config_path}/{filename} {etc_systemd_system}/{"".join(unit_file)}'
		)
	exec_cmd("sudo systemctl daemon-reload")


def _delete_symlinks(cli_path):
	cli_dir = os.path.abspath(cli_path)
	etc_systemd_system = os.path.join("/", "etc", "systemd", "system")
	unit_files = get_unit_files(cli_dir)
	for unit_file in unit_files:
		exec_cmd(f'sudo rm {etc_systemd_system}/{"".join(unit_file)}')
	exec_cmd("sudo systemctl daemon-reload")


def get_unit_files(cli_path):
	cli_name = get_cli_name(cli_path)
	unit_files = [
		[cli_name, ".target"],
		[cli_name + "-workers", ".target"],
		[cli_name + "-web", ".target"],
		[cli_name + "-redis", ".target"],
		[cli_name + "-ragapp-default-worker@", ".service"],
		[cli_name + "-ragapp-short-worker@", ".service"],
		[cli_name + "-ragapp-long-worker@", ".service"],
		[cli_name + "-ragapp-schedule", ".service"],
		[cli_name + "-ragapp-web", ".service"],
		[cli_name + "-node-socketio", ".service"],
		[cli_name + "-redis-cache", ".service"],
		[cli_name + "-redis-queue", ".service"],
	]
	return unit_files
