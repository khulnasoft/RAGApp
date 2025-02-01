# Copyright (c) 2021, Ragapp Technologies Pvt. Ltd. and Contributors
# MIT License. See license.txt


import functools

import ragapp


@ragapp.whitelist()
def get_google_fonts():
	return _get_google_fonts()


@functools.lru_cache
def _get_google_fonts():
	file_path = ragapp.get_app_path("ragapp", "data", "google_fonts.json")
	return ragapp.parse_json(ragapp.read_file(file_path))
