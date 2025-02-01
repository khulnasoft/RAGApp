# Releasing Ragapp NxERP

* Make a new cli dedicated for releasing
```
cli init release-cli --ragapp-path git@github.com:ragapp/ragapp.git
```

* Get NxERP in the release cli
```
cli get-app erpnext git@github.com:ragapp/erpnext.git
```

* Configure as release cli. Add this to the common_site_config.json
```
"release_cli": true,
```

* Add branches to update in common_site_config.json
```
"branches_to_update": {
    "staging": ["develop", "hotfix"],
    "hotfix": ["develop", "staging"]
}
```

* Use the release commands to release
```
Usage: cli release [OPTIONS] APP BUMP_TYPE
```

* Arguments :
  * _APP_ App name e.g [ragapp|erpnext|yourapp]
  * _BUMP_TYPE_ [major|minor|patch|stable|prerelease]
* Options:
  * --from-branch git develop branch, default is develop
  * --to-branch git master branch, default is master
  * --remote git remote, default is upstream
  * --owner git owner, default is ragapp
  * --repo-name git repo name if different from app name
  
* When updating major version, update `develop_version` in hooks.py, e.g. `9.x.x-develop`
