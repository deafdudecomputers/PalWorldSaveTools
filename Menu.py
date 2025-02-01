import os, subprocess, sys
from pathlib import Path
RED_FONT = "\033[91m"
BLUE_FONT = "\033[94m"
GREEN_FONT = "\033[92m"
YELLOW_FONT= "\033[93m"
PURPLE_FONT = "\033[95m"
RESET_FONT = "\033[0m"
def set_console_title(title): os.system(f'title {title}') if sys.platform == "win32" else print(f'\033]0;{title}\a', end='', flush=True)
def setup_environment():
    if sys.platform != "win32":
        import resource
        resource.setrlimit(resource.RLIMIT_NOFILE, (65535, 65535))
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"{YELLOW_FONT}Setting up your environment...{RESET_FONT}")
    os.makedirs("PalWorldSave/Players", exist_ok=True)
    if not os.path.exists("venv"): subprocess.run([sys.executable, "-m", "venv", "venv"])
    pip_executable = os.path.join("venv", "Scripts", "pip") if os.name == 'nt' else os.path.join("venv", "bin", "pip")
    subprocess.run([pip_executable, "install", "--no-cache-dir", "-r", "requirements.txt"])
    playwright_browsers_path = os.path.join(os.path.dirname(__file__), "venv", "playwright_browsers")
    os.environ["PLAYWRIGHT_BROWSERS_PATH"] = playwright_browsers_path
    venv_python = os.path.join("venv", "Scripts", "python.exe") if os.name == 'nt' else os.path.join("venv", "bin", "python")
    subprocess.run([venv_python, "-m", "playwright", "install"])
def get_versions():
    tools_version = "1.0.21.r1"
    game_version = "0.4.14"
    return tools_version, game_version
def display_logo():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("=" * 80)
    print(r"""
______     _ _    _            _     _ _____               _____           _     
| ___ \   | | |  | |          | |   | /  ___|             |_   _|         | |    
| |_/ /_ _| | |  | | ___  _ __| | __| \ `--.  __ ___   _____| | ___   ___ | |___ 
|  __/ _` | | |/\| |/ _ \| '__| |/ _` |`--. \/ _` \ \ / / _ \ |/ _ \ / _ \| / __|
| | | (_| | \  /\  / (_) | |  | | (_| /\__/ / (_| |\ V /  __/ | (_) | (_) | \__ \
\_|  \__,_|_|\/  \/ \___/|_|  |_|\__,_\____/ \__,_| \_/ \___\_/\___/ \___/|_|___/
    """)
    print(f"\n{GREEN_FONT}v{tools_version} - Working as of v{game_version} Patch{RESET_FONT}\n")
    print(f"{RED_FONT}WARNING: ALWAYS BACKUP YOUR SAVES BEFORE USING THIS TOOL!{RESET_FONT}\n")
    print(f"{RED_FONT}MAKE SURE TO UPDATE YOUR SAVES ON/AFTER THE v{game_version} PATCH!{RESET_FONT}\n")
    print(f"{RED_FONT}IF YOU DO NOT UPDATE YOUR SAVES, YOU WILL GET ERRORS!{RESET_FONT}\n")
    print("=" * 80)
def display_menu(tools_version, game_version):
    display_logo()
    print(f"                     {BLUE_FONT}Converting Tools{RESET_FONT}")
    print("=" * 80)
    for i, tool in enumerate(converting_tools, 1): print(f"{BLUE_FONT}{i}{RESET_FONT}. {tool}")
    print("=" * 80)
    print(f"                     {GREEN_FONT}Management Tools{RESET_FONT}")
    print("=" * 80)
    for i, tool in enumerate(management_tools, len(converting_tools) + 1): print(f"{GREEN_FONT}{i}{RESET_FONT}. {tool}")
    print("=" * 80)
    print(f"                     {YELLOW_FONT}Cleaning Tools{RESET_FONT}")
    print("=" * 80)
    for i, tool in enumerate(cleaning_tools, len(converting_tools) + len(management_tools) + 1): print(f"{YELLOW_FONT}{i}{RESET_FONT}. {tool}")
    print("=" * 80)
    print(f"                     {PURPLE_FONT}PalWorldSaveTools{RESET_FONT}")
    print("=" * 80)
    for i, tool in enumerate(pws_tools, len(converting_tools) + len(management_tools) + len(cleaning_tools) + 1): print(f"{PURPLE_FONT}{i}{RESET_FONT}. {tool}")
    print("=" * 80)
