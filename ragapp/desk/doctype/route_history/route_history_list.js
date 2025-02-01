ragapp.listview_settings["Route History"] = {
	onload: function (listview) {
		ragapp.require("logtypes.bundle.js", () => {
			ragapp.utils.logtypes.show_log_retention_message(cur_list.doctype);
		});
	},
};
