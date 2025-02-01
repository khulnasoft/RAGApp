// Copyright (c) 2017, Ragapp Technologies and contributors
// For license information, please see license.txt

ragapp.ui.form.on("Print Style", {
	refresh: function (frm) {
		frm.add_custom_button(__("Print Settings"), () => {
			ragapp.set_route("Form", "Print Settings");
		});
	},
});
