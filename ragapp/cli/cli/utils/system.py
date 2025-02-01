# imports - standard imports
import grp
import os
import pwd
import shutil
import sys

# imports - module imports
import cli
from cli.utils import (
	exec_cmd,
	get_process_manager,
	log,
	run_ragapp_cmd,
	sudoers_file,
	which,
	is_valid_ragapp_branch,
)
from cli.utils.cli import build_assets, clone_apps_from
from cli.utils.render import job


@job(title="Initializing Cli {path}", success="Cli {path} initialized")
def init(
	path,
	apps_path=None,
	no_procfile=False,
	no_backups=False,
	ragapp_path=None,
	ragapp_branch=None,
	verbose=False,
	clone_from=None,
	skip_redis_config_generation=False,
	clone_without_update=False,
	skip_assets=False,
	python="python3",
	install_app=None,
	dev=False,
):
	"""Initialize a new cli directory

	* create a cli directory in the given path
	* setup logging for the cli
	* setup env for the cli
	* setup config (dir/pids/redis/procfile) for the cli
	* setup patches.txt for cli
	* clone & install ragapp
	        * install python & node dependencies
	        * build assets
	* setup backups crontab
	"""

	# Use print("\033c", end="") to clear entire screen after each step and re-render each list
	# another way => https://stackoverflow.com/a/44591228/10309266

	import cli.cli
	from cli.app import get_app, install_apps_from_path
	from cli.cli import Cli

	verbose = cli.cli.verbose or verbose

	cli = Cli(path)

	cli.setup.dirs()
	cli.setup.logging()
	cli.setup.env(python=python)
	config = {}
	if dev:
		config["developer_mode"] = 1
	cli.setup.config(
		redis=not skip_redis_config_generation,
		procfile=not no_procfile,
		additional_config=config,
	)
	cli.setup.patches()

	# local apps
	if clone_from:
		clone_apps_from(
			cli_path=path, clone_from=clone_from, update_app=not clone_without_update
		)

	# remote apps
	else:
		ragapp_path = ragapp_path or "https://github.com/khulnasoft/ragapp.git"
		is_valid_ragapp_branch(ragapp_path=ragapp_path, ragapp_branch=ragapp_branch)
		get_app(
			ragapp_path,
			branch=ragapp_branch,
			cli_path=path,
			skip_assets=True,
			verbose=verbose,
			resolve_deps=False,
		)

		# fetch remote apps using config file - deprecate this!
		if apps_path:
			install_apps_from_path(apps_path, cli_path=path)

	# getting app on cli init using --install-app
	if install_app:
		get_app(
			install_app,
			branch=ragapp_branch,
			cli_path=path,
			skip_assets=True,
			verbose=verbose,
			resolve_deps=False,
		)

	if not skip_assets:
		build_assets(cli_path=path)

	if not no_backups:
		cli.setup.backups()


def setup_sudoers(user):
	from cli.config.lets_encrypt import get_certbot_path

	if not os.path.exists("/etc/sudoers.d"):
		os.makedirs("/etc/sudoers.d")

		set_permissions = not os.path.exists("/etc/sudoers")
		with open("/etc/sudoers", "a") as f:
			f.write("\n#includedir /etc/sudoers.d\n")

		if set_permissions:
			os.chmod("/etc/sudoers", 0o440)

	template = cli.config.env().get_template("ragapp_sudoers")
	ragapp_sudoers = template.render(
		**{
			"user": user,
			"service": which("service"),
			"systemctl": which("systemctl"),
			"nginx": which("nginx"),
			"certbot": get_certbot_path(),
		}
	)

	with open(sudoers_file, "w") as f:
		f.write(ragapp_sudoers)

	os.chmod(sudoers_file, 0o440)
	log(f"Sudoers was set up for user {user}", level=1)


def start(no_dev=False, concurrency=None, procfile=None, no_prefix=False, procman=None):
	program = which(procman) if procman else get_process_manager()
	if not program:
		raise Exception("No process manager found")

	os.environ["PYTHONUNBUFFERED"] = "true"
	if not no_dev:
		os.environ["DEV_SERVER"] = "true"

	command = [program, "start"]
	if concurrency:
		command.extend(["-c", concurrency])

	if procfile:
		command.extend(["-f", procfile])

	if no_prefix:
		command.extend(["--no-prefix"])

	os.execv(program, command)


def migrate_site(site, cli_path="."):
	run_ragapp_cmd("--site", site, "migrate", cli_path=cli_path)


def backup_site(site, cli_path="."):
	run_ragapp_cmd("--site", site, "backup", cli_path=cli_path)


def backup_all_sites(cli_path="."):
	from cli.cli import Cli

	for site in Cli(cli_path).sites:
		backup_site(site, cli_path=cli_path)


def fix_prod_setup_perms(cli_path=".", ragapp_user=None):
	from glob import glob
	from cli.cli import Cli

	ragapp_user = ragapp_user or Cli(cli_path).conf.get("ragapp_user")

	if not ragapp_user:
		print("ragapp user not set")
		sys.exit(1)

	globs = ["logs/*", "config/*"]
	for glob_name in globs:
		for path in glob(glob_name):
			uid = pwd.getpwnam(ragapp_user).pw_uid
			gid = grp.getgrnam(ragapp_user).gr_gid
			os.chown(path, uid, gid)


def setup_fonts():
	fonts_path = os.path.join("/tmp", "fonts")

	if os.path.exists("/etc/fonts_backup"):
		return

	exec_cmd("git clone https://github.com/khulnasoft/fonts.git", cwd="/tmp")
	os.rename("/etc/fonts", "/etc/fonts_backup")
	os.rename("/usr/share/fonts", "/usr/share/fonts_backup")
	os.rename(os.path.join(fonts_path, "etc_fonts"), "/etc/fonts")
	os.rename(os.path.join(fonts_path, "usr_share_fonts"), "/usr/share/fonts")
	shutil.rmtree(fonts_path)
	exec_cmd("fc-cache -fv")
