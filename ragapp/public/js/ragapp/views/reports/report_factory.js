// Copyright (c) 2025, KhulnaSoft, Ltd and Contributors
// MIT License. See license.txt

ragapp.views.ReportFactory = class ReportFactory extends ragapp.views.Factory {
	make(route) {
		const _route = ["List", route[1], "Report"];

		if (route[2]) {
			// custom report
			_route.push(route[2]);
		}

		ragapp.set_route(_route);
	}
};
