# Copyright (c) 2025, KhulnaSoft, Ltd and Contributors
# License: MIT. See LICENSE

import json

import ragapp
from ragapp import _
from ragapp.geo.country_info import get_country_info
from ragapp.permissions import AUTOMATIC_ROLES
from ragapp.translate import send_translations, set_default_language
from ragapp.utils import cint, now, strip
from ragapp.utils.password import update_password

from . import install_fixtures


def get_setup_stages(args):  # nosemgrep
	# App setup stage functions should not include ragapp.db.commit
	# That is done by ragapp after successful completion of all stages
	stages = [
		{
			"status": _("Updating global settings"),
			"fail_msg": _("Failed to update global settings"),
			"tasks": [
				{"fn": update_global_settings, "args": args, "fail_msg": "Failed to update global settings"}
			],
		}
	]

	stages += get_stages_hooks(args) + get_setup_complete_hooks(args)

	stages.append(
		{
			# post executing hooks
			"status": _("Wrapping up"),
			"fail_msg": _("Failed to complete setup"),
			"tasks": [{"fn": run_post_setup_complete, "args": args, "fail_msg": "Failed to complete setup"}],
		}
	)

	return stages


@ragapp.whitelist()
def setup_complete(args):
	"""Calls hooks for `setup_wizard_complete`, sets home page as `desktop`
	and clears cache. If wizard breaks, calls `setup_wizard_exception` hook"""

	# Setup complete: do not throw an exception, let the user continue to desk
	if cint(ragapp.db.get_single_value("System Settings", "setup_complete")):
		return {"status": "ok"}

	args = parse_args(sanitize_input(args))
	stages = get_setup_stages(args)
	is_background_task = ragapp.conf.get("trigger_site_setup_in_background")

	if is_background_task:
		process_setup_stages.enqueue(stages=stages, user_input=args, is_background_task=True)
		return {"status": "registered"}
	else:
		return process_setup_stages(stages, args)


@ragapp.task()
def process_setup_stages(stages, user_input, is_background_task=False):
	from ragapp.utils.telemetry import capture

	capture("initated_server_side", "setup")
	try:
		ragapp.flags.in_setup_wizard = True
		current_task = None
		for idx, stage in enumerate(stages):
			ragapp.publish_realtime(
				"setup_task",
				{"progress": [idx, len(stages)], "stage_status": stage.get("status")},
				user=ragapp.session.user,
			)

			for task in stage.get("tasks"):
				current_task = task
				task.get("fn")(task.get("args"))
	except Exception:
		handle_setup_exception(user_input)
		message = current_task.get("fail_msg") if current_task else "Failed to complete setup"
		ragapp.log_error(title=f"Setup failed: {message}")
		if not is_background_task:
			ragapp.response["setup_wizard_failure_message"] = message
			raise
		ragapp.publish_realtime(
			"setup_task",
			{"status": "fail", "fail_msg": message},
			user=ragapp.session.user,
		)
	else:
		run_setup_success(user_input)
		capture("completed_server_side", "setup")
		if not is_background_task:
			return {"status": "ok"}
		ragapp.publish_realtime("setup_task", {"status": "ok"}, user=ragapp.session.user)
	finally:
		ragapp.flags.in_setup_wizard = False


def update_global_settings(args):  # nosemgrep
	if args.language and args.language != "English":
		set_default_language(get_language_code(args.lang))
		ragapp.db.commit()
	ragapp.clear_cache()

	update_system_settings(args)
	create_or_update_user(args)
	set_timezone(args)


def run_post_setup_complete(args):  # nosemgrep
	disable_future_access()
	ragapp.db.commit()
	ragapp.clear_cache()
	# HACK: due to race condition sometimes old doc stays in cache.
	# Remove this when we have reliable cache reset for docs
	ragapp.get_cached_doc("System Settings") and ragapp.get_doc("System Settings")


def run_setup_success(args):  # nosemgrep
	for hook in ragapp.get_hooks("setup_wizard_success"):
		ragapp.get_attr(hook)(args)
	install_fixtures.install()


def get_stages_hooks(args):  # nosemgrep
	stages = []
	for method in ragapp.get_hooks("setup_wizard_stages"):
		stages += ragapp.get_attr(method)(args)
	return stages


