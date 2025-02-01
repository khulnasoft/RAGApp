ragapp.pages["user-profile"].on_page_load = function (wrapper) {
	ragapp.require("user_profile_controller.bundle.js", () => {
		let user_profile = new ragapp.ui.UserProfile(wrapper);
		user_profile.show();
	});
};
