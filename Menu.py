import os
import subprocess
import sys
from pathlib import Path

from .constants import (
    ABOUT_TXT,
    TOOLS_VERSION,
    GAME_VERSION,
    LINE_SEP,
    LOGO,
    converting_tools,
    management_tools,
    cleaning_tools,
    pws_tools
)

PYBIN = ""
PIPBIN = ""

def get_py_binary(bin_name="python"):
    """
    Get the path to the Python executable within a virtual environment.

    This function constructs the path to the Python executable based on the
    operating system and the provided binary name. It assumes the executable
    is located within a virtual environment directory named 'venv'.

    Args:
        bin_name (str): The name of the Python binary. Defaults to "python".
                        If the name ends with ".exe", it will be stripped off.

    Returns:
        str: The path to the Python executable within the virtual environment.
    """
    if bin_name.endswith(".exe"):
        bin_name = os.path.splitext(bin_name)[0]
    target_bin = f"{bin_name}.exe" if os.name == "nt" else bin_name
    bin_dir = "Scripts" if os.name == "nt" else "bin"
    return os.path.join("venv", bin_dir, target_bin)

def update_binary_definitions():
    """
    Update the Python binary definitions in the global scope.

    This function updates the global variables PYBIN and PIPBIN with the
    paths to the Python and Pip executables respectively. It is useful when
    the virtual environment is recreated or the script is run in a different
    environment.
    """
    global PYBIN, PIPBIN # pylint: disable=global-statement
    PYBIN = get_py_binary()
    PIPBIN = get_py_binary("pip")

def clear_screen():
    """
    Clear the console screen based on the operating system.

    This function clears the console screen based on the operating system
    using the appropriate command for the platform.
    """
    os.system("cls" if os.name == "nt" else "clear")

def set_console_title(title):
    """
    Sets the console window title.

    Parameters:
    title (str): The title to set for the console window.

    Behavior:
    - On Windows (win32), it uses the `os.system` call to set the console title.
    - On other platforms, it uses an ANSI escape sequence to set the console title.

    Note:
    This function requires the `sys` and `os` modules to be imported.
    """
    if sys.platform == "win32":
        os.system(f"title {title}")
        return
    print(f"\033]0;{title}\a", end="", flush=True)


def setup_environment():
    """
    Sets up the environment for the application.

    - If the platform is not Windows, it sets the file descriptor limit to 65535.
    - Clears the screen.
    - Prints a message indicating the environment setup.
    - Creates necessary directories if they do not exist.
    - Creates a virtual environment if it does not exist.
    - Installs required packages from requirements.txt.

    Raises:
        OSError: If there is an issue creating directories or running subprocesses.
    """
    if sys.platform != "win32":
        import resource  # pylint: disable=import-error,import-outside-toplevel
        resource.setrlimit(resource.RLIMIT_NOFILE, (65535, 65535))
    clear_screen()
    print("Setting up your environment...")
    os.makedirs("PalWorldSave/Players", exist_ok=True)
    if not os.path.exists("venv"):
        subprocess.run([sys.executable, "-m", "venv", "venv"], check=False)
    subprocess.run([PIPBIN, "install", "-r", "requirements.txt"], check=False)


def get_versions():

    """
    Returns the current versions of the tools and the game.

    Returns:
        tuple: A tuple containing the tools version and the game version.
    """
    return TOOLS_VERSION, GAME_VERSION


def display_logo():
    """
    Clears the screen and displays the logo along with version information and warnings.

    This function performs the following actions:
    1. Clears the screen.
    2. Prints a line separator.
    3. Prints the logo.
    4. Prints the tool's version and the game's version patch information.
    5. Displays a warning to backup saves before using the tool.
    6. Displays a warning to update saves after the specified game version patch.
    7. Displays a warning about potential errors if saves are not updated.

    Note:
        The function uses ANSI escape codes to print warnings in red color.
    """
    clear_screen()
    print(LINE_SEP)
    print(LOGO)
    print(f"\nv{TOOLS_VERSION} - Working as of v{GAME_VERSION} Patch\n")
    print("\033[91mWARNING: ALWAYS BACKUP YOUR SAVES BEFORE USING THIS TOOL!\n\033[0m")
    print(
        f"\033[91mMAKE SURE TO UPDATE YOUR SAVES ON/AFTER THE v{GAME_VERSION} PATCH!\n\033[0m"
    )
    print("\033[91mIF YOU DO NOT UPDATE YOUR SAVES, YOU WILL GET ERRORS!\n\033[0m")
    print(LINE_SEP)