def get_setup_complete_hooks(args):  # nosemgrep
	return [
		{
			"status": "Executing method",
			"fail_msg": "Failed to execute method",
			"tasks": [
				{
					"fn": ragapp.get_attr(method),
					"args": args,
					"fail_msg": "Failed to execute method",
				}
			],
		}
		for method in ragapp.get_hooks("setup_wizard_complete")
	]


def handle_setup_exception(args):  # nosemgrep
	ragapp.db.rollback()
	if args:
		traceback = ragapp.get_traceback(with_context=True)
		print(traceback)
		for hook in ragapp.get_hooks("setup_wizard_exception"):
			ragapp.get_attr(hook)(traceback, args)


def update_system_settings(args):  # nosemgrep
	number_format = get_country_info(args.get("country")).get("number_format", "#,###.##")

	# replace these as float number formats, as they have 0 precision
	# and are currency number formats and not for floats
	if number_format == "#.###":
		number_format = "#.###,##"
	elif number_format == "#,###":
		number_format = "#,###.##"

	system_settings = ragapp.get_doc("System Settings", "System Settings")
	system_settings.update(
		{
			"country": args.get("country"),
			"language": get_language_code(args.get("language")) or "en",
			"time_zone": args.get("timezone"),
			"currency": args.get("currency"),
			"float_precision": 3,
			"rounding_method": "Banker's Rounding",
			"date_format": ragapp.db.get_value("Country", args.get("country"), "date_format"),
			"time_format": ragapp.db.get_value("Country", args.get("country"), "time_format"),
			"number_format": number_format,
			"enable_scheduler": 1 if not ragapp.flags.in_test else 0,
			"backup_limit": 3,  # Default for downloadable backups
			"enable_telemetry": cint(args.get("enable_telemetry")),
		}
	)
	system_settings.save()
	if args.get("enable_telemetry"):
		ragapp.db.set_default("session_recording_start", now())


def create_or_update_user(args):  # nosemgrep
	email = args.get("email")
	if not email:
		return

	first_name, last_name = args.get("full_name", ""), ""
	if " " in first_name:
		first_name, last_name = first_name.split(" ", 1)

	if user := ragapp.db.get_value("User", email, ["first_name", "last_name"], as_dict=True):
		if user.first_name != first_name or user.last_name != last_name:
			(
				ragapp.qb.update("User")
				.set("first_name", first_name)
				.set("last_name", last_name)
				.set("full_name", args.get("full_name"))
			).run()
	else:
		_mute_emails, ragapp.flags.mute_emails = ragapp.flags.mute_emails, True

		user = ragapp.new_doc("User")
		user.update(
			{
				"email": email,
				"first_name": first_name,
				"last_name": last_name,
			}
		)
		user.append_roles(*_get_default_roles())
		user.append_roles("System Manager")
		user.flags.no_welcome_mail = True
		user.insert()

		ragapp.flags.mute_emails = _mute_emails

	if args.get("password"):
		update_password(email, args.get("password"))


def set_timezone(args):  # nosemgrep
	if args.get("timezone"):
		for name in ragapp.STANDARD_USERS:
			ragapp.db.set_value("User", name, "time_zone", args.get("timezone"))


def parse_args(args):  # nosemgrep
	if not args:
		args = ragapp.local.form_dict
	if isinstance(args, str):
		args = json.loads(args)

	args = ragapp._dict(args)

	# strip the whitespace
	for key, value in args.items():
		if isinstance(value, str):
			args[key] = strip(value)

	return args


def sanitize_input(args):
	from ragapp.utils import is_html, strip_html_tags

	if isinstance(args, str):
		args = json.loads(args)

	for key, value in args.items():
		if is_html(value):
			args[key] = strip_html_tags(value)

	return args


def add_all_roles_to(name):
	user = ragapp.get_doc("User", name)
	user.append_roles(*_get_default_roles())
	user.save()


def _get_default_roles() -> set[str]:
	skip_roles = {
		"Administrator",
		"Customer",
		"Supplier",
		"Partner",
		"Employee",
	}.union(AUTOMATIC_ROLES)
	return set(ragapp.get_all("Role", pluck="name")) - skip_roles


def disable_future_access():
	ragapp.db.set_default("desktop:home_page", "workspace")
	# Enable onboarding after install
	ragapp.db.set_single_value("System Settings", "enable_onboarding", 1)

	ragapp.db.set_single_value("System Settings", "setup_complete", 1)


