import os

from . import __version__ as app_version

app_name = "ragapp"
app_title = "Framework"
app_publisher = "Ragapp Technologies"
app_description = "Full stack web framework with Python, Javascript, MariaDB, Redis, Node"
app_license = "MIT"
app_logo_url = "/assets/ragapp/images/ragapp-framework-logo.svg"
develop_version = "15.x.x-develop"
app_home = "/app/build"

app_email = "info@khulnasoft.com"

before_install = "ragapp.utils.install.before_install"
after_install = "ragapp.utils.install.after_install"

page_js = {"setup-wizard": "public/js/ragapp/setup_wizard.js"}

# website
app_include_js = [
	"libs.bundle.js",
	"desk.bundle.js",
	"list.bundle.js",
	"form.bundle.js",
	"controls.bundle.js",
	"report.bundle.js",
	"telemetry.bundle.js",
	"billing.bundle.js",
]

app_include_css = [
	"desk.bundle.css",
	"report.bundle.css",
]
app_include_icons = [
	"/assets/ragapp/icons/timeless/icons.svg",
	"/assets/ragapp/icons/espresso/icons.svg",
]

doctype_js = {
	"Web Page": "public/js/ragapp/utils/web_template.js",
	"Website Settings": "public/js/ragapp/utils/web_template.js",
}

web_include_js = ["website_script.js"]
web_include_css = []
web_include_icons = [
	"/assets/ragapp/icons/timeless/icons.svg",
	"/assets/ragapp/icons/espresso/icons.svg",
]

email_css = ["email.bundle.css"]

website_route_rules = [
	{"from_route": "/blog/<category>", "to_route": "Blog Post"},
	{"from_route": "/kb/<category>", "to_route": "Help Article"},
	{"from_route": "/newsletters", "to_route": "Newsletter"},
	{"from_route": "/profile", "to_route": "me"},
	{"from_route": "/app/<path:app_path>", "to_route": "app"},
]

website_redirects = [
	{"source": r"/desk(.*)", "target": r"/app\1"},
	{
		"source": "/.well-known/openid-configuration",
		"target": "/api/method/ragapp.integrations.oauth2.openid_configuration",
	},
]

base_template = "templates/base.html"

write_file_keys = ["file_url", "file_name"]

notification_config = "ragapp.core.notifications.get_notification_config"

before_tests = "ragapp.utils.install.before_tests"

email_append_to = ["Event", "ToDo", "Communication"]

calendars = ["Event"]

leaderboards = "ragapp.desk.leaderboard.get_leaderboards"

# login

on_session_creation = [
	"ragapp.core.doctype.activity_log.feed.login_feed",
	"ragapp.core.doctype.user.user.notify_admin_access_to_system_manager",
]

on_logout = "ragapp.core.doctype.session_default_settings.session_default_settings.clear_session_defaults"

# PDF
pdf_header_html = "ragapp.utils.pdf.pdf_header_html"
pdf_body_html = "ragapp.utils.pdf.pdf_body_html"
pdf_footer_html = "ragapp.utils.pdf.pdf_footer_html"

# permissions

