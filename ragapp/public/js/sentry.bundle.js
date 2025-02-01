import * as Sentry from "@sentry/browser";

Sentry.init({
	dsn: ragapp.boot.sentry_dsn,
	release: ragapp?.boot?.versions?.ragapp,
	autoSessionTracking: false,
	initialScope: {
		// don't use ragapp.session.user, it's set much later and will fail because of async loading
		user: { id: ragapp.boot.sitename },
		tags: { ragapp_user: ragapp.boot.user.name ?? "Unidentified" },
	},
	beforeSend(event, hint) {
		// Check if it was caused by ragapp.throw()
		if (
			hint.originalException instanceof Error &&
			hint.originalException.stack &&
			hint.originalException.stack.includes("ragapp.throw")
		) {
			return null;
		}
		return event;
	},
});
