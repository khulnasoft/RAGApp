# Copyright (c) 2025, KhulnaSoft, Ltd and Contributors
# License: MIT. See LICENSE
import getpass

import ragapp
from ragapp.geo.doctype.country.country import import_country_and_currency
from ragapp.utils import cint
from ragapp.utils.password import update_password


def before_install():
	ragapp.reload_doc("core", "doctype", "doctype_state")
	ragapp.reload_doc("core", "doctype", "docfield")
	ragapp.reload_doc("core", "doctype", "docperm")
	ragapp.reload_doc("core", "doctype", "doctype_action")
	ragapp.reload_doc("core", "doctype", "doctype_link")
	ragapp.reload_doc("desk", "doctype", "form_tour_step")
	ragapp.reload_doc("desk", "doctype", "form_tour")
	ragapp.reload_doc("core", "doctype", "doctype")
	ragapp.clear_cache()


def after_install():
	create_user_type()
	install_basic_docs()

	from ragapp.core.doctype.file.utils import make_home_folder
	from ragapp.core.doctype.language.language import sync_languages

	make_home_folder()
	import_country_and_currency()
	sync_languages()

	# save default print setting
	print_settings = ragapp.get_doc("Print Settings")
	print_settings.save()

	# all roles to admin
	ragapp.get_doc("User", "Administrator").add_roles(*ragapp.get_all("Role", pluck="name"))

	# update admin password
	update_password("Administrator", get_admin_password())

	if not ragapp.conf.skip_setup_wizard:
		# only set home_page if the value doesn't exist in the db
		if not ragapp.db.get_default("desktop:home_page"):
			ragapp.db.set_default("desktop:home_page", "setup-wizard")
			ragapp.db.set_single_value("System Settings", "setup_complete", 0)

	# clear test log
	from ragapp.tests.utils.generators import _after_install_clear_test_log

	_after_install_clear_test_log()

	add_standard_navbar_items()

	ragapp.db.commit()


def create_user_type():
	for user_type in ["System User", "Website User"]:
		if not ragapp.db.exists("User Type", user_type):
			ragapp.get_doc({"doctype": "User Type", "name": user_type, "is_standard": 1}).insert(
				ignore_permissions=True
			)


def install_basic_docs():
	# core users / roles
	install_docs = [
		{
			"doctype": "User",
			"name": "Administrator",
			"first_name": "Administrator",
			"email": "admin@example.com",
			"enabled": 1,
			"is_admin": 1,
			"roles": [{"role": "Administrator"}],
			"thread_notify": 0,
			"send_me_a_copy": 0,
		},
		{
			"doctype": "User",
			"name": "Guest",
			"first_name": "Guest",
			"email": "guest@example.com",
			"enabled": 1,
			"is_guest": 1,
			"roles": [{"role": "Guest"}],
			"thread_notify": 0,
			"send_me_a_copy": 0,
		},
		{"doctype": "Role", "role_name": "Report Manager"},
		{"doctype": "Role", "role_name": "Translator"},
		{
			"doctype": "Workflow State",
			"workflow_state_name": "Pending",
			"icon": "question-sign",
			"style": "",
		},
		{
			"doctype": "Workflow State",
			"workflow_state_name": "Approved",
			"icon": "ok-sign",
			"style": "Success",
		},
		{
			"doctype": "Workflow State",
			"workflow_state_name": "Rejected",
			"icon": "remove",
			"style": "Danger",
		},
		{"doctype": "Workflow Action Master", "workflow_action_name": "Approve"},
		{"doctype": "Workflow Action Master", "workflow_action_name": "Reject"},
		{"doctype": "Workflow Action Master", "workflow_action_name": "Review"},
		{
			"doctype": "Email Domain",
			"domain_name": "example.com",
			"email_id": "account@example.com",
			"password": "pass",
			"email_server": "imap.example.com",
			"use_imap": 1,
			"smtp_server": "smtp.example.com",
		},
		{
			"doctype": "Email Account",
			"domain": "example.com",
			"email_id": "notifications@example.com",
			"default_outgoing": 1,
		},
		{
			"doctype": "Email Account",
			"domain": "example.com",
			"email_id": "replies@example.com",
			"default_incoming": 1,
		},
	]

	for d in install_docs:
		try:
			ragapp.get_doc(d).insert(ignore_if_duplicate=True)
		except ragapp.NameError:
			pass


def get_admin_password():
	return ragapp.conf.get("admin_password") or getpass.getpass("Set Administrator password: ")


def before_tests():
	if len(ragapp.get_installed_apps()) > 1:
		# don't run before tests if any other app is installed
		return

	ragapp.db.truncate("Custom Field")
	ragapp.db.truncate("Event")

	ragapp.clear_cache()

	# complete setup if missing
	if not cint(ragapp.db.get_single_value("System Settings", "setup_complete")):
		complete_setup_wizard()

	ragapp.db.set_single_value("Website Settings", "disable_signup", 0)
	ragapp.db.commit()
	ragapp.clear_cache()


def complete_setup_wizard():
	from ragapp.desk.page.setup_wizard.setup_wizard import setup_complete

	setup_complete(
		{
			"language": "English",
			"email": "test@erpnext.com",
			"full_name": "Test User",
			"password": "test",
			"country": "United States",
			"timezone": "America/New_York",
			"currency": "USD",
			"enable_telemtry": 1,
		}
	)


def add_standard_navbar_items():
	navbar_settings = ragapp.get_single("Navbar Settings")

	# don't add settings/help options if they're already present
	if navbar_settings.settings_dropdown and navbar_settings.help_dropdown:
		return

	navbar_settings.settings_dropdown = []
	navbar_settings.help_dropdown = []

	for item in ragapp.get_hooks("standard_navbar_items"):
		navbar_settings.append("settings_dropdown", item)

	for item in ragapp.get_hooks("standard_help_items"):
		navbar_settings.append("help_dropdown", item)

	navbar_settings.save()