permission_query_conditions = {
	"Event": "ragapp.desk.doctype.event.event.get_permission_query_conditions",
	"ToDo": "ragapp.desk.doctype.todo.todo.get_permission_query_conditions",
	"User": "ragapp.core.doctype.user.user.get_permission_query_conditions",
	"Dashboard Settings": "ragapp.desk.doctype.dashboard_settings.dashboard_settings.get_permission_query_conditions",
	"Notification Log": "ragapp.desk.doctype.notification_log.notification_log.get_permission_query_conditions",
	"Dashboard": "ragapp.desk.doctype.dashboard.dashboard.get_permission_query_conditions",
	"Dashboard Chart": "ragapp.desk.doctype.dashboard_chart.dashboard_chart.get_permission_query_conditions",
	"Number Card": "ragapp.desk.doctype.number_card.number_card.get_permission_query_conditions",
	"Notification Settings": "ragapp.desk.doctype.notification_settings.notification_settings.get_permission_query_conditions",
	"Note": "ragapp.desk.doctype.note.note.get_permission_query_conditions",
	"Kanban Board": "ragapp.desk.doctype.kanban_board.kanban_board.get_permission_query_conditions",
	"Contact": "ragapp.contacts.address_and_contact.get_permission_query_conditions_for_contact",
	"Address": "ragapp.contacts.address_and_contact.get_permission_query_conditions_for_address",
	"Communication": "ragapp.core.doctype.communication.communication.get_permission_query_conditions_for_communication",
	"Workflow Action": "ragapp.workflow.doctype.workflow_action.workflow_action.get_permission_query_conditions",
	"Prepared Report": "ragapp.core.doctype.prepared_report.prepared_report.get_permission_query_condition",
	"File": "ragapp.core.doctype.file.file.get_permission_query_conditions",
}

has_permission = {
	"Event": "ragapp.desk.doctype.event.event.has_permission",
	"ToDo": "ragapp.desk.doctype.todo.todo.has_permission",
	"Note": "ragapp.desk.doctype.note.note.has_permission",
	"User": "ragapp.core.doctype.user.user.has_permission",
	"Dashboard Chart": "ragapp.desk.doctype.dashboard_chart.dashboard_chart.has_permission",
	"Number Card": "ragapp.desk.doctype.number_card.number_card.has_permission",
	"Kanban Board": "ragapp.desk.doctype.kanban_board.kanban_board.has_permission",
	"Contact": "ragapp.contacts.address_and_contact.has_permission",
	"Address": "ragapp.contacts.address_and_contact.has_permission",
	"Communication": "ragapp.core.doctype.communication.communication.has_permission",
	"Workflow Action": "ragapp.workflow.doctype.workflow_action.workflow_action.has_permission",
	"File": "ragapp.core.doctype.file.file.has_permission",
	"Prepared Report": "ragapp.core.doctype.prepared_report.prepared_report.has_permission",
	"Notification Settings": "ragapp.desk.doctype.notification_settings.notification_settings.has_permission",
}

has_website_permission = {"Address": "ragapp.contacts.doctype.address.address.has_website_permission"}

jinja = {
	"methods": "ragapp.utils.jinja_globals",
	"filters": [
		"ragapp.utils.data.global_date_format",
		"ragapp.utils.markdown",
		"ragapp.website.utils.abs_url",
	],
}

standard_queries = {"User": "ragapp.core.doctype.user.user.user_query"}

doc_events = {
	"*": {
		"on_update": [
			"ragapp.desk.notifications.clear_doctype_notifications",
			"ragapp.workflow.doctype.workflow_action.workflow_action.process_workflow_actions",
			"ragapp.core.doctype.file.utils.attach_files_to_document",
			"ragapp.automation.doctype.assignment_rule.assignment_rule.apply",
			"ragapp.automation.doctype.assignment_rule.assignment_rule.update_due_date",
			"ragapp.core.doctype.user_type.user_type.apply_permissions_for_non_standard_user_type",
			"ragapp.core.doctype.permission_log.permission_log.make_perm_log",
		],
		"after_rename": "ragapp.desk.notifications.clear_doctype_notifications",
		"on_cancel": [
			"ragapp.desk.notifications.clear_doctype_notifications",
			"ragapp.workflow.doctype.workflow_action.workflow_action.process_workflow_actions",
			"ragapp.automation.doctype.assignment_rule.assignment_rule.apply",
		],
		"on_trash": [
			"ragapp.desk.notifications.clear_doctype_notifications",
			"ragapp.workflow.doctype.workflow_action.workflow_action.process_workflow_actions",
		],
		"on_update_after_submit": [
			"ragapp.workflow.doctype.workflow_action.workflow_action.process_workflow_actions",
			"ragapp.automation.doctype.assignment_rule.assignment_rule.apply",
			"ragapp.automation.doctype.assignment_rule.assignment_rule.update_due_date",
			"ragapp.core.doctype.file.utils.attach_files_to_document",
		],
		"on_change": [
			"ragapp.social.doctype.energy_point_rule.energy_point_rule.process_energy_points",
			"ragapp.automation.doctype.milestone_tracker.milestone_tracker.evaluate_milestone",
		],
		"after_delete": ["ragapp.core.doctype.permission_log.permission_log.make_perm_log"],
	},
	"Event": {
		"after_insert": "ragapp.integrations.doctype.google_calendar.google_calendar.insert_event_in_google_calendar",
		"on_update": "ragapp.integrations.doctype.google_calendar.google_calendar.update_event_in_google_calendar",
		"on_trash": "ragapp.integrations.doctype.google_calendar.google_calendar.delete_event_from_google_calendar",
	},
	"Contact": {
		"after_insert": "ragapp.integrations.doctype.google_contacts.google_contacts.insert_contacts_to_google_contacts",
		"on_update": "ragapp.integrations.doctype.google_contacts.google_contacts.update_contacts_to_google_contacts",
	},
	"DocType": {
		"on_update": "ragapp.cache_manager.build_domain_restricted_doctype_cache",
	},
	"Page": {
		"on_update": "ragapp.cache_manager.build_domain_restricted_page_cache",
	},
}

