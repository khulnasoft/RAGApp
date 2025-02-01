// Copyright (c) 2016, Ragapp Technologies and contributors
// For license information, please see license.txt

ragapp.ui.form.on("Deleted Document", {
	refresh: function (frm) {
		if (frm.doc.restored) {
			frm.add_custom_button(__("Open"), function () {
				ragapp.set_route("Form", frm.doc.deleted_doctype, frm.doc.new_name);
			});
		} else {
			frm.add_custom_button(__("Restore"), function () {
				ragapp.call({
					method: "ragapp.core.doctype.deleted_document.deleted_document.restore",
					args: { name: frm.doc.name },
					callback: function (r) {
						frm.reload_doc();
					},
				});
			});
		}
	},
});