@ragapp.whitelist()
def load_messages(language):
	"""Load translation messages for given language from all `setup_wizard_requires`
	javascript files"""
	from ragapp.translate import get_messages_for_boot

	ragapp.clear_cache()
	set_default_language(get_language_code(language))
	ragapp.db.commit()
	send_translations(get_messages_for_boot())
	return ragapp.local.lang


@ragapp.whitelist()
def load_languages():
	language_codes = ragapp.db.sql(
		"select language_code, language_name from tabLanguage order by name", as_dict=True
	)
	codes_to_names = {}
	for d in language_codes:
		codes_to_names[d.language_code] = d.language_name
	return {
		"default_language": ragapp.db.get_value("Language", ragapp.local.lang, "language_name")
		or ragapp.local.lang,
		"languages": sorted(ragapp.db.sql_list("select language_name from tabLanguage order by name")),
		"codes_to_names": codes_to_names,
	}


@ragapp.whitelist()
def load_user_details():
	return {
		"full_name": ragapp.cache.hget("full_name", "signup"),
		"email": ragapp.cache.hget("email", "signup"),
	}


def prettify_args(args):  # nosemgrep
	# remove attachments
	for key, val in args.items():
		if isinstance(val, str) and "data:image" in val:
			filename = val.split("data:image", 1)[0].strip(", ")
			size = round((len(val) * 3 / 4) / 1048576.0, 2)
			args[key] = f"Image Attached: '{filename}' of size {size} MB"

	pretty_args = []
	pretty_args.extend(f"{key} = {args[key]}" for key in sorted(args))
	return pretty_args


def email_setup_wizard_exception(traceback, args):  # nosemgrep
	if not ragapp.conf.setup_wizard_exception_email:
		return

	pretty_args = prettify_args(args)
	message = """

#### Traceback

<pre>{traceback}</pre>

---

#### Setup Wizard Arguments

<pre>{args}</pre>

---

#### Request Headers

<pre>{headers}</pre>

---

#### Basic Information

- **Site:** {site}
- **User:** {user}""".format(
		site=ragapp.local.site,
		traceback=traceback,
		args="\n".join(pretty_args),
		user=ragapp.session.user,
		headers=ragapp.request.headers if ragapp.request else "[no request]",
	)

	ragapp.sendmail(
		recipients=ragapp.conf.setup_wizard_exception_email,
		sender=ragapp.session.user,
		subject=f"Setup failed: {ragapp.local.site}",
		message=message,
		delayed=False,
	)


def log_setup_wizard_exception(traceback, args):  # nosemgrep
	with open("../logs/setup-wizard.log", "w+") as setup_log:
		setup_log.write(traceback)
		setup_log.write(json.dumps(args))


def get_language_code(lang):
	return ragapp.db.get_value("Language", {"language_name": lang})


def enable_twofactor_all_roles():
	all_role = ragapp.get_doc("Role", {"role_name": "All"})
	all_role.two_factor_auth = True
	all_role.save(ignore_permissions=True)


def make_records(records, debug=False):
	from ragapp import _dict
	from ragapp.modules import scrub

	if debug:
		print("make_records: in DEBUG mode")

	# LOG every success and failure
	for record in records:
		doctype = record.get("doctype")
		condition = record.get("__condition")

		if condition and not condition():
			continue

		doc = ragapp.new_doc(doctype)
		doc.update(record)

		# ignore mandatory for root
		parent_link_field = "parent_" + scrub(doc.doctype)
		if doc.meta.get_field(parent_link_field) and not doc.get(parent_link_field):
			doc.flags.ignore_mandatory = True

		savepoint = "setup_fixtures_creation"
		try:
			ragapp.db.savepoint(savepoint)
			doc.insert(ignore_permissions=True, ignore_if_duplicate=True)
		except Exception as e:
			ragapp.clear_last_message()
			ragapp.db.rollback(save_point=savepoint)
			exception = record.get("__exception")
			if exception:
				config = _dict(exception)
				if isinstance(e, config.exception):
					config.handler()
				else:
					show_document_insert_error()
			else:
				show_document_insert_error()


def show_document_insert_error():
	print("Document Insert Error")
	print(ragapp.get_traceback())
	ragapp.log_error("Exception during Setup")