scheduler_events = {
	"cron": {
		# 5 minutes
		"0/5 * * * *": [
			"ragapp.email.doctype.notification.notification.trigger_offset_alerts",
		],
		# 15 minutes
		"0/15 * * * *": [
			"ragapp.oauth.delete_oauth2_data",
			"ragapp.website.doctype.web_page.web_page.check_publish_status",
			"ragapp.twofactor.delete_all_barcodes_for_users",
			"ragapp.email.doctype.email_account.email_account.notify_unreplied",
			"ragapp.utils.global_search.sync_global_search",
			"ragapp.deferred_insert.save_to_db",
			"ragapp.automation.doctype.reminder.reminder.send_reminders",
		],
		# 10 minutes
		"0/10 * * * *": [
			"ragapp.email.doctype.email_account.email_account.pull",
		],
		# Hourly but offset by 30 minutes
		"30 * * * *": [
			"ragapp.core.doctype.prepared_report.prepared_report.expire_stalled_report",
		],
		# Daily but offset by 45 minutes
		"45 0 * * *": [
			"ragapp.core.doctype.log_settings.log_settings.run_log_clean_up",
		],
	},
	"all": [
		"ragapp.email.queue.flush",
		"ragapp.monitor.flush",
	],
	"hourly": [
		"ragapp.model.utils.link_count.update_link_count",
		"ragapp.model.utils.user_settings.sync_user_settings",
		"ragapp.desk.page.backups.backups.delete_downloadable_backups",
		"ragapp.desk.form.document_follow.send_hourly_updates",
		"ragapp.integrations.doctype.google_calendar.google_calendar.sync",
		"ragapp.email.doctype.newsletter.newsletter.send_scheduled_email",
		"ragapp.website.doctype.personal_data_deletion_request.personal_data_deletion_request.process_data_deletion_request",
	],
	"daily": [
		"ragapp.desk.notifications.clear_notifications",
		"ragapp.desk.doctype.event.event.send_event_digest",
		"ragapp.sessions.clear_expired_sessions",
		"ragapp.email.doctype.notification.notification.trigger_daily_alerts",
		"ragapp.website.doctype.personal_data_deletion_request.personal_data_deletion_request.remove_unverified_record",
		"ragapp.desk.form.document_follow.send_daily_updates",
		"ragapp.social.doctype.energy_point_settings.energy_point_settings.allocate_review_points",
		"ragapp.integrations.doctype.google_contacts.google_contacts.sync",
		"ragapp.automation.doctype.auto_repeat.auto_repeat.make_auto_repeat_entry",
		"ragapp.automation.doctype.auto_repeat.auto_repeat.set_auto_repeat_as_completed",
	],
	"daily_long": [
		"ragapp.integrations.doctype.dropbox_settings.dropbox_settings.take_backups_daily",
		"ragapp.integrations.doctype.s3_backup_settings.s3_backup_settings.take_backups_daily",
		"ragapp.email.doctype.auto_email_report.auto_email_report.send_daily",
		"ragapp.integrations.doctype.google_drive.google_drive.daily_backup",
	],
	"weekly_long": [
		"ragapp.integrations.doctype.dropbox_settings.dropbox_settings.take_backups_weekly",
		"ragapp.integrations.doctype.s3_backup_settings.s3_backup_settings.take_backups_weekly",
		"ragapp.desk.form.document_follow.send_weekly_updates",
		"ragapp.utils.change_log.check_for_update",
		"ragapp.social.doctype.energy_point_log.energy_point_log.send_weekly_summary",
		"ragapp.integrations.doctype.google_drive.google_drive.weekly_backup",
		"ragapp.desk.doctype.changelog_feed.changelog_feed.fetch_changelog_feed",
	],
	"monthly": [
		"ragapp.email.doctype.auto_email_report.auto_email_report.send_monthly",
		"ragapp.social.doctype.energy_point_log.energy_point_log.send_monthly_summary",
	],
	"monthly_long": [
		"ragapp.integrations.doctype.s3_backup_settings.s3_backup_settings.take_backups_monthly"
	],
}

