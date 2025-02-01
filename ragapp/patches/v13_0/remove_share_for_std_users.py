import ragapp
import ragapp.share


def execute():
	for user in ragapp.STANDARD_USERS:
		ragapp.share.remove("User", user, user)
