#!/bin/bash
set -e
cd ~ || exit

echo "Setting Up Cli..."

pip install ragapp-cli
cli -v init ragapp-cli --skip-assets --skip-redis-config-generation --python "$(which python)" --ragapp-path "${GITHUB_WORKSPACE}"
cd ./ragapp-cli || exit

echo "Generating POT file..."
cli generate-pot-file --app ragapp

cd ./apps/ragapp || exit

echo "Configuring git user..."
git config user.email "developers@erpnext.com"
git config user.name "ragapp-pr-bot"

echo "Setting the correct git remote..."
# Here, the git remote is a local file path by default. Let's change it to the upstream repo.
git remote set-url upstream https://github.com/khulnasoft/ragapp.git

echo "Creating a new branch..."
isodate=$(date -u +"%Y-%m-%d")
branch_name="pot_${BASE_BRANCH}_${isodate}"
git checkout -b "${branch_name}"

echo "Commiting changes..."
git add ragapp/locale/main.pot
git commit -m "chore: update POT file"

gh auth setup-git
git push -u upstream "${branch_name}"

echo "Creating a PR..."
gh pr create --fill --base "${BASE_BRANCH}" --head "${branch_name}" -R ragapp/ragapp