sounds = [
	{"name": "email", "src": "/assets/ragapp/sounds/email.mp3", "volume": 0.1},
	{"name": "submit", "src": "/assets/ragapp/sounds/submit.mp3", "volume": 0.1},
	{"name": "cancel", "src": "/assets/ragapp/sounds/cancel.mp3", "volume": 0.1},
	{"name": "delete", "src": "/assets/ragapp/sounds/delete.mp3", "volume": 0.05},
	{"name": "click", "src": "/assets/ragapp/sounds/click.mp3", "volume": 0.05},
	{"name": "error", "src": "/assets/ragapp/sounds/error.mp3", "volume": 0.1},
	{"name": "alert", "src": "/assets/ragapp/sounds/alert.mp3", "volume": 0.2},
	# {"name": "chime", "src": "/assets/ragapp/sounds/chime.mp3"},
]

setup_wizard_exception = [
	"ragapp.desk.page.setup_wizard.setup_wizard.email_setup_wizard_exception",
	"ragapp.desk.page.setup_wizard.setup_wizard.log_setup_wizard_exception",
]

before_migrate = ["ragapp.core.doctype.patch_log.patch_log.before_migrate"]
after_migrate = ["ragapp.website.doctype.website_theme.website_theme.after_migrate"]

otp_methods = ["OTP App", "Email", "SMS"]

user_data_fields = [
	{"doctype": "Access Log", "strict": True},
	{"doctype": "Activity Log", "strict": True},
	{"doctype": "Comment", "strict": True},
	{
		"doctype": "Contact",
		"filter_by": "email_id",
		"redact_fields": ["first_name", "last_name", "phone", "mobile_no"],
		"rename": True,
	},
	{"doctype": "Contact Email", "filter_by": "email_id"},
	{
		"doctype": "Address",
		"filter_by": "email_id",
		"redact_fields": [
			"address_title",
			"address_line1",
			"address_line2",
			"city",
			"county",
			"state",
			"pincode",
			"phone",
			"fax",
		],
	},
	{
		"doctype": "Communication",
		"filter_by": "sender",
		"redact_fields": ["sender_full_name", "phone_no", "content"],
	},
	{"doctype": "Communication", "filter_by": "recipients"},
	{"doctype": "Email Group Member", "filter_by": "email"},
	{"doctype": "Email Unsubscribe", "filter_by": "email", "partial": True},
	{"doctype": "Email Queue", "filter_by": "sender"},
	{"doctype": "Email Queue Recipient", "filter_by": "recipient"},
	{
		"doctype": "File",
		"filter_by": "attached_to_name",
		"redact_fields": ["file_name", "file_url"],
	},
	{
		"doctype": "User",
		"filter_by": "name",
		"redact_fields": [
			"email",
			"username",
			"first_name",
			"middle_name",
			"last_name",
			"full_name",
			"birth_date",
			"user_image",
			"phone",
			"mobile_no",
			"location",
			"banner_image",
			"interest",
			"bio",
			"email_signature",
		],
	},
	{"doctype": "Version", "strict": True},
]

