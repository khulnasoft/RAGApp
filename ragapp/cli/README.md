<div align="center">

![Logo](resources/logo.png)

## Cli
**CLI to manage Ragapp applications**


[![Python version](https://img.shields.io/badge/python-%3E=_3.10-green.svg)](https://www.python.org/downloads/)
[![PyPI Version](https://badge.fury.io/py/ragapp-cli.svg)](https://pypi.org/project/ragapp-cli)
![Platform Compatibility](https://img.shields.io/badge/platform-linux%20%7C%20macos-blue)

</div>

## Cli

Cli is a command-line utility that helps you to install, update, and manage multiple sites for Ragapp applications on [*nix systems](https://en.wikipedia.org/wiki/Unix-like) for development and production.

## Key features

Cli helps you set up and manage your ragapp sites with ease. Here are some of the key features:
- Initializing a new cli to work on sites and apps
- Creating a new ragapp site
- Creating and installing apps that can be used on the sites
- Managing ragapp sites
- Managing site backups

## Installation

A typical cli setup provides two types of environments &mdash; Development and Production.

The setup for each of these installations can be achieved in multiple ways:

 - [Containerized Installation](#containerized-installation)
 - [Manual Installation](https://docs.ragapp.io/framework/user/en/tutorial/install-and-setup-cli)

We recommend using Docker Installation to setup a Production Environment. For Development, you may choose either of the two methods to setup an instance.

Otherwise, if you are looking to evaluate Ragapp apps without the hassle of managing hosting yourself, you can try them on [Ragapp Cloud](https://ragappcloud.com/).

<div>
	<a href="https://ragappcloud.com/dashboard/signup" target="_blank">
		<picture>
			<source media="(prefers-color-scheme: dark)" srcset="https://ragapp.io/files/try-on-fc-white.png">
			<img src="https://ragapp.io/files/try-on-fc-black.png" alt="Try on Ragapp Cloud" height="28" />
		</picture>
	</a>
</div>

### Containerized Installation

A Ragapp instance can be setup and replicated easily using [Docker](https://docker.com). The officially supported Docker installation can be used to setup either of both Development and Production environments.

To setup either of the environments, you will need to clone the official docker repository:

```sh
git clone https://github.com/khulnasoft/ragapp_docker.git
```

A quick setup guide for both the environments can be found below. For more details, check out the [Ragapp Docker Repository](https://github.com/khulnasoft/ragapp_docker).

### Easy Install Script

The Easy Install script should get you going with a Ragapp setup with minimal manual intervention and effort.

This script uses Docker with the [Ragapp Docker Repository](https://github.com/khulnasoft/ragapp_docker) and can be used for both Development setup and Production setup.

#### Setup

Download the Easy Install script and execute it:

```sh
wget https://raw.githubusercontent.com/ragapp/cli/develop/easy-install.py
python3 easy-install.py deploy --email=user@domain.tld --sitename=subdomain.domain.tld --app=erpnext
```

This script will install docker on your system and will fetch the required containers, setup cli and a default NxERP instance.

The script will generate MySQL root password and an Administrator password for the Ragapp/NxERP instance, which will then be saved under `$HOME/passwords.txt` of the user used to setup the instance.
It will also generate a new compose file under `$HOME/<project-name>-compose.yml`.

When the setup is complete, you will be able to access the system at `http://<your-server-ip>`, wherein you can use the Administrator password to login.

#### Arguments

Here are the arguments for the easy-install script

<details>
<summary><b>Build custom images</b></summary>

```txt
usage: easy-install.py build [-h] [-n PROJECT] [-i IMAGE] [-q] [-m HTTP_PORT] [-v VERSION] [-a APPS] [-s SITES] [-e EMAIL]
                             [-p] [-r RAGAPP_PATH] [-b RAGAPP_BRANCH] [-j APPS_JSON] [-t TAGS] [-c CONTAINERFILE]
                             [-y PYTHON_VERSION] [-d NODE_VERSION] [-x] [-u]

options:
  -h, --help            show this help message and exit
  -n PROJECT, --project PROJECT
                        Project Name
  -g, --backup-schedule BACKUP_SCHEDULE
                        Backup schedule cronstring, default: "@every 6h"
  -i IMAGE, --image IMAGE
                        Full Image Name
  -q, --no-ssl          No https
  -m HTTP_PORT, --http-port HTTP_PORT
                        Http port in case of no-ssl
  -v VERSION, --version VERSION
                        NxERP version to install, defaults to latest stable
  -a APPS, --app APPS   list of app(s) to be installed
  -s SITES, --sitename SITES
                        Site Name(s) for your production cli
  -e EMAIL, --email EMAIL
                        Add email for the SSL.
  -p, --push            Push the built image to registry
  -r RAGAPP_PATH, --ragapp-path RAGAPP_PATH
                        Ragapp Repository to use, default: https://github.com/khulnasoft/ragapp
  -b RAGAPP_BRANCH, --ragapp-branch RAGAPP_BRANCH
                        Ragapp branch to use, default: version-15
  -j APPS_JSON, --apps-json APPS_JSON
                        Path to apps json, default: ragapp_docker/development/apps-example.json
  -t TAGS, --tag TAGS   Full Image Name(s), default: custom-apps:latest
  -c CONTAINERFILE, --containerfile CONTAINERFILE
                        Path to Containerfile: images/layered/Containerfile
  -y PYTHON_VERSION, --python-version PYTHON_VERSION
                        Python Version, default: 3.11.6
  -d NODE_VERSION, --node-version NODE_VERSION
                        NodeJS Version, default: 18.18.2
  -x, --deploy          Deploy after build
  -u, --upgrade         Upgrade after build
```
</details>

<details>
<summary><b>Deploy using compose</b></summary>

```txt
usage: easy-install.py deploy [-h] [-n PROJECT] [-i IMAGE] [-q] [-m HTTP_PORT] [-v VERSION] [-a APPS] [-s SITES] [-e EMAIL]

options:
  -h, --help            show this help message and exit
  -n PROJECT, --project PROJECT
                        Project Name
  -g, --backup-schedule BACKUP_SCHEDULE
                        Backup schedule cronstring, default: "@every 6h"
  -i IMAGE, --image IMAGE
                        Full Image Name
  -q, --no-ssl          No https
  -m HTTP_PORT, --http-port HTTP_PORT
                        Http port in case of no-ssl
  -v VERSION, --version VERSION
                        NxERP version to install, defaults to latest stable
  -a APPS, --app APPS   list of app(s) to be installed
  -s SITES, --sitename SITES
                        Site Name(s) for your production cli
  -e EMAIL, --email EMAIL
                        Add email for the SSL.
```
</details>

<details>
<summary><b>Upgrade existing project</b></summary>

```txt
usage: easy-install.py upgrade [-h] [-n PROJECT] [-i IMAGE] [-q] [-m HTTP_PORT] [-v VERSION]

options:
  -h, --help            show this help message and exit
  -n PROJECT, --project PROJECT
                        Project Name
  -g, --backup-schedule BACKUP_SCHEDULE
                        Backup schedule cronstring, default: "@every 6h"
  -i IMAGE, --image IMAGE
                        Full Image Name
  -q, --no-ssl          No https
  -m HTTP_PORT, --http-port HTTP_PORT
                        Http port in case of no-ssl
  -v VERSION, --version VERSION
                        NxERP or image version to install, defaults to latest stable
```
</details>

<details>
<summary><b>Development setup using compose</b></summary>

```txt
usage: easy-install.py develop [-h] [-n PROJECT]

options:
  -h, --help            show this help message and exit
  -n PROJECT, --project PROJECT
                        Compose project name
```
</details>

<details>
<summary><b>Exec into existing project</b></summary>

```txt
usage: easy-install.py exec [-h] [-n PROJECT]

options:
  -h, --help            show this help message and exit
  -n PROJECT, --project PROJECT
                        Project Name
```
</details>

To use custom apps, you need to create a json file with list of apps and pass it to build command.

Example apps.json

```json
[
  {
    "url": "https://github.com/khulnasoft/wiki.git",
    "branch": "master"
  }
]
```

Execute following command to build and deploy above apps:

```sh
$ python3 easy-install.py build \
	--tag=ghcr.io/org/repo/custom-apps:latest \
	--push \
	--image=ghcr.io/org/repo/custom-apps \
	--version=latest \
	--deploy \
	--project=actions_test \
	--email=test@ragapp.io \
	--apps-json=apps.json \
	--app=wiki
```

Note:

- `--tag`, tag to set for built image, can be multiple.
- `--push`, push the built image.
- `--image`, the image to use when starting docker compose project.
- `--version`, the version to use when starting docker compose project.
- `--app`, app to install on site creation, can be multiple.
- `--deploy`, flag to deploy after build/push is complete
- `--project=actions_test`, name of the project, compose file with project name will be stored in user home directory.
- `--email=test@ragapp.io`, valid email for letsencrypt certificate expiry notification.
- `--apps-json`, path to json file with list of apps to be added to cli.

#### Troubleshooting

In case the setup fails, the log file is saved under `$HOME/easy-install.log`. You may then

- Create an Issue in this repository with the log file attached.

## Basic Usage

**Note:** Apart from `cli init`, all other cli commands are expected to be run in the respective cli directory.

 * Create a new cli:

	```sh
	$ cli init [cli-name]
	```

 * Add a site under current cli:

	```sh
	$ cli new-site [site-name]
	```
	- **Optional**: If the database for the site does not reside on localhost or listens on a custom port, you can use the flags `--db-host` to set a custom host and/or `--db-port` to set a custom port.

		```sh
		$ cli new-site [site-name] --db-host [custom-db-host-ip] --db-port [custom-db-port]
		```

 * Download and add applications to cli:

	```sh
	$ cli get-app [app-name] [app-link]
	```

 * Install apps on a particular site

	```sh
	$ cli --site [site-name] install-app [app-name]
	```

 * Start cli (only for development)

	```sh
	$ cli start
	```

 * Show cli help:

	```sh
	$ cli --help
	```


For more in-depth information on commands and their usage, follow [Commands and Usage](https://github.com/khulnasoft/ragapp/blob/develop/docs/commands_and_usage.md). As for a consolidated list of cli commands, check out [Cli Usage](https://github.com/khulnasoft/ragapp/blob/develop/docs/cli_usage.md).

![Help](resources/help.png)


## Custom Cli Commands

If you wish to extend the capabilities of cli with your own custom Ragapp Application, you may follow [Adding Custom Cli Commands](https://github.com/khulnasoft/ragapp/blob/develop/docs/cli_custom_cmd.md).


## Guides

- [Configuring HTTPS](https://docs.ragapp.io/framework/user/en/cli/guides/configuring-https)
- [Using Let's Encrypt to setup HTTPS](https://docs.ragapp.io/framework/user/en/cli/guides/lets-encrypt-ssl-setup)
- [Diagnosing the Scheduler](https://docs.ragapp.io/framework/user/en/cli/guides/diagnosing-the-scheduler)
- [Change Hostname](https://docs.ragapp.io/framework/user/en/cli/guides/adding-custom-domains)
- [Manual Setup](https://docs.ragapp.io/framework/user/en/tutorial/install-and-setup-cli)
- [Setup Production](https://docs.ragapp.io/framework/user/en/cli/guides/setup-production)
- [Setup Multitenancy](https://docs.ragapp.io/framework/user/en/cli/guides/setup-multitenancy)
- [Stopping Production](https://github.com/khulnasoft/ragapp/wiki/Stopping-Production-and-starting-Development)


## Resources

- [Cli Commands Cheat Sheet](https://docs.ragapp.io/framework/user/en/cli/resources/cli-commands-cheatsheet)
- [Background Services](https://docs.ragapp.io/framework/user/en/cli/resources/background-services)
- [Cli Procfile](https://docs.ragapp.io/framework/user/en/cli/resources/cli-procfile)


## Development

To contribute and develop on the cli CLI tool, clone this repo and create an editable install. In editable mode, you may get the following warning everytime you run a cli command:

	WARN: cli is installed in editable mode!

	This is not the recommended mode of installation for production. Instead, install the package from PyPI with: `pip install ragapp-cli`

### Clone and install

```sh
git clone https://github.com/khulnasoft/ragapp ~/cli-repo
pip install -e ~/cli-repo
```

```shell
cli src
```
This should display $HOME/cli-repo

### To clear up the editable install and delete the corresponding egg file from the python path:

```sh
# Delete cli installed in editable install
rm -r $(find ~ -name '*.egg-info')
pip uninstall ragapp-cli
```

### Then you can install the latest from PyPI
```sh
pip install -U ragapp-cli
```

To confirm the switch, check the output of `cli src`. It should change from something like `$HOME/cli-repo` to `/usr/local/lib/python3.12/dist-packages` and stop the editable install warnings from getting triggered at every command.


## Releases

Cli's version information can be accessed via `cli.VERSION` in the package's __init__.py file. Ever since the v5.0 release, we've started publishing releases on GitHub, and PyPI.

[GitHub](https://github.com/khulnasoft/ragapp/releases)
[Pypi](https://pypi.org/project/ragapp-cli)


## Learn and connect

- [Discuss](https://discuss.ragapp.io/)
- [YouTube](https://www.youtube.com/@ragapptech)

## Contribute
To contribute to this project, please review the [Contribution Guidelines](https://github.com/khulnasoft-lab/nxerp/wiki/Contribution-Guidelines) for detailed instructions. Make sure to follow our [Code of Conduct](https://github.com/khulnasoft/ragapp/blob/develop/CODE_OF_CONDUCT.md) to keep the community welcoming and respectful.

## Security
The Ragapp team and community prioritize security. If you discover a security issue, please report it via our [Security Report Form](https://ragapp.io/security).
Your responsible disclosure helps keep Ragapp and its users safe. We'll do our best to respond quickly and keep you informed throughout the process.
For guidelines on reporting, check out our [Reporting Guidelines](https://ragapp.io/security), and review our [Logo and Trademark Policy](https://github.com/khulnasoft-lab/nxerp/blob/develop/TRADEMARK_POLICY.md) for branding information.

<br/><br/>
<div align="center">
	<a href="https://ragapp.io" target="_blank">
		<picture>
			<source media="(prefers-color-scheme: dark)" srcset="https://ragapp.io/files/Ragapp-white.png">
			<img src="https://ragapp.io/files/Ragapp-black.png" alt="Ragapp Technologies" height="28"/>
		</picture>
	</a>
</div>
