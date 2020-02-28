# Shiny Watcher

Shiny Watcher checks your DB for active Shinies and then sends a notification to Discord if it finds any. It allows to filter out Pokemon and Workers, as well as connect a Login E-Mail for every worker.

Notifications will always be: `Name (IV%) until Time (time left)\nWorker name (account/email)`. The coordinates are in an embed so you can copy them by only holding them tapped for ~2 seconds on an Android device. Fast and easy

![Screenshot](https://i.imgur.com/kvUSoI4.png)

## Notes
- Only works with python3.6 and above
- MAD and Discord only
- Credits to [Naji](https://github.com/na-ji/mad-shiny-notifications) who inspired me to do this

## Getting Started
- `cp config.ini.example config.ini && cp workers.json.example workers.json`
- Fill out config.ini and workers.json (It's explained below what to fill in)
- `python3 shinywatcher.py`
- The script does not loop itself. You can use pm2 (`pm2 start shinywatcher.py --interpreter=python3 --restart-delay=10000`) or cron to only have it send notifications between work and sleep. Make sure to use `cd /path/shinywatcher/ && python3 shinywatcher.py`

## What to fill in
### Config
- `ONLY_SHOW_WORKERS` Leave blank if you want notifications from all workers. If you only want them from certain Accounts, follow the format in the example
- `EXCLUDE_MONS` Filter out Mons you already you already have enough Shinies of. Follow the example format!
### workers.json
- What you put in here will be used as the account name in your notifications
- To set it up, just follow the example. `"{Worker Name}": "{Account Name/E-Mail}"` and repeat
