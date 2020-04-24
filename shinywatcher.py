import sys
import ast
import requests
import time
import json

from pymysql import connect
from datetime import datetime, timedelta
from configparser import ConfigParser


config = dict()
config_raw = ConfigParser()
config_raw.read("config.ini")

# CONFIG
config["wh"] = config_raw.get("Config", "WEBHOOK_URL")
config["tz"] = config_raw.getint("Config", "TIMEZONE_OFFSET")
config["workers"] = config_raw.get("Config", "ONLY_SHOW_WORKERS")
config["mons"] = config_raw.get("Config", "EXCLUDE_MONS")
config["mons"] = list(config["mons"].split(","))
config["locale"] = config_raw.get("Config", "LANGUAGE")
config["os"] = config_raw.get("Config", "OS")

# DB
config["db_dbname"] = config_raw.get("DB", "DB_NAME")
config["db_host"] = config_raw.get("DB", "HOST")
config["db_port"] = config_raw.getint("DB", "PORT")
config["db_user"] = config_raw.get("DB", "USER")
config["db_pass"] = config_raw.get("DB", "PASSWORD")

mydb = connect(
    host=config["db_host"],
    user=config["db_user"],
    passwd=config["db_pass"],
    database=config["db_dbname"],
    port=config["db_port"],
    autocommit=True,
)
cursor = mydb.cursor()

worker_filter = ""
if not config['workers'] == "":
    worker_filter = f"AND t.worker in ({config['workers']})"

mon_names = ast.literal_eval(open(f"locale/{config['locale']}-mons.txt", "r").read())

with open("workers.json", "r") as f:
    worker_mails = json.load(f)

def get_cache():
    return open("cache.txt", "r").read().splitlines()

def check_shinies():
    cursor.execute(f"SELECT encounter_id, pokemon_id, disappear_time, individual_attack, individual_defense, individual_stamina, cp_multiplier, longitude, latitude, t.worker FROM pokemon LEFT JOIN trs_stats_detect_raw t ON encounter_id = CAST(t.type_id AS UNSIGNED INTEGER) WHERE disappear_time > utc_timestamp() AND t.is_shiny = 1 {worker_filter} ORDER BY pokemon_id DESC, disappear_time DESC")
    results = cursor.fetchall()
    for enc_id, mon_id, etime, atk, defe, sta, cp_multiplier, lon, lat, worker in results:
        if str(enc_id) in get_cache():
            continue
        if mon_id in config['mons']:
            continue
        
        for aname, aid in mon_names.items():
            if str(aid) == str(mon_id):
                mon_name = aname.title()
        mon_img = f"https://raw.githubusercontent.com/Plaryu/PJSsprites/master/pokemon_icon_{str(mon_id).zfill(3)}_00.png"

        print(f"found shiny {mon_name}")

        iv = int(round((((atk + defe + sta) / 45) * 100), 0))
        etime = etime + timedelta(hours=config['tz'])
        end = etime.strftime("%H:%M:%S")
        td = etime - datetime.now()
        timeleft = divmod(td.seconds, 60)

        email = ""
        email = worker_mails[worker]

        if cp_multiplier < 0.734:
            mon_level = round(58.35178527 * cp_multiplier * cp_multiplier - 2.838007664 * cp_multiplier + 0.8539209906)
        else:
            mon_level = round(171.0112688 * cp_multiplier - 95.20425243)

        if config["os"] == "android":
            data = {
                "username": mon_name,
                "avatar_url": mon_img,
                "content": f"**{mon_name}** ({iv}%, lv{mon_level}) until **{end}** ({timeleft[0]}m {timeleft[1]}s)\n{worker} ({email})",
                "embeds": [
                    {
                    "description": f"{lat},{lon}"
                    }
                ]
            }
            result = requests.post(config['wh'], json=data)
            print(result)

        elif config['os'] == "ios":
            data = {
                "username": mon_name,
                "avatar_url": mon_img,
                "content": f"**{mon_name}** ({iv}%, lv{mon_level}) until **{end}** ({timeleft[0]}m {timeleft[1]}s)\n{worker} ({email})"
            }
            result = requests.post(config['wh'], json=data)
            print(result)

            time.sleep(1)
            data = {
                "username": mon_name,
                "avatar_url": mon_img,
                "content": f"```{lat},{lon}```"
            }
            result = requests.post(config['wh'], json=data)
            print(result)

        with open("cache.txt", "a") as f:
            f.write(f"{enc_id}\n")

        time.sleep(2)

check_shinies()

cursor.close()
mydb.close()