def run_tool(choice):
    python_exe = os.path.join("venv", "Scripts", "python.exe") if os.name == 'nt' else os.path.join("venv", "bin", "python")
    assets_folder = os.path.join(os.path.dirname(__file__), "Assets")
    tool_mapping = {
        1: lambda: subprocess.run([python_exe, os.path.join(assets_folder, "convert_level_location_finder.py"), "json"]),
        2: lambda: subprocess.run([python_exe, os.path.join(assets_folder, "convert_level_location_finder.py"), "sav"]),
        3: lambda: subprocess.run([python_exe, os.path.join(assets_folder, "convert_players_location_finder.py"), "json"]),
        4: lambda: subprocess.run([python_exe, os.path.join(assets_folder, "convert_players_location_finder.py"), "sav"]),
        5: lambda: subprocess.run([python_exe, os.path.join(assets_folder, "game_pass_save_fix.py")]),
        6: lambda: subprocess.run([python_exe, os.path.join(assets_folder, "convertids.py")]),
        7: lambda: subprocess.run([python_exe, os.path.join(assets_folder, "coords.py")]),
        8: lambda: subprocess.run([python_exe, os.path.join(assets_folder, "slot_injector.py")]),
        9: lambda: subprocess.run([python_exe, os.path.join(assets_folder, "palworld_save_pal.py")]),
        10: scan_save,
        11: generate_map,
        12: lambda: subprocess.run([python_exe, os.path.join(assets_folder, "character_transfer.py")]),
        13: lambda: subprocess.run([python_exe, os.path.join(assets_folder, "fix_host_save.py")]),
        14: lambda: subprocess.run([python_exe, os.path.join(assets_folder, "restore_map.py")]),
        15: lambda: subprocess.run([python_exe, os.path.join(assets_folder, "delete_inactive_players.py"), "players.log"]),
        16: lambda: subprocess.run([python_exe, os.path.join(assets_folder, "delete_pals_save.py"), "players.log"]),
        17: lambda: subprocess.run([python_exe, os.path.join(assets_folder, "palguard_bases.py")]),
        18: reset_update_tools,
        19: about_tools,
        20: usage_tools,
        21: readme_tools,
        22: sys.exit
    }
    tool_mapping.get(choice, lambda: print("Invalid choice!"))()
def scan_save():
    python_exe = os.path.join("venv", "Scripts", "python.exe") if os.name == 'nt' else os.path.join("venv", "bin", "python")
    for file in ["scan_save.log", "players.log", "sort_players.log"]: Path(file).unlink(missing_ok=True)
    if Path("Pal Logger").exists(): subprocess.run(["rmdir", "/s", "/q", "Pal Logger"], shell=True)
    if Path("PalWorldSave/Level.sav").exists(): subprocess.run([python_exe, os.path.join("Assets", "scan_save.py"), "PalWorldSave/Level.sav"])
    else: print(f"{RED_FONT}Error: PalWorldSave/Level.sav not found!{RESET_FONT}")
def generate_map():
    python_exe = os.path.join("venv", "Scripts", "python.exe") if os.name == 'nt' else os.path.join("venv", "bin", "python")
    subprocess.run([python_exe, "-m", "Assets.bases"])
    if Path("updated_worldmap.png").exists():
        print(f"{GREEN_FONT}Opening updated_worldmap.png...{RESET_FONT}")
        subprocess.run(["start", "updated_worldmap.png"], shell=True)
    else: print(f"{RED_FONT}updated_worldmap.png not found.{RESET_FONT}")
