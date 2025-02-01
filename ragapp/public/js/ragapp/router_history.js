ragapp.route_history_queue = [];
const routes_to_skip = ["Form", "social", "setup-wizard", "recorder"];

const save_routes = ragapp.utils.debounce(() => {
	if (ragapp.session.user === "Guest") return;
	const routes = ragapp.route_history_queue;
	if (!routes.length) return;

	ragapp.route_history_queue = [];

	ragapp
		.xcall("ragapp.desk.doctype.route_history.route_history.deferred_insert", {
			routes: routes,
		})
		.catch(() => {
			ragapp.route_history_queue.concat(routes);
		});
}, 10000);

ragapp.router.on("change", () => {
	const route = ragapp.get_route();
	if (is_route_useful(route)) {
		ragapp.route_history_queue.push({
			creation: ragapp.datetime.now_datetime(),
			route: ragapp.get_route_str(),
		});

		save_routes();
	}
});

function is_route_useful(route) {
	if (!route[1]) {
		return false;
	} else if ((route[0] === "List" && !route[2]) || routes_to_skip.includes(route[0])) {
		return false;
	} else {
		return true;
	}
}
