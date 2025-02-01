Add the following configuration to `launch.json` `configurations` array to start bench console and use debugger. Replace `development.localhost` with appropriate site. Also replace `ragapp-bench` with name of the bench directory.

```json
{
  "name": "Bench Console",
  "type": "python",
  "request": "launch",
  "program": "${workspaceFolder}/ragapp-bench/apps/ragapp/ragapp/utils/bench_helper.py",
  "args": ["ragapp", "--site", "development.localhost", "console"],
  "pythonPath": "${workspaceFolder}/ragapp-bench/env/bin/python",
  "cwd": "${workspaceFolder}/ragapp-bench/sites",
  "env": {
    "DEV_SERVER": "1"
  }
}
```
