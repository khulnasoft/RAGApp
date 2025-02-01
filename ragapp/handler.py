# Copyright (c) 2022, Ragapp Technologies Pvt. Ltd. and Contributors
# License: MIT. See LICENSE

import os
from mimetypes import guess_type
from typing import TYPE_CHECKING

from werkzeug.wrappers import Response

import ragapp
import ragapp.sessions
import ragapp.utils
from ragapp import _, is_whitelisted, ping
from ragapp.core.doctype.server_script.server_script_utils import get_server_script_map
from ragapp.monitor import add_data_to_monitor
from ragapp.utils import cint
from ragapp.utils.csvutils import build_csv_response
from ragapp.utils.deprecations import deprecated
from ragapp.utils.image import optimize_image
from ragapp.utils.response import build_response

if TYPE_CHECKING:
	from ragapp.core.doctype.file.file import File
	from ragapp.core.doctype.user.user import User

ALLOWED_MIMETYPES = (
	"image/png",
	"image/jpeg",
	"application/pdf",
	"application/msword",
	"application/vnd.openxmlformats-officedocument.wordprocessingml.document",
	"application/vnd.ms-excel",
	"application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
	"application/vnd.oasis.opendocument.text",
	"application/vnd.oasis.opendocument.spreadsheet",
	"text/plain",
	"video/quicktime",
	"video/mp4",
	"text/csv",
)


def handle():
	"""handle request"""

	cmd = ragapp.local.form_dict.cmd
	data = None

	if cmd != "login":
		data = execute_cmd(cmd)

	# data can be an empty string or list which are valid responses
	if data is not None:
		if isinstance(data, Response):
			# method returns a response object, pass it on
			return data

		# add the response to `message` label
		ragapp.response["message"] = data


def execute_cmd(cmd, from_async=False):
	"""execute a request as python module"""
	for hook in reversed(ragapp.get_hooks("override_whitelisted_methods", {}).get(cmd, [])):
		# override using the last hook
		cmd = hook
		break

	# via server script
	server_script = get_server_script_map().get("_api", {}).get(cmd)
	if server_script:
		return run_server_script(server_script)

	try:
		method = get_attr(cmd)
	except Exception as e:
		ragapp.throw(_("Failed to get method for command {0} with {1}").format(cmd, e))

	if from_async:
		method = method.queue

	if method != run_doc_method:
		is_whitelisted(method)
		is_valid_http_method(method)

	return ragapp.call(method, **ragapp.form_dict)


def run_server_script(server_script):
	response = ragapp.get_doc("Server Script", server_script).execute_method()

	# some server scripts return output using flags (empty dict by default),
	# while others directly modify ragapp.response
	# return flags if not empty dict (this overwrites ragapp.response.message)
	if response != {}:
		return response


def is_valid_http_method(method):
	if ragapp.flags.in_safe_exec:
		return

	http_method = ragapp.local.request.method

	if http_method not in ragapp.allowed_http_methods_for_whitelisted_func[method]:
		ragapp.throw_permission_error()


@ragapp.whitelist(allow_guest=True)
def logout():
	ragapp.local.login_manager.logout()
	ragapp.db.commit()


@ragapp.whitelist(allow_guest=True)
def web_logout():
	ragapp.local.login_manager.logout()
	ragapp.db.commit()
	ragapp.respond_as_web_page(
		_("Logged Out"), _("You have been successfully logged out"), indicator_color="green"
	)


