# Copyright (c) 2018, Ragapp Technologies Pvt. Ltd. and Contributors
# License: MIT. See LICENSE

import ragapp

common_default_keys = ["__default", "__global"]

doctypes_for_mapping = {
	"Energy Point Rule",
	"Assignment Rule",
	"Milestone Tracker",
	"Document Naming Rule",
}


def get_doctype_map_key(doctype):
	return ragapp.scrub(doctype) + "_map"


doctype_map_keys = tuple(map(get_doctype_map_key, doctypes_for_mapping))

cli_cache_keys = ("assets_json",)

global_cache_keys = (
	"app_hooks",
	"installed_apps",
	"all_apps",
	"app_modules",
	"installed_app_modules",
	"module_app",
	"module_installed_app",
	"system_settings",
	"scheduler_events",
	"time_zone",
	"webhooks",
	"active_domains",
	"active_modules",
	"assignment_rule",
	"server_script_map",
	"wkhtmltopdf_version",
	"domain_restricted_doctypes",
	"domain_restricted_pages",
	"information_schema:counts",
	"db_tables",
	"server_script_autocompletion_items",
	*doctype_map_keys,
)

user_cache_keys = (
	"bootinfo",
	"user_recent",
	"roles",
	"user_doc",
	"lang",
	"defaults",
	"user_permissions",
	"home_page",
	"linked_with",
	"desktop_icons",
	"portal_menu_items",
	"user_perm_can_read",
	"has_role:Page",
	"has_role:Report",
	"desk_sidebar_items",
	"contacts",
)

doctype_cache_keys = (
	"doctype_form_meta",
	"last_modified",
	"linked_doctypes",
	"notifications",
	"workflow",
	"data_import_column_header_map",
)

wildcard_keys = (
	"document_cache::*",
	"table_columns::*",
)


def clear_user_cache(user=None):
	from ragapp.desk.notifications import clear_notifications

	# this will automatically reload the global cache
	# so it is important to clear this first
	clear_notifications(user)

	if user:
		ragapp.cache.hdel_names(user_cache_keys, user)
		ragapp.cache.delete_keys("user:" + user)
		clear_defaults_cache(user)
	else:
		ragapp.cache.delete_key(user_cache_keys)
		clear_defaults_cache()
		clear_global_cache()


def clear_domain_cache(user=None):
	domain_cache_keys = ("domain_restricted_doctypes", "domain_restricted_pages")
	ragapp.cache.delete_value(domain_cache_keys)


def clear_global_cache():
	from ragapp.website.utils import clear_website_cache

	clear_doctype_cache()
	clear_website_cache()
	ragapp.cache.delete_value(global_cache_keys + cli_cache_keys)
	ragapp.setup_module_map()


def clear_defaults_cache(user=None):
	if user:
		for key in [user, *common_default_keys]:
			ragapp.client_cache.delete_value(f"defaults::{key}")
	elif ragapp.flags.in_install != "ragapp":
		ragapp.client_cache.delete_keys("defaults::*")


def clear_doctype_cache(doctype=None):
	clear_controller_cache(doctype)

	_clear_doctype_cache_from_redis(doctype)
	if hasattr(ragapp.db, "after_commit"):
		ragapp.db.after_commit.add(lambda: _clear_doctype_cache_from_redis(doctype))
		ragapp.db.after_rollback.add(lambda: _clear_doctype_cache_from_redis(doctype))


def _clear_doctype_cache_from_redis(doctype: str | None = None):
	from ragapp.desk.notifications import delete_notification_count_for
	from ragapp.model.meta import clear_meta_cache

	to_del = ["is_table", "doctype_modules"]

	if doctype:

		def clear_single(dt):
			ragapp.clear_document_cache(dt)
			ragapp.cache.hdel_names(doctype_cache_keys, dt)
			clear_meta_cache(dt)

		clear_single(doctype)

		# clear all parent doctypes
		for dt in ragapp.get_all(
			"DocField", "parent", dict(fieldtype=["in", ragapp.model.table_fields], options=doctype)
		):
			clear_single(dt.parent)

		# clear all parent doctypes
		if not ragapp.flags.in_install:
			for dt in ragapp.get_all(
				"Custom Field", "dt", dict(fieldtype=["in", ragapp.model.table_fields], options=doctype)
			):
				clear_single(dt.dt)

		# clear all notifications
		delete_notification_count_for(doctype)

	else:
		# clear all
		to_del += doctype_cache_keys
		for pattern in wildcard_keys:
			to_del += ragapp.cache.get_keys(pattern)
		clear_meta_cache()

	ragapp.cache.delete_value(to_del)


