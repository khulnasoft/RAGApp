"""Module for setting up system and respective cli configurations"""


def env():
	from jinja2 import Environment, PackageLoader

	return Environment(loader=PackageLoader("cli.config"))