@ragapp.whitelist(allow_guest=True)
def upload_file():
	user = None
	if ragapp.session.user == "Guest":
		if ragapp.get_system_settings("allow_guests_to_upload_files"):
			ignore_permissions = True
		else:
			raise ragapp.PermissionError
	else:
		user: User = ragapp.get_doc("User", ragapp.session.user)
		ignore_permissions = False

	files = ragapp.request.files
	is_private = ragapp.form_dict.is_private
	doctype = ragapp.form_dict.doctype
	docname = ragapp.form_dict.docname
	fieldname = ragapp.form_dict.fieldname
	file_url = ragapp.form_dict.file_url
	folder = ragapp.form_dict.folder or "Home"
	method = ragapp.form_dict.method
	filename = ragapp.form_dict.file_name
	optimize = ragapp.form_dict.optimize
	content = None

	if library_file := ragapp.form_dict.get("library_file_name"):
		ragapp.has_permission("File", doc=library_file, throw=True)
		doc = ragapp.get_value(
			"File",
			ragapp.form_dict.library_file_name,
			["is_private", "file_url", "file_name"],
			as_dict=True,
		)
		is_private = doc.is_private
		file_url = doc.file_url
		filename = doc.file_name

	if not ignore_permissions:
		check_write_permission(doctype, docname)

	if "file" in files:
		file = files["file"]
		content = file.stream.read()
		filename = file.filename

		content_type = guess_type(filename)[0]
		if optimize and content_type and content_type.startswith("image/"):
			args = {"content": content, "content_type": content_type}
			if ragapp.form_dict.max_width:
				args["max_width"] = int(ragapp.form_dict.max_width)
			if ragapp.form_dict.max_height:
				args["max_height"] = int(ragapp.form_dict.max_height)
			content = optimize_image(**args)

	ragapp.local.uploaded_file_url = file_url
	ragapp.local.uploaded_file = content
	ragapp.local.uploaded_filename = filename

	if content is not None and (ragapp.session.user == "Guest" or (user and not user.has_desk_access())):
		filetype = guess_type(filename)[0]
		if filetype not in ALLOWED_MIMETYPES:
			ragapp.throw(_("You can only upload JPG, PNG, PDF, TXT, CSV or Microsoft documents."))

	if method:
		method = ragapp.get_attr(method)
		is_whitelisted(method)
		return method()
	else:
		return ragapp.get_doc(
			{
				"doctype": "File",
				"attached_to_doctype": doctype,
				"attached_to_name": docname,
				"attached_to_field": fieldname,
				"folder": folder,
				"file_name": filename,
				"file_url": file_url,
				"is_private": cint(is_private),
				"content": content,
			}
		).save(ignore_permissions=ignore_permissions)


def check_write_permission(doctype: str | None = None, name: str | None = None):
	check_doctype = doctype and not name
	if doctype and name:
		try:
			doc = ragapp.get_doc(doctype, name)
			doc.check_permission("write")
		except ragapp.DoesNotExistError:
			# doc has not been inserted yet, name is set to "new-some-doctype"
			# If doc inserts fine then only this attachment will be linked see file/utils.py:relink_mismatched_files
			return

	if check_doctype:
		ragapp.has_permission(doctype, "write", throw=True)


@ragapp.whitelist(allow_guest=True)
def download_file(file_url: str):
	"""
	Download file using token and REST API. Valid session or
	token is required to download private files.

	Method : GET
	Endpoints : download_file, ragapp.core.doctype.file.file.download_file
	URL Params : file_name = /path/to/file relative to site path
	"""
	file: File = ragapp.get_doc("File", {"file_url": file_url})
	if not file.is_downloadable():
		raise ragapp.PermissionError

	ragapp.local.response.filename = os.path.basename(file_url)
	ragapp.local.response.filecontent = file.get_content()
	ragapp.local.response.type = "download"


def get_attr(cmd):
	"""get method object from cmd"""
	if "." in cmd:
		method = ragapp.get_attr(cmd)
	else:
		from ragapp.deprecation_dumpster import deprecation_warning

		deprecation_warning(
			"unknown",
			"v17",
			f"Calling shorthand for {cmd} is deprecated, please specify full path in RPC call.",
		)
		method = globals()[cmd]
	return method


def run_doc_method(method, docs=None, dt=None, dn=None, arg=None, args=None):
	"""run a whitelisted controller method"""
	from inspect import signature

	if not args and arg:
		args = arg

	if dt:  # not called from a doctype (from a page)
		if not dn:
			dn = dt  # single
		doc = ragapp.get_doc(dt, dn)

	else:
		docs = ragapp.parse_json(docs)
		doc = ragapp.get_doc(docs)
		doc._original_modified = doc.modified
		doc.check_if_latest()

	if not doc:
		ragapp.throw_permission_error()

	doc.check_permission("read")

	try:
		args = ragapp.parse_json(args)
	except ValueError:
		pass

	method_obj = getattr(doc, method)
	fn = getattr(method_obj, "__func__", method_obj)
	is_whitelisted(fn)
	is_valid_http_method(fn)

	fnargs = list(signature(method_obj).parameters)

	if not fnargs or (len(fnargs) == 1 and fnargs[0] == "self"):
		response = doc.run_method(method)

	elif "args" in fnargs or not isinstance(args, dict):
		response = doc.run_method(method, args)

	else:
		response = doc.run_method(method, **args)

	ragapp.response.docs.append(doc)
	if response is None:
		return

	# build output as csv
	if cint(ragapp.form_dict.get("as_csv")):
		build_csv_response(response, _(doc.doctype).replace(" ", ""))
		return

	ragapp.response["message"] = response

	add_data_to_monitor(methodname=method)


runserverobj = deprecated(run_doc_method)
