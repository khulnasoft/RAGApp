ragapp.listview_settings["Access Log"] = {
	onload: function (list_view) {
		ragapp.require("logtypes.bundle.js", () => {
			ragapp.utils.logtypes.show_log_retention_message(list_view.doctype);
		});
	},
};
