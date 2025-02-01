# cli CLI Usage

This may not be known to a lot of people but half the cli commands we're used to, exist in the Ragapp Framework and not in cli directly. Those commands generally are the `--site` commands. This page is concerned only with the commands in the cli project. Any framework commands won't be a part of this consolidation.


# cli CLI Commands

Under Click's structure, `cli` is the main command group, under which there are three main groups of commands in cli currently, namely

 - **install**: The install command group deals with commands used to install system dependencies for setting up Ragapp environment

 - **setup**: This command group for consists of commands used to maipulate the requirements and environments required by your Ragapp environment

 - **config**: The config command group deals with making changes in the current cli (not the CLI tool) configuration


## Using the cli command line

```zsh
➜ cli
Usage: cli [OPTIONS] COMMAND [ARGS]...

  Cli manager for Ragapp

Options:
  --version
  --help     Show this message and exit.

Commands:
  backup                   Backup single site
  backup-all-sites         Backup all sites in current cli
  config                   Change cli configuration
  disable-production       Disables production environment for the cli.
  download-translations    Download latest translations
  exclude-app              Exclude app from updating
  find                     Finds clies recursively from location
  get-app                  Clone an app from the internet or filesystem and...
```

Similarly, all available flags and options can be checked for commands individually by executing them with the `--help` flag. The `init` command for instance:

```zsh
➜ cli init --help
Usage: cli init [OPTIONS] PATH

  Initialize a new cli instance in the specified path

Options:
  --python TEXT                   Path to Python Executable.
  --ignore-exist                  Ignore if Cli instance exists.
  --apps_path TEXT                path to json files with apps to install
                                  after init
```



## cli and sudo

Some cli commands may require sudo, such as some `setup` commands and everything else under the `install` commands group. For these commands, you may not be asked for your root password if sudoers setup has been done. The security implications, well we'll talk about those soon.



## General Commands

These commands belong directly to the cli group so they can be invoked directly prefixing each with `cli` in your shell. Therefore, the usage for these commands is as

```zsh
    cli COMMAND [ARGS]...
```

### The usual commands

 - **init**: Initialize a new cli instance in the specified path. This sets up a complete cli folder with an `apps` folder which contains all the Ragapp apps available in the current cli, `sites` folder that stores all site data seperated by individual site folders, `config` folder that contains your redis, NGINX and supervisor configuration files. The `env` folder consists of all python dependencies the current cli and installed Ragapp applications have.
 - **restart**: Restart web, supervisor, systemd processes units. Used in production setup.
 - **update**: If executed in a cli directory, without any flags will backup, pull, setup requirements, build, run patches and restart cli. Using specific flags will only do certain tasks instead of all.
 - **migrate-env**: Migrate Virtual Environment to desired Python version. This regenerates the `env` folder with the specified Python version.
 - **retry-upgrade**: Retry a failed upgrade
 - **disable-production**: Disables production environment for the cli.
 - **renew-lets-encrypt**: Renew Let's Encrypt certificate for site SSL.
 - **backup**: Backup single site data. Can be used to backup files as well.
 - **backup-all-sites**: Backup all sites in current cli.

 - **get-app**: Download an app from the internet or filesystem and set it up in your cli. This clones the git repo of the Ragapp project and installs it in the cli environment.
 - **remove-app**: Completely remove app from cli and re-build assets if not installed on any site.
 - **exclude-app**: Exclude app from updating during a `cli update`
 - **include-app**: Include app for updating. All Ragapp applications are included by default when installed.
 - **remote-set-url**: Set app remote url
 - **remote-reset-url**: Reset app remote url to ragapp official
 - **remote-urls**: Show apps remote url
 - **switch-to-branch**: Switch all apps to specified branch, or specify apps separated by space
 - **switch-to-develop**: Switch Ragapp and NxERP to develop branch


### A little advanced

 - **set-nginx-port**: Set NGINX port for site
 - **set-ssl-certificate**: Set SSL certificate path for site
 - **set-ssl-key**: Set SSL certificate private key path for site
 - **set-url-root**: Set URL root for site
 - **set-mariadb-host**: Set MariaDB host for cli
 - **set-redis-cache-host**: Set Redis cache host for cli
 - **set-redis-queue-host**: Set Redis queue host for cli
 - **set-redis-socketio-host**: Set Redis socketio host for cli
 - **use**: Set default site for cli
 - **download-translations**: Download latest translations


