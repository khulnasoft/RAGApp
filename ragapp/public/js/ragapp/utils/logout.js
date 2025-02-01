ragapp.logout = function () {
	ragapp.call({
		method: "logout",
		callback: function (r) {
			if (r.exc) {
				return;
			}
			window.location.href = "/login";
		},
	});
};