def clear_controller_cache(doctype=None):
	if not doctype:
		ragapp.controllers.pop(ragapp.local.site, None)
		return

	if site_controllers := ragapp.controllers.get(ragapp.local.site):
		site_controllers.pop(doctype, None)


def get_doctype_map(doctype, name, filters=None, order_by=None):
	return ragapp.cache.hget(
		get_doctype_map_key(doctype),
		name,
		lambda: ragapp.get_all(doctype, filters=filters, order_by=order_by, ignore_ddl=True),
	)


def clear_doctype_map(doctype, name):
	ragapp.cache.hdel(ragapp.scrub(doctype) + "_map", name)


def build_table_count_cache():
	if (
		ragapp.flags.in_patch
		or ragapp.flags.in_install
		or ragapp.flags.in_migrate
		or ragapp.flags.in_import
		or ragapp.flags.in_setup_wizard
	):
		return

	table_name = ragapp.qb.Field("table_name").as_("name")
	table_rows = ragapp.qb.Field("table_rows").as_("count")
	information_schema = ragapp.qb.Schema("information_schema")

	data = (ragapp.qb.from_(information_schema.tables).select(table_name, table_rows)).run(as_dict=True)
	counts = {d.get("name").replace("tab", "", 1): d.get("count", None) for d in data}
	ragapp.cache.set_value("information_schema:counts", counts)

	return counts


def build_domain_restricted_doctype_cache(*args, **kwargs):
	if (
		ragapp.flags.in_patch
		or ragapp.flags.in_install
		or ragapp.flags.in_migrate
		or ragapp.flags.in_import
		or ragapp.flags.in_setup_wizard
	):
		return
	active_domains = ragapp.get_active_domains()
	doctypes = ragapp.get_all("DocType", filters={"restrict_to_domain": ("IN", active_domains)})
	doctypes = [doc.name for doc in doctypes]
	ragapp.cache.set_value("domain_restricted_doctypes", doctypes)

	return doctypes


def build_domain_restricted_page_cache(*args, **kwargs):
	if (
		ragapp.flags.in_patch
		or ragapp.flags.in_install
		or ragapp.flags.in_migrate
		or ragapp.flags.in_import
		or ragapp.flags.in_setup_wizard
	):
		return
	active_domains = ragapp.get_active_domains()
	pages = ragapp.get_all("Page", filters={"restrict_to_domain": ("IN", active_domains)})
	pages = [page.name for page in pages]
	ragapp.cache.set_value("domain_restricted_pages", pages)

	return pages


def clear_cache(user: str | None = None, doctype: str | None = None):
	"""Clear **User**, **DocType** or global cache.

	:param user: If user is given, only user cache is cleared.
	:param doctype: If doctype is given, only DocType cache is cleared."""
	import ragapp.cache_manager
	import ragapp.utils.caching
	from ragapp.website.router import clear_routing_cache

	if doctype:
		ragapp.cache_manager.clear_doctype_cache(doctype)
		reset_metadata_version()
	elif user:
		ragapp.cache_manager.clear_user_cache(user)
	else:  # everything
		# Delete ALL keys associated with this site.
		keys_to_delete = set(ragapp.cache.get_keys(""))
		for key in ragapp.get_hooks("persistent_cache_keys"):
			keys_to_delete.difference_update(ragapp.cache.get_keys(key))
		ragapp.cache.delete_value(list(keys_to_delete), make_keys=False)

		reset_metadata_version()
		ragapp.local.cache = {}
		ragapp.local.new_doc_templates = {}

		for fn in ragapp.get_hooks("clear_cache"):
			ragapp.get_attr(fn)()

	if (not doctype and not user) or doctype == "DocType":
		ragapp.utils.caching._SITE_CACHE.clear()
		ragapp.client_cache.clear_cache()

	ragapp.local.role_permissions = {}
	if hasattr(ragapp.local, "request_cache"):
		ragapp.local.request_cache.clear()
	if hasattr(ragapp.local, "system_settings"):
		del ragapp.local.system_settings
	if hasattr(ragapp.local, "website_settings"):
		del ragapp.local.website_settings

	clear_routing_cache()


def reset_metadata_version():
	"""Reset `metadata_version` (Client (Javascript) build ID) hash."""
	v = ragapp.generate_hash()
	ragapp.client_cache.set_value("metadata_version", v)
	return v
