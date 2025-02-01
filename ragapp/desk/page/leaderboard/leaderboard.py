# Copyright (c) 2017, Ragapp Technologies Pvt. Ltd. and Contributors
# License: MIT. See LICENSE
import ragapp


@ragapp.whitelist()
def get_leaderboard_config():
	leaderboard_config = ragapp._dict()
	leaderboard_hooks = ragapp.get_hooks("leaderboards")
	for hook in leaderboard_hooks:
		leaderboard_config.update(ragapp.get_attr(hook)())

	return leaderboard_config
