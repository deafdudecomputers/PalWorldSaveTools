import os, subprocess, sys
from pathlib import Path
def set_console_title(title): os.system(f'title {title}')
def setup_environment():
    print("Setting up your environment...")
    os.makedirs("PalWorldSave/Players", exist_ok=True) 
    if not Path("venv").exists():
        subprocess.run(["python", "-m", "venv", "venv"])
    activate_command = ".\\venv\\Scripts\\activate.bat"
    subprocess.run(activate_command, shell=True)    
    subprocess.run(["python", "-m", "pip", "install", "-r", "requirements.txt"])
    print("Dependencies installed.")
def get_versions():
    tools_version = "1.0.14"
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
    print(f"\nv{tools_version} - Working as of v{game_version} Patch\n")
    print("WARNING: ALWAYS BACKUP YOUR SAVES BEFORE USING THIS TOOL!\n")
    print("=" * 80)
def display_menu(tools_version, game_version):
    display_logo()
    print("                     Converting Tools")
    print("=" * 80)
    for i, tool in enumerate(converting_tools, 1):
        print(f"{i}. {tool}")
    print("=" * 80)
    print("                     Management Tools")
    print("=" * 80)
    for i, tool in enumerate(management_tools, len(converting_tools) + 1):
        print(f"{i}. {tool}")
    print("=" * 80)
    print("                     Cleaning Tools")
    print("=" * 80)
    for i, tool in enumerate(cleaning_tools, len(converting_tools) + len(management_tools) + 1):
        print(f"{i}. {tool}")
    print("=" * 80)
    print("                     PalWorldSaveTools")
    print("=" * 80)
    for i, tool in enumerate(pws_tools, len(converting_tools) + len(management_tools) + len(cleaning_tools) + 1):
        print(f"{i}. {tool}")
    print("=" * 80)
def run_tool(choice):
    tool_mapping = {
        1: lambda: subprocess.run(["python", "convert_level_location_finder.py", "json"]),
        2: lambda: subprocess.run(["python", "convert_level_location_finder.py", "sav"]),
        3: lambda: subprocess.run(["python", "convert_players_location_finder.py", "json"]),
        4: lambda: subprocess.run(["python", "convert_players_location_finder.py", "sav"]),
        5: lambda: subprocess.run(["python", "game_pass_save_fix.py"]),
        6: lambda: subprocess.run(["python", "gamepass_save_converter.py"]),
        7: lambda: subprocess.run(["python", "convertids.py"]),
        8: lambda: subprocess.run(["python", "coords.py"]),
        9: lambda: subprocess.run(["python", "slot_injector.py"]),
        10: lambda: subprocess.run(["python", "palworld_save_pal.py"]),
        11: scan_save,
        12: generate_map,
        13: lambda: subprocess.run(["python", "character_transfer.py"]),
        14: lambda: subprocess.run(["python", "delete_inactive_players.py", "players.log"]),
        15: lambda: subprocess.run(["python", "delete_pals_save.py", "players.log"]),
        16: lambda: subprocess.run(["python", "palguard_bases.py"]),
        17: reset_update_tools,
        18: about_tools,
        19: usage_tools,
        20: readme_tools,
        21: sys.exit
    }
    tool_mapping.get(choice, lambda: print("Invalid choice!"))()
def scan_save():
    for file in ["scan_save.log", "players.log", "sort_players.log"]:
        Path(file).unlink(missing_ok=True)
    if Path("Pal Logger").exists():
        subprocess.run(["rmdir", "/s", "/q", "Pal Logger"], shell=True)
    if Path("PalWorldSave/Level.sav").exists():
        subprocess.run(["python", "scan_save.py", "PalWorldSave/Level.sav"])
    else:
        print("Error: PalWorldSave/Level.sav not found!")
def generate_map():
    subprocess.run(["python", "-m", "internal_libs.bases"])
    if Path("updated_worldmap.png").exists():
        print("Opening updated_worldmap.png...")
        subprocess.run(["start", "updated_worldmap.png"], shell=True)
    else:
        print("updated_worldmap.png not found.")
def reset_update_tools():
    subprocess.run(["python", "-m", "ensurepip", "--upgrade"])
    subprocess.run(["git", "init"])
    subprocess.run(["git", "remote", "add", "origin", "https://github.com/deafdudecomputers/PalWorldSaveTools.git"])
    subprocess.run(["git", "fetch", "--all"])
    subprocess.run(["git", "reset", "--hard", "origin/main"])
    subprocess.run(["git", "clean", "-fdx"])
    print("Update complete. All files replaced.")
    os.execv(sys.executable, ['python'] + sys.argv)
    os.system('cls' if os.name == 'nt' else 'clear')
def about_tools():
    display_logo()
    print("PalWorldSaveTools, all in one tool for fixing/transferring/editing/etc PalWorld saves.")
    print("Author: MagicBear and cheahjs")
    print("License: MIT License")
    print("Updated by: Pylar and Techdude")
    print("Map Pictures Provided by: Kozejin")
    print("Testers/Helpers: Lethe and xKillerMaverick")
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
    if readme_path.exists():
        subprocess.run(["start", str(readme_path)], shell=True)
    else:
        print("README.md not found.")
converting_tools = [
    "Convert Level.sav file to Level.json",
    "Convert Level.json file back to Level.sav",
    "Convert Player files to json format",
    "Convert Player files back to sav format",
    "Convert Game Pass Save to Steam Save",
    "Convert Steam Save to Game Pass Save",
    "Convert SteamID",
    "Convert Coordinates"
]
management_tools = [
    "Slot Injector",
    "Modify Save",
    "Scan Save",
    "Generate Map",
    "Transfer Character"
]
cleaning_tools = [
    "Delete Inactive Players Saves",
    "Delete Players Saves by Pals amount",
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
    setup_environment()
    tools_version, game_version = get_versions()
    while True:
        set_console_title(f"PalWorldSaveTools v{tools_version} - Working as of v{game_version}")
        display_menu(tools_version, game_version)
        try:
            choice = int(input("Select what you want to do: "))
            os.system('cls' if os.name == 'nt' else 'clear')
            run_tool(choice)
            input("Press Enter to continue...")
        except ValueError:
            print("Invalid input. Please enter a number.")