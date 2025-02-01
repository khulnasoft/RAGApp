// Copyright (c) 2025, KhulnaSoft, Ltd and Contributors
// MIT License. See license.txt
/* eslint-disable no-console */

// __('Modules') __('Domains') __('Places') __('Administration') # for translation, don't remove

ragapp.start_app = function () {
	if (!ragapp.Application) return;
	ragapp.assets.check();
	ragapp.provide("ragapp.app");
	ragapp.provide("ragapp.desk");
	ragapp.app = new ragapp.Application();
};

$(document).ready(function () {
	if (!ragapp.utils.supportsES6) {
		ragapp.msgprint({
			indicator: "red",
			title: __("Browser not supported"),
			message: __(
				"Some of the features might not work in your browser. Please update your browser to the latest version."
			),
		});
	}
	ragapp.start_app();
});

ragapp.Application = class Application {
	constructor() {
		this.startup();
	}

	startup() {
		ragapp.realtime.init();
		ragapp.model.init();

		this.load_bootinfo();
		this.load_user_permissions();
		this.make_nav_bar();
		this.make_sidebar();
		this.set_favicon();
		this.set_fullwidth_if_enabled();
		this.add_browser_class();
		this.setup_energy_point_listeners();
		this.setup_copy_doc_listener();
		this.setup_broadcast_listeners();

		ragapp.ui.keys.setup();

		this.setup_theme();

		// page container
		this.make_page_container();
		this.setup_tours();
		this.set_route();

		// trigger app startup
		$(document).trigger("startup");
		$(document).trigger("app_ready");

		this.show_notices();
		this.show_notes();

		if (ragapp.ui.startup_setup_dialog && !ragapp.boot.setup_complete) {
			ragapp.ui.startup_setup_dialog.pre_show();
			ragapp.ui.startup_setup_dialog.show();
		}

		// listen to build errors
		this.setup_build_events();

		if (ragapp.sys_defaults.email_user_password) {
			var email_list = ragapp.sys_defaults.email_user_password.split(",");
			for (var u in email_list) {
				if (email_list[u] === ragapp.user.name) {
					this.set_password(email_list[u]);
				}
			}
		}

		// REDESIGN-TODO: Fix preview popovers
		this.link_preview = new ragapp.ui.LinkPreview();

		ragapp.broadcast.emit("boot", {
			csrf_token: ragapp.csrf_token,
			user: ragapp.session.user,
		});
	}

	make_sidebar() {
		this.sidebar = new ragapp.ui.Sidebar({});
	}

	setup_theme() {
		ragapp.ui.keys.add_shortcut({
			shortcut: "shift+ctrl+g",
			description: __("Switch Theme"),
			action: () => {
				if (ragapp.theme_switcher && ragapp.theme_switcher.dialog.is_visible) {
					ragapp.theme_switcher.hide();
				} else {
					ragapp.theme_switcher = new ragapp.ui.ThemeSwitcher();
					ragapp.theme_switcher.show();
				}
			},
		});

		ragapp.ui.add_system_theme_switch_listener();
		const root = document.documentElement;

		const observer = new MutationObserver(() => {
			ragapp.ui.set_theme();
		});
		observer.observe(root, {
			attributes: true,
			attributeFilter: ["data-theme-mode"],
		});

		ragapp.ui.set_theme();
	}

	setup_tours() {
		if (
			!window.Cypress &&
			ragapp.boot.onboarding_tours &&
			ragapp.boot.user.onboarding_status != null
		) {
			let pending_tours = !ragapp.boot.onboarding_tours.every(
				(tour) => ragapp.boot.user.onboarding_status[tour[0]]?.is_complete
			);
			if (pending_tours && ragapp.boot.onboarding_tours.length > 0) {
				ragapp.require("onboarding_tours.bundle.js", () => {
					ragapp.utils.sleep(1000).then(() => {
						ragapp.ui.init_onboarding_tour();
					});
				});
			}
		}
	}

	show_notices() {
		if (ragapp.boot.messages) {
			ragapp.msgprint(ragapp.boot.messages);
		}

		if (ragapp.user_roles.includes("System Manager")) {
			// delayed following requests to make boot faster
			setTimeout(() => {
				this.show_change_log();
				this.show_update_available();
			}, 1000);
		}

		if (!ragapp.boot.developer_mode) {
			let console_security_message = __(
				"Using this console may allow attackers to impersonate you and steal your information. Do not enter or paste code that you do not understand."
			);
			console.log(`%c${console_security_message}`, "font-size: large");
		}

		ragapp.realtime.on("version-update", function () {
			var dialog = ragapp.msgprint({
				message: __(
					"The application has been updated to a new version, please refresh this page"
				),
				indicator: "green",
				title: __("Version Updated"),
			});
			dialog.set_primary_action(__("Refresh"), function () {
				location.reload(true);
			});
			dialog.get_close_btn().toggle(false);
		});
	}

	set_route() {
		if (ragapp.boot && localStorage.getItem("session_last_route")) {
			ragapp.set_route(localStorage.getItem("session_last_route"));
			localStorage.removeItem("session_last_route");
		} else {
			// route to home page
			ragapp.router.route();
		}
		ragapp.router.on("change", () => {
			$(".tooltip").hide();
		});
	}

	set_password(user) {
		var me = this;
		ragapp.call({
			method: "ragapp.core.doctype.user.user.get_email_awaiting",
			args: {
				user: user,
			},
			callback: function (email_account) {
				email_account = email_account["message"];
				if (email_account) {
					var i = 0;
					if (i < email_account.length) {
						me.email_password_prompt(email_account, user, i);
					}
				}
			},
		});
	}

	email_password_prompt(email_account, user, i) {
		var me = this;
		const email_id = email_account[i]["email_id"];
		let d = new ragapp.ui.Dialog({
			title: __("Password missing in Email Account"),
			fields: [
				{
					fieldname: "password",
					fieldtype: "Password",
					label: __(
						"Please enter the password for: <b>{0}</b>",
						[email_id],
						"Email Account"
					),
					reqd: 1,
				},
				{
					fieldname: "submit",
					fieldtype: "Button",
					label: __("Submit", null, "Submit password for Email Account"),
				},
			],
		});
		d.get_input("submit").on("click", function () {
			//setup spinner
			d.hide();
			var s = new ragapp.ui.Dialog({
				title: __("Checking one moment"),
				fields: [
					{
						fieldtype: "HTML",
						fieldname: "checking",
					},
				],
			});
			s.fields_dict.checking.$wrapper.html('<i class="fa fa-spinner fa-spin fa-4x"></i>');
			s.show();
			ragapp.call({
				method: "ragapp.email.doctype.email_account.email_account.set_email_password",
				args: {
					email_account: email_account[i]["email_account"],
					password: d.get_value("password"),
				},
				callback: function (passed) {
					s.hide();
					d.hide(); //hide waiting indication
					if (!passed["message"]) {
						ragapp.show_alert(
							{ message: __("Login Failed please try again"), indicator: "error" },
							5
						);
						me.email_password_prompt(email_account, user, i);
					} else {
						if (i + 1 < email_account.length) {
							i = i + 1;
							me.email_password_prompt(email_account, user, i);
						}
					}
				},
			});
		});
		d.show();
	}
	load_bootinfo() {
		if (ragapp.boot) {
			this.setup_workspaces();
			ragapp.model.sync(ragapp.boot.docs);
			this.check_metadata_cache_status();
			this.set_globals();
			this.sync_pages();
			ragapp.router.setup();
			this.setup_moment();
			if (ragapp.boot.print_css) {
				ragapp.dom.set_style(ragapp.boot.print_css, "print-style");
			}
			ragapp.user.name = ragapp.boot.user.name;
			ragapp.router.setup();
		} else {
			this.set_as_guest();
		}
	}

	setup_workspaces() {
		ragapp.modules = {};
		ragapp.workspaces = {};
		ragapp.boot.allowed_workspaces = ragapp.boot.sidebar_pages.pages;

		for (let page of ragapp.boot.allowed_workspaces || []) {
			ragapp.modules[page.module] = page;
			ragapp.workspaces[ragapp.router.slug(page.name)] = page;
		}
	}

	load_user_permissions() {
		ragapp.defaults.load_user_permission_from_boot();

		ragapp.realtime.on(
			"update_user_permissions",
			ragapp.utils.debounce(() => {
				ragapp.defaults.update_user_permissions();
			}, 500)
		);
	}

	check_metadata_cache_status() {
		if (ragapp.boot.metadata_version != localStorage.metadata_version) {
			ragapp.assets.clear_local_storage();
			ragapp.assets.init_local_storage();
		}
	}

	set_globals() {
		ragapp.session.user = ragapp.boot.user.name;
		ragapp.session.logged_in_user = ragapp.boot.user.name;
		ragapp.session.user_email = ragapp.boot.user.email;
		ragapp.session.user_fullname = ragapp.user_info().fullname;

		ragapp.user_defaults = ragapp.boot.user.defaults;
		ragapp.user_roles = ragapp.boot.user.roles;
		ragapp.sys_defaults = ragapp.boot.sysdefaults;

		ragapp.ui.py_date_format = ragapp.boot.sysdefaults.date_format
			.replace("dd", "%d")
			.replace("mm", "%m")
			.replace("yyyy", "%Y");
		ragapp.boot.user.last_selected_values = {};
	}
	sync_pages() {
		// clear cached pages if timestamp is not found
		if (localStorage["page_info"]) {
			ragapp.boot.allowed_pages = [];
			var page_info = JSON.parse(localStorage["page_info"]);
			$.each(ragapp.boot.page_info, function (name, p) {
				if (!page_info[name] || page_info[name].modified != p.modified) {
					delete localStorage["_page:" + name];
				}
				ragapp.boot.allowed_pages.push(name);
			});
		} else {
			ragapp.boot.allowed_pages = Object.keys(ragapp.boot.page_info);
		}
		localStorage["page_info"] = JSON.stringify(ragapp.boot.page_info);
	}
	set_as_guest() {
		ragapp.session.user = "Guest";
		ragapp.session.user_email = "";
		ragapp.session.user_fullname = "Guest";

		ragapp.user_defaults = {};
		ragapp.user_roles = ["Guest"];
		ragapp.sys_defaults = {};
	}
	make_page_container() {
		if ($("#body").length) {
			$(".splash").remove();
			ragapp.temp_container = $("<div id='temp-container' style='display: none;'>").appendTo(
				"body"
			);
			ragapp.container = new ragapp.views.Container();
		}
	}
	make_nav_bar() {
		// toolbar
		if (ragapp.boot && ragapp.boot.home_page !== "setup-wizard") {
			ragapp.ragapp_toolbar = new ragapp.ui.toolbar.Toolbar();
		}
	}
	logout() {
		var me = this;
		me.logged_out = true;
		return ragapp.call({
			method: "logout",
			callback: function (r) {
				if (r.exc) {
					return;
				}
				me.redirect_to_login();
			},
		});
	}
	handle_session_expired() {
		ragapp.app.redirect_to_login();
	}
	redirect_to_login() {
		window.location.href = `/login?redirect-to=${encodeURIComponent(
			window.location.pathname + window.location.search
		)}`;
	}
	set_favicon() {
		var link = $('link[type="image/x-icon"]').remove().attr("href");
		$('<link rel="shortcut icon" href="' + link + '" type="image/x-icon">').appendTo("head");
		$('<link rel="icon" href="' + link + '" type="image/x-icon">').appendTo("head");
	}
	trigger_primary_action() {
		// to trigger change event on active input before triggering primary action
		$(document.activeElement).blur();
		// wait for possible JS validations triggered after blur (it might change primary button)
		setTimeout(() => {
			if (window.cur_dialog && cur_dialog.display && !cur_dialog.is_minimized) {
				// trigger primary
				cur_dialog.get_primary_btn().trigger("click");
			} else if (cur_frm && cur_frm.page.btn_primary.is(":visible")) {
				cur_frm.page.btn_primary.trigger("click");
			} else if (ragapp.container.page.save_action) {
				ragapp.container.page.save_action();
			}
		}, 100);
	}

	show_change_log() {
		var me = this;
		let change_log = ragapp.boot.change_log;

		// ragapp.boot.change_log = [{
		// 	"change_log": [
		// 		[<version>, <change_log in markdown>],
		// 		[<version>, <change_log in markdown>],
		// 	],
		// 	"description": "ERP made simple",
		// 	"title": "NxERP",
		// 	"version": "12.2.0"
		// }];

		if (
			!Array.isArray(change_log) ||
			!change_log.length ||
			window.Cypress ||
			cint(ragapp.boot.sysdefaults.disable_change_log_notification)
		) {
			return;
		}

		// Iterate over changelog
		var change_log_dialog = ragapp.msgprint({
			message: ragapp.render_template("change_log", { change_log: change_log }),
			title: __("Updated To A New Version 🎉"),
			wide: true,
		});
		change_log_dialog.keep_open = true;
		change_log_dialog.custom_onhide = function () {
			ragapp.call({
				method: "ragapp.utils.change_log.update_last_known_versions",
			});
			me.show_notes();
		};
	}

	show_update_available() {
		if (!ragapp.boot.has_app_updates) return;
		ragapp.xcall("ragapp.utils.change_log.show_update_popup");
	}

	add_browser_class() {
		$("html").addClass(ragapp.utils.get_browser().name.toLowerCase());
	}

	set_fullwidth_if_enabled() {
		ragapp.ui.toolbar.set_fullwidth_if_enabled();
	}

	show_notes() {
		var me = this;
		if (ragapp.boot.notes.length) {
			ragapp.boot.notes.forEach(function (note) {
				if (!note.seen || note.notify_on_every_login) {
					var d = ragapp.msgprint({ message: note.content, title: note.title });
					d.keep_open = true;
					d.custom_onhide = function () {
						note.seen = true;

						// Mark note as read if the Notify On Every Login flag is not set
						if (!note.notify_on_every_login) {
							ragapp.call({
								method: "ragapp.desk.doctype.note.note.mark_as_seen",
								args: {
									note: note.name,
								},
							});
						}

						// next note
						me.show_notes();
					};
				}
			});
		}
	}

	setup_build_events() {
		if (ragapp.boot.developer_mode) {
			ragapp.require("build_events.bundle.js");
		}
	}

	setup_energy_point_listeners() {
		ragapp.realtime.on("energy_point_alert", (message) => {
			ragapp.show_alert(message);
		});
	}

	setup_copy_doc_listener() {
		$("body").on("paste", (e) => {
			try {
				let pasted_data = ragapp.utils.get_clipboard_data(e);
				let doc = JSON.parse(pasted_data);
				if (doc.doctype) {
					e.preventDefault();
					const sleep = ragapp.utils.sleep;

					ragapp.dom.freeze(__("Creating {0}", [doc.doctype]) + "...");
					// to avoid abrupt UX
					// wait for activity feedback
					sleep(500).then(() => {
						let res = ragapp.model.with_doctype(doc.doctype, () => {
							let newdoc = ragapp.model.copy_doc(doc);
							newdoc.__newname = doc.name;
							delete doc.name;
							newdoc.idx = null;
							newdoc.__run_link_triggers = false;
							ragapp.set_route("Form", newdoc.doctype, newdoc.name);
							ragapp.dom.unfreeze();
						});
						res && res.fail?.(ragapp.dom.unfreeze);
					});
				}
			} catch (e) {
				//
			}
		});
	}

	/// Setup event listeners for events across browser tabs / web workers.
	setup_broadcast_listeners() {
		// booted in another tab -> refresh csrf to avoid invalid requests.
		ragapp.broadcast.on("boot", ({ csrf_token, user }) => {
			if (user && user != ragapp.session.user) {
				ragapp.msgprint({
					message: __(
						"You've logged in as another user from another tab. Refresh this page to continue using system."
					),
					title: __("User Changed"),
					primary_action: {
						label: __("Refresh"),
						action: () => {
							window.location.reload();
						},
					},
				});
				return;
			}

			if (csrf_token) {
				// If user re-logged in then their other tabs won't be usable without this update.
				ragapp.csrf_token = csrf_token;
			}
		});
	}

	setup_moment() {
		moment.updateLocale("en", {
			week: {
				dow: ragapp.datetime.get_first_day_of_the_week_index(),
			},
		});
		moment.locale("en");
		moment.user_utc_offset = moment().utcOffset();
		if (ragapp.boot.timezone_info) {
			moment.tz.add(ragapp.boot.timezone_info);
		}
	}
};

ragapp.get_module = function (m, default_module) {
	var module = ragapp.modules[m] || default_module;
	if (!module) {
		return;
	}

	if (module._setup) {
		return module;
	}

	if (!module.label) {
		module.label = m;
	}

	if (!module._label) {
		module._label = __(module.label);
	}

	module._setup = true;

	return module;
};
