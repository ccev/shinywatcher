# Shiny Watcher

**Please note that Shiny Watcher is no standalone project. If you want this to work, you need to set up a whole MAD scanner. I recommend to only use this if you already have MAD running and just want to know about shinies it's finding.**

- Get support on this [Discord Server](https://discord.gg/cMZs5tk)
- If you want to use Shiny Watcher as a MAD Plugin, check out [this fork](https://github.com/GhostTalker/shinywatcher) - it's pretty easy to get it running
- If you use RDM, there's probably an easier solution to this since shiny data is sent via webhook

Shiny Watcher checks your DB for active Shinies and then sends a notification to Discord if it finds any. It allows to filter out Pokemon and Workers as well as connect a Login E-Mail to every worker.

Notifications will always be: `Name (IV%) until Time (time left)\nWorker name (account/email)`. The coordinates are in an embed so you can copy them by pressing for ~2 seconds on an Android device. Fast and easy. There's also an option to optimize notifications for iOS.

![Screenshot](https://i.imgur.com/kvUSoI4.png)

## Notes
- Only works with python3.6 and above
- MAD and Discord only
- Credits to [Naji](https://github.com/na-ji/mad-shiny-notifications) who inspired me to do this

## Getting Started
- `cp config.ini.example config.ini && cp workers.json.example workers.json`
- Fill out config.ini and workers.json (It's explained below what to fill in)
- `python3 shinywatcher.py`
- The script does not loop itself. You can use pm2 (`pm2 start shinywatcher.py --interpreter=python3 --restart-delay=10000`) to loop it or make a cronjob to only have it send notifications between work and sleep. Make sure to use `cd /path/shinywatcher/ && python3 shinywatcher.py` in it

## What to fill in
### Config
- `ONLY_SHOW_WORKERS` Leave blank if you want notifications from all workers. If you only want them from certain Accounts, follow the format in the example
- `EXCLUDE_MONS` Filter out Mons you already have enough Shinies of. Follow the example format!
- `OS` Set your notifications to `android` or `ios` mode. On Android, messages have an embed contaning the coords. For iOS an extra message containing coords will be sent
### workers.json
- What you put in here will be used as the account name in your notifications
- To set it up, just follow the example. `"{Worker Name}": "{Account Name/E-Mail}"` and repeat
