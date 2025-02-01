ragapp.user_info = function (uid) {
	if (!uid) uid = ragapp.session.user;

	let user_info;
	if (!(ragapp.boot.user_info && ragapp.boot.user_info[uid])) {
		user_info = { fullname: uid || "Unknown" };
	} else {
		user_info = ragapp.boot.user_info[uid];
	}

	user_info.abbr = ragapp.get_abbr(user_info.fullname);
	user_info.color = ragapp.get_palette(user_info.fullname);

	return user_info;
};

ragapp.update_user_info = function (user_info) {
	for (let user in user_info) {
		if (ragapp.boot.user_info[user]) {
			Object.assign(ragapp.boot.user_info[user], user_info[user]);
		} else {
			ragapp.boot.user_info[user] = user_info[user];
		}
	}
};

ragapp.provide("ragapp.user");

$.extend(ragapp.user, {
	name: "Guest",
	full_name: function (uid) {
		return uid === ragapp.session.user
			? __(
					"You",
					null,
					"Name of the current user. For example: You edited this 5 hours ago."
			  )
			: ragapp.user_info(uid).fullname;
	},
	image: function (uid) {
		return ragapp.user_info(uid).image;
	},
	abbr: function (uid) {
		return ragapp.user_info(uid).abbr;
	},
	has_role: function (rl) {
		if (typeof rl == "string") rl = [rl];
		for (var i in rl) {
			if ((ragapp.boot ? ragapp.boot.user.roles : ["Guest"]).indexOf(rl[i]) != -1)
				return true;
		}
	},
	get_desktop_items: function () {
		// hide based on permission
		var modules_list = $.map(ragapp.boot.allowed_modules, function (icon) {
			var m = icon.module_name;
			var type = ragapp.modules[m] && ragapp.modules[m].type;

			if (ragapp.boot.user.allow_modules.indexOf(m) === -1) return null;

			var ret = null;
			if (type === "module") {
				if (ragapp.boot.user.allow_modules.indexOf(m) != -1 || ragapp.modules[m].is_help)
					ret = m;
			} else if (type === "page") {
				if (ragapp.boot.allowed_pages.indexOf(ragapp.modules[m].link) != -1) ret = m;
			} else if (type === "list") {
				if (ragapp.model.can_read(ragapp.modules[m]._doctype)) ret = m;
			} else if (type === "view") {
				ret = m;
			} else if (type === "setup") {
				if (
					ragapp.user.has_role("System Manager") ||
					ragapp.user.has_role("Administrator")
				)
					ret = m;
			} else {
				ret = m;
			}

			return ret;
		});

		return modules_list;
	},

	is_report_manager: function () {
		return ragapp.user.has_role(["Administrator", "System Manager", "Report Manager"]);
	},

	get_formatted_email: function (email) {
		var fullname = ragapp.user.full_name(email);

		if (!fullname) {
			return email;
		} else {
			// to quote or to not
			var quote = "";

			// only if these special characters are found
			// why? To make the output same as that in python!
			if (fullname.search(/[\[\]\\()<>@,:;".]/) !== -1) {
				quote = '"';
			}

			return repl("%(quote)s%(fullname)s%(quote)s <%(email)s>", {
				fullname: fullname,
				email: email,
				quote: quote,
			});
		}
	},

	get_emails: () => {
		return Object.keys(ragapp.boot.user_info).map((key) => ragapp.boot.user_info[key].email);
	},

	/* Normally ragapp.user is an object
	 * having properties and methods.
	 * But in the following case
	 *
	 * if (ragapp.user === 'Administrator')
	 *
	 * ragapp.user will cast to a string
	 * returning ragapp.user.name
	 */
	toString: function () {
		return this.name;
	},
});

ragapp.session_alive = true;
$(document).bind("mousemove", function () {
	if (ragapp.session_alive === false) {
		$(document).trigger("session_alive");
	}
	ragapp.session_alive = true;
	if (ragapp.session_alive_timeout) clearTimeout(ragapp.session_alive_timeout);
	ragapp.session_alive_timeout = setTimeout("ragapp.session_alive=false;", 30000);
});
