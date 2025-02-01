// Copyright (c) 2022, Ragapp Technologies and contributors
// For license information, please see license.txt

ragapp.ui.form.on("Error Log", {
	refresh: function (frm) {
		frm.disable_save();

		if (frm.doc.reference_doctype && frm.doc.reference_name) {
			frm.add_custom_button(__("Show Related Errors"), function () {
				ragapp.set_route("List", "Error Log", {
					reference_doctype: frm.doc.reference_doctype,
					reference_name: frm.doc.reference_name,
				});
			});
			frm.add_custom_button(__("Open reference document"), function () {
				ragapp.set_route("Form", frm.doc.reference_doctype, frm.doc.reference_name);
			});
		}
	},
});