### Developer's commands

 - **start**: Start Ragapp development processes. Uses the Procfile to start the Ragapp development environment.
 - **src**: Prints cli source folder path, which can be used to cd into the cli installation repository by `cd $(cli src)`.
 - **find**: Finds clies recursively from location or specified path.
 - **pip**: Use the current cli's pip to manage Python packages. For help about pip usage: `cli pip help [COMMAND]` or `cli pip [COMMAND] -h`.
 - **new-app**: Create a new Ragapp application under apps folder.


### Release cli
 - **release**: Create a release of a Ragapp application
 - **prepare-beta-release**: Prepare major beta release from develop branch



## Setup commands

The setup commands used for setting up the Ragapp environment in context of the current cli need to be executed using `cli setup` as the prefix. So, the general usage of these commands is as

```zsh
    cli setup COMMAND [ARGS]...
```

 - **sudoers**: Add commands to sudoers list for allowing cli commands execution without root password

 - **env**: Setup Python virtual environment for cli. This sets up a `env` folder under the root of the cli directory.
 - **redis**: Generates configuration for Redis
 - **fonts**: Add Ragapp fonts to system
 - **config**: Generate or over-write sites/common_site_config.json
 - **backups**: Add cronjob for cli backups
 - **socketio**: Setup node dependencies for socketio server
 - **requirements**: Setup Python and Node dependencies

 - **manager**: Setup `cli-manager.local` site with the [Cli Manager](https://github.com/khulnasoft/ragapp_manager) app, a GUI for cli installed on it.

 - **procfile**: Generate Procfile for cli start

 - **production**: Setup Ragapp production environment for specific user. This installs ansible, NGINX, supervisor, fail2ban and generates the respective configuration files.
 - **nginx**: Generate configuration files for NGINX
 - **fail2ban**: Setup fail2ban, an intrusion prevention software framework that protects computer servers from brute-force attacks
 - **systemd**: Generate configuration for systemd
 - **firewall**: Setup firewall for system
 - **ssh-port**: Set SSH Port for system
 - **reload-nginx**: Checks NGINX config file and reloads service
 - **supervisor**: Generate configuration for supervisor
 - **lets-encrypt**: Setup lets-encrypt SSL for site
 - **wildcard-ssl**: Setup wildcard SSL certificate for multi-tenant cli

 - **add-domain**: Add a custom domain to a particular site
 - **remove-domain**: Remove custom domain from a site
 - **sync-domains**: Check if there is a change in domains. If yes, updates the domains list.

 - **role**: Install dependencies via ansible roles



## Config commands

The config group commands are used for manipulating configurations in the current cli context. The usage for these commands is as

```zsh
    cli config COMMAND [ARGS]...
```

 - **set-common-config**: Set value in common config
 - **remove-common-config**: Remove specific keys from current cli's common config

 - **update_cli_on_update**: Enable/Disable cli updates on running cli update
 - **restart_supervisor_on_update**: Enable/Disable auto restart of supervisor processes
 - **restart_systemd_on_update**: Enable/Disable auto restart of systemd units
 - **dns_multitenant**: Enable/Disable cli multitenancy on running cli update
 - **serve_default_site**: Configure nginx to serve the default site on port 80
 - **http_timeout**: Set HTTP timeout



## Install commands

The install group commands are used for manipulating system level dependencies. The usage for these commands is as

```zsh
    cli install COMMAND [ARGS]...
```

 - **prerequisites**: Installs pre-requisite libraries, essential tools like b2zip, htop, screen, vim, x11-fonts, python libs, cups and Redis
 - **nodejs**: Installs Node.js v8
 - **nginx**: Installs NGINX. If user is specified, sudoers is setup for that user
 - **packer**: Installs Oracle virtualbox and packer 1.2.1
 - **psutil**: Installs psutil via pip
 - **mariadb**: Install and setup MariaDB of specified version and root password
 - **wkhtmltopdf**: Installs wkhtmltopdf v0.12.3 for linux
 - **supervisor**: Installs supervisor. If user is specified, sudoers is setup for that user
 - **fail2ban**: Install fail2ban, an intrusion prevention software framework that protects computer servers from brute-force attacks
 - **virtualbox**: Installs supervisor
