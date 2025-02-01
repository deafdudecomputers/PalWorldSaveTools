from import_libs import *
from playwright.sync_api import sync_playwright
def get_steam_id_from_local():
    local_app_data_path = os.path.expandvars(r"%localappdata%\Pal\Saved\SaveGames")
    if os.path.exists(local_app_data_path):
        subdirs = [d for d in os.listdir(local_app_data_path) if os.path.isdir(os.path.join(local_app_data_path, d))]
        return subdirs[0] if subdirs else None
    return None
def fetch_palworld_uids(steam_id):
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto("https://uid.palservers.xyz/")
            page.fill("input", steam_id)
            page.press("input", "Enter")
            page.wait_for_selector("pre", timeout=10)
            pre_element = page.query_selector("pre")
            result_text = pre_element.inner_text()
            lines = result_text.split('\n')
            return {
                "steam_id": lines[0].split(': ')[1] if len(lines) > 0 else None,
                "steam_profile_url": f"https://steamcommunity.com/profiles/{lines[0].split(': ')[1]}" if len(lines) > 0 else None,
                "palworld_uid_steam_hex": f"{lines[1].split(': ')[1]}-0000-0000-0000-000000000000" if len(lines) > 1 else None,
                "palworld_uid_nosteam_hex": f"{lines[5].split(': ')[1]}-0000-0000-0000-000000000000" if len(lines) > 5 else None
            }
    except Exception as e: pass
    return None
steam_id_from_local = get_steam_id_from_local()
if steam_id_from_local:
    result = fetch_palworld_uids(steam_id_from_local)
    if result:
        print(f"Your SteamID: {steam_id_from_local}")
        print(f"Your Steam Profile URL: {result['steam_profile_url']}")
        print(f"Your Palworld UID (Steam): {result.get('palworld_uid_steam_hex', 'Not found')}")
        print(f"Your Palworld UID (NoSteam): {result.get('palworld_uid_nosteam_hex', 'Not found')}")
steam_input = input("Enter SteamID (with or without 'steam_' or full URL): ").strip()
if "steamcommunity.com/profiles/" in steam_input:
    steam_input = steam_input.split("steamcommunity.com/profiles/")[1].split("/")[0]
elif steam_input.startswith("steam_"):
    steam_input = steam_input[6:]
result = fetch_palworld_uids(steam_input)
if result:
    print("Palworld UID:", result["palworld_uid_steam_hex"].upper())
    print("NoSteam UID:", result["palworld_uid_nosteam_hex"].upper())