global_search_doctypes = {
	"Default": [
		{"doctype": "Contact"},
		{"doctype": "Address"},
		{"doctype": "ToDo"},
		{"doctype": "Note"},
		{"doctype": "Event"},
		{"doctype": "Blog Post"},
		{"doctype": "Dashboard"},
		{"doctype": "Country"},
		{"doctype": "Currency"},
		{"doctype": "Newsletter"},
		{"doctype": "Letter Head"},
		{"doctype": "Workflow"},
		{"doctype": "Web Page"},
		{"doctype": "Web Form"},
	]
}

override_whitelisted_methods = {
	# Legacy File APIs
	"ragapp.utils.file_manager.download_file": "download_file",
	"ragapp.core.doctype.file.file.download_file": "download_file",
	"ragapp.core.doctype.file.file.unzip_file": "ragapp.core.api.file.unzip_file",
	"ragapp.core.doctype.file.file.get_attached_images": "ragapp.core.api.file.get_attached_images",
	"ragapp.core.doctype.file.file.get_files_in_folder": "ragapp.core.api.file.get_files_in_folder",
	"ragapp.core.doctype.file.file.get_files_by_search_text": "ragapp.core.api.file.get_files_by_search_text",
	"ragapp.core.doctype.file.file.get_max_file_size": "ragapp.core.api.file.get_max_file_size",
	"ragapp.core.doctype.file.file.create_new_folder": "ragapp.core.api.file.create_new_folder",
	"ragapp.core.doctype.file.file.move_file": "ragapp.core.api.file.move_file",
	"ragapp.core.doctype.file.file.zip_files": "ragapp.core.api.file.zip_files",
	# Legacy (& Consistency) OAuth2 APIs
	"ragapp.www.login.login_via_google": "ragapp.integrations.oauth2_logins.login_via_google",
	"ragapp.www.login.login_via_github": "ragapp.integrations.oauth2_logins.login_via_github",
	"ragapp.www.login.login_via_facebook": "ragapp.integrations.oauth2_logins.login_via_facebook",
	"ragapp.www.login.login_via_ragapp": "ragapp.integrations.oauth2_logins.login_via_ragapp",
	"ragapp.www.login.login_via_office365": "ragapp.integrations.oauth2_logins.login_via_office365",
	"ragapp.www.login.login_via_salesforce": "ragapp.integrations.oauth2_logins.login_via_salesforce",
	"ragapp.www.login.login_via_fairlogin": "ragapp.integrations.oauth2_logins.login_via_fairlogin",
}

ignore_links_on_delete = [
	"Communication",
	"ToDo",
	"DocShare",
	"Email Unsubscribe",
	"Activity Log",
	"File",
	"Version",
	"Document Follow",
	"Comment",
	"View Log",
	"Tag Link",
	"Notification Log",
	"Email Queue",
	"Document Share Key",
	"Integration Request",
	"Unhandled Email",
	"Webhook Request Log",
	"Workspace",
	"Route History",
	"Access Log",
	"Permission Log",
]

# Request Hooks
before_request = [
	"ragapp.recorder.record",
	"ragapp.monitor.start",
	"ragapp.rate_limiter.apply",
]

after_request = [
	"ragapp.monitor.stop",
]

# Background Job Hooks
before_job = [
	"ragapp.recorder.record",
	"ragapp.monitor.start",
]

