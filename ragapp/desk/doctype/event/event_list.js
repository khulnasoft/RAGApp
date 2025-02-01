ragapp.listview_settings["Event"] = {
	add_fields: ["starts_on", "ends_on"],
	onload: function () {
		ragapp.route_options = {
			status: "Open",
		};
	},
};