def reset_update_tools():
    repo_url = "https://github.com/deafdudecomputers/PalWorldSaveTools.git"
    python_exe = os.path.join("venv", "Scripts", "python.exe") if os.name == 'nt' else os.path.join("venv", "bin", "python")
    print(f"{GREEN_FONT}Resetting/Updating PalWorldSaveTools...{RESET_FONT}")
    subprocess.run([python_exe, "-m", "ensurepip", "--upgrade"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(["git", "init"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(["git", "remote", "remove", "origin"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(["git", "remote", "add", "origin", repo_url], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"{GREEN_FONT}Replacing all files in the current directory with the latest from GitHub...{RESET_FONT}")
    subprocess.run(["git", "fetch", "--all"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(["git", "reset", "--hard", "origin/main"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(["git", "clean", "-fdx"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if os.name == 'nt': subprocess.run(["cmd", "/c", "rmdir", "/s", "/q", ".git"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    else: subprocess.run(["rm", "-rf", ".git"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"{GREEN_FONT}Update complete. All files have been replaced.{RESET_FONT}")
    input(f"{GREEN_FONT}Press Enter to continue...{RESET_FONT}")
    setup_environment()
def about_tools():
    display_logo()
    print("PalWorldSaveTools, all in one tool for fixing/transferring/editing/etc PalWorld saves.")
    print("Author: MagicBear and cheahjs")
    print("License: MIT License")
    print("Updated by: Pylar and Techdude")
    print("Map Pictures Provided by: Kozejin")
    print("Testers/Helpers: Lethe, rcioletti and xKillerMaverick")
    print("The UI was made by xKillerMaverick")
    print("Contact me on Discord: Pylar1991")
def usage_tools():
    display_logo()
    print("Some options may require you to use PalWorldSave folder, so place your saves in that folder.")
    print("If you encounter some errors, make sure to run Scan Save first.")
    print("Then repeat the previous option to see if it fixes the previous error.")
    print("If everything else fails, you may contact me on Discord: Pylar1991")
    print("Or raise an issue on my github: https://github.com/deafdudecomputers/PalWorldSaveTools")
def readme_tools():
    display_logo()
    readme_path = Path("README.md")
    if readme_path.exists(): subprocess.run(["start", str(readme_path)], shell=True)
    else: print(f"{RED_FONT}README.md not found.{RESET_FONT}")
converting_tools = [
    "Convert Level.sav file to Level.json",
    "Convert Level.json file back to Level.sav",
    "Convert Player files to json format",
    "Convert Player files back to sav format",
    "Convert Game Pass Save to Steam Save",
    "Convert SteamID",
    "Convert Coordinates"
]
management_tools = [
    "Slot Injector",
    "Modify Save",
    "Scan Save",
    "Generate Map",
    "Character Transfer",
    "Fix Host Save",
    "Restore Map"
]
cleaning_tools = [
    "Delete Inactive Players Saves",
    "Delete Saves by Pals Count",
    "Generate palguard killnearestbase commands"
]
pws_tools = [
    "Reset/Update PalWorldSaveTools",
    "About PalWorldSaveTools",
    "PalWorldSaveTools Usage",
    "PalWorldSaveTools Readme",
    "Exit"
]
if __name__ == "__main__":
    tools_version, game_version = get_versions()
    set_console_title(f"PalWorldSaveTools v{tools_version}")
    setup_environment()
    os.system('cls' if os.name == 'nt' else 'clear')
    if len(sys.argv) > 1:
        try:
            choice = int(sys.argv[1])
            run_tool(choice)
            tools_version, game_version = get_versions()
            set_console_title(f"PalWorldSaveTools v{tools_version}")
        except ValueError:
            print(f"{RED_FONT}Invalid argument. Please pass a valid number.{RESET_FONT}")
    else:
        while True:
            tools_version, game_version = get_versions()
            set_console_title(f"PalWorldSaveTools v{tools_version}")
            display_menu(tools_version, game_version)
            try:
                choice = int(input(f"{GREEN_FONT}Select what you want to do: {RESET_FONT}"))
                os.system('cls' if os.name == 'nt' else 'clear')
                run_tool(choice)
                input(f"{GREEN_FONT}Press Enter to continue...{RESET_FONT}")
            except ValueError:
                print(f"{RED_FONT}Invalid input. Please enter a number.{RESET_FONT}")