// Copyright (c) 2020, Ragapp Technologies and contributors
// For license information, please see license.txt

ragapp.ui.form.on("Navbar Settings", {
	after_save: function (frm) {
		ragapp.ui.toolbar.clear_cache();
	},
});