if os.getenv("RAGAPP_SENTRY_DSN") and (
	os.getenv("ENABLE_SENTRY_DB_MONITORING")
	or os.getenv("SENTRY_TRACING_SAMPLE_RATE")
	or os.getenv("SENTRY_PROFILING_SAMPLE_RATE")
):
	before_request.append("ragapp.utils.sentry.set_sentry_context")
	before_job.append("ragapp.utils.sentry.set_sentry_context")

after_job = [
	"ragapp.recorder.dump",
	"ragapp.monitor.stop",
	"ragapp.utils.file_lock.release_document_locks",
	"ragapp.utils.background_jobs.flush_telemetry",
]

extend_bootinfo = [
	"ragapp.utils.telemetry.add_bootinfo",
	"ragapp.core.doctype.user_permission.user_permission.send_user_permissions",
]

get_changelog_feed = "ragapp.desk.doctype.changelog_feed.changelog_feed.get_feed"

export_python_type_annotations = True

standard_navbar_items = [
	{
		"item_label": "User Settings",
		"item_type": "Action",
		"action": "ragapp.ui.toolbar.route_to_user()",
		"is_standard": 1,
	},
	{
		"item_label": "Workspace Settings",
		"item_type": "Action",
		"action": "ragapp.quick_edit('Workspace Settings')",
		"is_standard": 1,
	},
	{
		"item_label": "Session Defaults",
		"item_type": "Action",
		"action": "ragapp.ui.toolbar.setup_session_defaults()",
		"is_standard": 1,
	},
	{
		"item_label": "Reload",
		"item_type": "Action",
		"action": "ragapp.ui.toolbar.clear_cache()",
		"is_standard": 1,
	},
	{
		"item_label": "View Website",
		"item_type": "Action",
		"action": "ragapp.ui.toolbar.view_website()",
		"is_standard": 1,
	},
	{
		"item_label": "Apps",
		"item_type": "Route",
		"route": "/apps",
		"is_standard": 1,
	},
	{
		"item_label": "Toggle Full Width",
		"item_type": "Action",
		"action": "ragapp.ui.toolbar.toggle_full_width()",
		"is_standard": 1,
	},
	{
		"item_label": "Toggle Theme",
		"item_type": "Action",
		"action": "new ragapp.ui.ThemeSwitcher().show()",
		"is_standard": 1,
	},
	{
		"item_type": "Separator",
		"is_standard": 1,
		"item_label": "",
	},
	{
		"item_label": "Log out",
		"item_type": "Action",
		"action": "ragapp.app.logout()",
		"is_standard": 1,
	},
]

standard_help_items = [
	{
		"item_label": "About",
		"item_type": "Action",
		"action": "ragapp.ui.toolbar.show_about()",
		"is_standard": 1,
	},
	{
		"item_label": "Keyboard Shortcuts",
		"item_type": "Action",
		"action": "ragapp.ui.toolbar.show_shortcuts(event)",
		"is_standard": 1,
	},
	{
		"item_label": "System Health",
		"item_type": "Route",
		"route": "/app/system-health-report",
		"is_standard": 1,
	},
	{
		"item_label": "Ragapp Support",
		"item_type": "Route",
		"route": "https://ragapp.khulnasoft.com/support",
		"is_standard": 1,
	},
]

# log doctype cleanups to automatically add in log settings
default_log_clearing_doctypes = {
	"Error Log": 14,
	"Email Queue": 30,
	"Scheduled Job Log": 7,
	"Submission Queue": 7,
	"Prepared Report": 14,
	"Webhook Request Log": 30,
	"Unhandled Email": 30,
	"Reminder": 30,
	"Integration Request": 90,
	"Activity Log": 90,
	"Route History": 90,
}

# These keys will not be erased when doing ragapp.clear_cache()
persistent_cache_keys = [
	"changelog-*",  # version update notifications
	"insert_queue_for_*",  # Deferred Insert
	"recorder-*",  # Recorder
	"global_search_queue",
	"monitor-transactions",
	"rate-limit-counter-*",
	"rl:*",
]
