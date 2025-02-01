## Usage

* Updating

To update the cli CLI tool, depending on your method of installation, you may use 

	pip3 install -U ragapp-cli


To backup, update all apps and sites on your cli, you may use

	cli update


To manually update the cli, run `cli update` to update all the apps, run
patches, build JS and CSS files and restart supervisor (if configured to).

You can also run the parts of the cli selectively.

`cli update --pull` will only pull changes in the apps

`cli update --patch` will only run database migrations in the apps

`cli update --build` will only build JS and CSS files for the cli

`cli update --cli` will only update the cli utility (this project)

`cli update --requirements` will only update all dependencies (Python + Node) for the apps available in current cli


* Create a new cli

	The init command will create a cli directory with ragapp framework installed. It will be setup for periodic backups and auto updates once a day.

		cli init ragapp-cli && cd ragapp-cli

* Add a site

	Ragapp apps are run by ragapp sites and you will have to create at least one site. The new-site command allows you to do that.

		cli new-site site1.local

* Add apps

	The get-app command gets remote ragapp apps from a remote git repository and installs them. Example: [erpnext](https://github.com/khulnasoft-lab/nxerp)

		cli get-app erpnext https://github.com/khulnasoft-lab/nxerp

* Install apps

	To install an app on your new site, use the cli `install-app` command.

		cli --site site1.local install-app erpnext

* Start cli

	To start using the cli, use the `cli start` command

		cli start

	To login to Ragapp / NxERP, open your browser and go to `[your-external-ip]:8000`, probably `localhost:8000`

	The default username is "Administrator" and password is what you set when you created the new site.

* Setup Manager

## What it does

		cli setup manager

1. Create new site cli-manager.local
2. Gets the `cli_manager` app from https://github.com/khulnasoft/ragapp_manager if it doesn't exist already
3. Installs the cli_manager app on the site cli-manager.local

