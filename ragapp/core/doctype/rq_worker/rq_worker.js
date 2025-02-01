// Copyright (c) 2022, Ragapp Technologies and contributors
// For license information, please see license.txt

ragapp.ui.form.on("RQ Worker", {
	refresh: function (frm) {
		// Nothing in this form is supposed to be editable.
		frm.disable_form();
	},
});
