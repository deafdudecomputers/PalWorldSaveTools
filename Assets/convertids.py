from import_libs import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import logging
def get_steam_id_from_local():
    local_app_data_path = os.path.expandvars(r"%localappdata%\Pal\Saved\SaveGames")
    try:
        if not os.path.exists(local_app_data_path): return None
        subdirs = [d for d in os.listdir(local_app_data_path) if os.path.isdir(os.path.join(local_app_data_path, d))]
        if not subdirs: return None
        return subdirs[0]
    except: return None
def fetch_palworld_uids(steam_id):
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--headless')
    options.add_argument('--disable-extensions')
    options.add_argument('--disable-gpu')
    options.add_argument('--remote-debugging-port=0')
    options.add_argument('--log-level=3')
    options.add_argument('--silent')
    logging.getLogger('selenium.webdriver.remote.remote_connection').setLevel(logging.WARNING)
    sys.stderr = open(os.devnull, 'w')
    driver = None
    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        driver.get("https://uid.palservers.xyz/")
        input_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "input")))
        input_field.send_keys(steam_id)
        input_field.send_keys(Keys.RETURN)
        pre_element = driver.find_element(By.XPATH, "//pre[contains(text(), 'Steam ID:')]")
        result_text = pre_element.text
        lines = result_text.split('\n')
        steam_uid = lines[0].split(': ')[1] if len(lines) > 0 else None
        hex_uid_steam = lines[1].split(': ')[1] if len(lines) > 1 else None
        hex_uid_nosteam = lines[5].split(': ')[1] if len(lines) > 5 else None
        return {
            "steam_id": steam_uid,
            "steam_profile_url": f"https://steamcommunity.com/profiles/{steam_uid}",
            "palworld_uid_steam_hex": f"{hex_uid_steam}-0000-0000-0000-000000000000" if hex_uid_steam else None,
            "palworld_uid_nosteam_hex": f"{hex_uid_nosteam}-0000-0000-0000-000000000000" if hex_uid_nosteam else None
        }
    except Exception as e:
        print(f"❌ Error fetching data: {e}")
    finally:
        if driver:
            driver.quit()
    return None    
steam_id_from_local = get_steam_id_from_local()
if steam_id_from_local:
    result = fetch_palworld_uids(steam_id_from_local)    
    if result:
        hex_uid_steam = result.get("palworld_uid_steam_hex", "Not found")
        hex_uid_nosteam = result.get("palworld_uid_nosteam_hex", "Not found")
        print(f"Your SteamID: {steam_id_from_local}")
        print(f"Your Steam Profile URL: https://steamcommunity.com/profiles/{steam_id_from_local}")
        print(f"Your Palworld UID (Steam): {hex_uid_steam}")
        print(f"Your Palworld UID (NoSteam): {hex_uid_nosteam}")
steam_input = input("Enter SteamID (with or without 'steam_' or full URL): ")
if "steamcommunity.com/profiles/" in steam_input: 
    steam_input = steam_input.split("steamcommunity.com/profiles/")[1].split("/")[0]
elif steam_input.startswith("steam_"): 
    steam_input = steam_input[6:]
try:
    steam_id = int(steam_input)
    result = fetch_palworld_uids(steam_id)    
    if result:
        palworld_uid = result["palworld_uid_steam_hex"]
        nosteam_uid = result["palworld_uid_nosteam_hex"]        
        print("Palworld UID:", palworld_uid.upper())
        print("NoSteam UID:", nosteam_uid.upper())
    else:
        print("❌ Failed to fetch UIDs from the website.")
except ValueError:
    pass