def display_menu():
    """
    Displays the main menu for the PalWorldSaveTools application.

    The menu is divided into several sections, each containing a list of tools.
    The sections include:
    - Converting Tools
    - Management Tools
    - Cleaning Tools
    - PalWorldSaveTools

    Each tool is displayed with an index number for easy selection.
    """
    display_logo()
    sections = [
        ("Converting Tools", converting_tools),
        ("Management Tools", management_tools),
        ("Cleaning Tools", cleaning_tools),
        ("PalWorldSaveTools", pws_tools),
    ]
    index = 1
    for title, tools in sections:
        print(title.rjust(21+len(title)))
        print(LINE_SEP)
        for tool in tools:
            print(f"{index}. {tool}")
            index += 1
        print(LINE_SEP)



def tool_subprocess(command, *args):
    """
    Executes a subprocess command using the specified Python executable.

    Args:
        command (str): The command to be executed.
        *args: Additional arguments to be passed to the command.

    Returns:
        None
    """
    subprocess.run([PYBIN, command, *args], check=False)

def quiet_subprocess(*commands):
    """
    Run a subprocess command quietly, suppressing stdout and stderr.

    Args:
        *commands: Variable length argument list representing the command and its arguments to be executed.

    Returns:
        None
    """
    subprocess.run(
        args=commands,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False
    )

def run_tool(choice):
    """
    Executes a tool based on the user's choice.

    Parameters:
    choice (int): The number corresponding to the tool to be executed.

    The mapping of choices to tools is as follows:
        1: Convert level location finder (json)
        2: Convert level location finder (sav)
        3: Convert players location finder (json)
        4: Convert players location finder (sav)
        5: Game pass save fix
        6: Convert IDs
        7: Coords
        8: Slot injector
        9: Palworld save pal
        10: Scan save
        11: Generate map
        12: Character transfer
        13: Fix host save
        14: Delete inactive players (players.log)
        15: Delete pals save (players.log)
        16: Palguard bases
        17: Reset update tools
        18: About tools
        19: Usage tools
        20: Readme tools
        21: Exit the program

    If an invalid choice is provided, it prints "Invalid choice!".
    """
    tool_mapping = {
        1: tool_subprocess("convert_level_location_finder.py", "json"),
        2: tool_subprocess("convert_level_location_finder.py", "sav"),
        3: tool_subprocess("convert_players_location_finder.py", "json"),
        4: tool_subprocess("convert_players_location_finder.py", "sav"),
        5: tool_subprocess("game_pass_save_fix.py"),
        6: tool_subprocess("convertids.py"),
        7: tool_subprocess("coords.py"),
        8: tool_subprocess("slot_injector.py"),
        9: tool_subprocess("palworld_save_pal.py"),
        10: scan_save,
        11: generate_map,
        12: tool_subprocess("character_transfer.py"),
        13: tool_subprocess("fix_host_save.py"),
        14: tool_subprocess("delete_inactive_players.py", "players.log"),
        15: tool_subprocess("delete_pals_save.py", "players.log"),
        16: tool_subprocess("palguard_bases.py"),
        17: reset_update_tools,
        18: about_tools,
        19: usage_tools,
        20: readme_tools,
        21: sys.exit,
    }
    tool_mapping.get(choice, lambda: print("Invalid choice!"))()


def scan_save():
    """
    Scans the save files and performs cleanup and logging operations.

    This function performs the following steps:
    1. Deletes the files "scan_save.log", "players.log", and "sort_players.log" if they exist.
    2. Removes the "Pal Logger" directory if it exists.
    3. If the "PalWorldSave/Level.sav" file exists, runs the "scan_save.py" script on it.
    4. Prints an error message if the "PalWorldSave/Level.sav" file is not found.
    """
    for file in ["scan_save.log", "players.log", "sort_players.log"]:
        Path(file).unlink(missing_ok=True)
    if Path("Pal Logger").exists():
        subprocess.run(["rmdir", "/s", "/q", "Pal Logger"], shell=True, check=False)
    if Path("PalWorldSave/Level.sav").exists():
        subprocess.run([PYBIN, "scan_save.py", "PalWorldSave/Level.sav"], check=False)
    else:
        print("Error: PalWorldSave/Level.sav not found!")


def generate_map():
    """
    Generates a map by running an internal library module and attempts to open the resulting image file.

    This function executes a subprocess to run the 'internal_libs.bases' module. After running the module,
    it checks for the existence of the 'updated_worldmap.png' file. If the file exists, it opens the image
    using the default image viewer. If the file does not exist, it prints a message indicating that the file
    was not found.

    Returns:
        None
    """
    subprocess.run([PYBIN, "-m", "internal_libs.bases"], check=False)
    if Path("updated_worldmap.png").exists():
        print("Opening updated_worldmap.png...")
        subprocess.run(["start", "updated_worldmap.png"], shell=True, check=False)
    else:
        print("updated_worldmap.png not found.")


def reset_update_tools():
    """
    Resets and updates the PalWorldSaveTools repository by performing the following steps:
    
    1. Ensures the latest version of pip is installed.
    2. Initializes a new Git repository.
    3. Removes any existing remote named 'origin'.
    4. Adds a new remote pointing to the PalWorldSaveTools GitHub repository.
    5. Fetches all updates from the remote repository.
    6. Resets the local repository to match the latest state of the remote 'main' branch.
    7. Cleans the working directory by removing untracked files and directories.
    8. Deletes the local Git repository to remove any Git-related files.
    9. Sets up the environment and updates binary definitions.
    
    This function is intended to replace all files in the current directory with the latest
    versions from the GitHub repository, effectively resetting the local copy to match the
    remote repository.
    
    Note: This function requires the `quiet_subprocess`, `setup_environment`, and 
    `update_binary_definitions` functions to be defined elsewhere in the code.
    """
    repo_url = "https://github.com/djstompzone/PalWorldSaveTools.git"
    print("Resetting/Updating PalWorldSaveTools...")
    quiet_subprocess([PYBIN, "-m", "ensurepip", "--upgrade"])
    quiet_subprocess(["git", "init"])
    quiet_subprocess(["git", "remote", "remove", "origin"])
    quiet_subprocess(["git", "remote", "add", "origin", repo_url])
    print("Replacing all files in the current directory with the latest from GitHub...")
    quiet_subprocess(["git", "fetch", "--all"])
    quiet_subprocess(["git", "reset", "--hard", "origin/main"])
    quiet_subprocess(["git", "clean", "-fdx"])
    if os.name == "nt":
        quiet_subprocess(["cmd", "/c", "rmdir", "/s", "/q", ".git"])
    else:
        quiet_subprocess(["rm", "-rf", ".git"])
    print("Update complete. All files have been replaced.")
    input("Press Enter to continue...")
    setup_environment()
    update_binary_definitions()


def about_tools():
    """
    Displays the logo and prints the information about the tools.

    This function calls the display_logo() function to show the logo and then
    prints the ABOUT_TXT string which contains information about the tools.
    """
    display_logo()
    print(ABOUT_TXT)

def usage_tools():
    """
    Displays usage instructions and troubleshooting information for the PalWorldSaveTools.

    This function shows the logo and provides the following information:
    - Instructions on using the PalWorldSave folder for certain options.
    - Advice to run the "Scan Save" option if errors are encountered.
    - Steps to repeat the previous option to potentially fix errors.
    - Contact information for further assistance via Discord or GitHub.

    Contact:
    - Discord: Pylar1991
    - GitHub: https://github.com/deafdudecomputers/PalWorldSaveTools
    """
    display_logo()
    print(
        "Some options may require you to use PalWorldSave folder, so place your saves in that folder."
    )
    print("If you encounter some errors, make sure to run Scan Save first.")
    print("Then repeat the previous option to see if it fixes the previous error.")
    print("If everything else fails, you may contact me on Discord: Pylar1991")
    print(
        "Or raise an issue on my github: https://github.com/deafdudecomputers/PalWorldSaveTools"
    )


def readme_tools():
    """
    Displays the logo and attempts to open the README.md file in the default text editor.

    If the README.md file exists in the current directory, it will be opened using the default
    text editor. If the file does not exist, a message will be printed to the console indicating
    that the README.md file was not found.

    Note:
        This function uses the `subprocess.run` method with `shell=True` to open the file, which
        may have security implications. Use with caution.

    Raises:
        None

    Returns:
        None
    """
    display_logo()
    readme_path = Path("README.md")
    if readme_path.exists():
        subprocess.run(["start", str(readme_path)], check=False, shell=True)
    else:
        print("README.md not found.")



def main():
    """
    Main function to run the PalWorldSaveTools menu.

    This function sets the console title, checks for command-line arguments,
    and runs the corresponding tool if a valid argument is provided. If no
    valid argument is provided, it displays the menu and prompts the user
    to select an option. The selected tool is then executed.

    The function handles invalid inputs by displaying appropriate error
    messages and re-displaying the menu.

    Returns:
        None
    """
    set_console_title(f"PalWorldSaveTools v{TOOLS_VERSION}")
    if len(sys.argv) > 1:
        try:
            choice = int(sys.argv[1])
            run_tool(choice)
            return
        except ValueError:
            print("Invalid argument. Please pass a valid number.")
            return
        finally:
            set_console_title(f"PalWorldSaveTools v{TOOLS_VERSION}")
    display_menu()
    try:
        choice = int(input("Select what you want to do: "))
        clear_screen()
        run_tool(choice)
        input("Press Enter to continue...")
        return main()
    except ValueError:
        print("Invalid input. Please enter a number.")
        return main()


if __name__ == "__main__":
    setup_environment()
    clear_screen()
    main()
