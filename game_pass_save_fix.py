from tkinter import messagebox

from PIL import Image

from internal_libs.import_libs import (
    string,
    threading,
    os,
    shutil,
    subprocess,
    zipfile,
    ijson,
    random,
    customtkinter,
)


save_extractor_done = threading.Event()
save_converter_done = threading.Event()
window = customtkinter.CTk()

APP_WIDTH = 400
APP_HEIGHT = 200

def get_save_game_pass(button):
    """
    Handles the process of fetching the save game from Game Pass.

    This function performs the following steps:
    1. Checks if the "./saves" directory exists and removes it if it does.
    2. Prints a message indicating that the save is being fetched from Game Pass.
    3. Destroys the provided button widget.
    4. Creates and places a progress bar widget on the window.
    5. Initializes the progress bar to 0.0.
    6. Starts a thread to check for zip files.
    7. Starts a thread to update the progress bar.

    Args:
        button (customtkinter.CTkButton): The button widget that triggers this function.
    """
    if os.path.exists("./saves"):
        shutil.rmtree("./saves")
    print("Fetching save from Game Pass...")
    button.destroy()
    progressbar = customtkinter.CTkProgressBar(master=window)
    progressbar.place(relx=0.5, rely=0.65, anchor="center")
    progressbar.set(0.0)
    threading.Thread(target=check_for_zip_files, daemon=True).start()
    threading.Thread(target=check_progress, args=(progressbar,), daemon=True).start()


def check_progress(progressbar):
    """
    Checks the progress of the save file extraction and updates the progress bar accordingly.

    If the save file extraction is complete, it sets the progress bar to 50% and starts a new
    thread to convert the save files. If the extraction is not complete, it schedules the
    check_progress function to be called again after 1 second.

    Args:
        progressbar (Progressbar): The progress bar widget to update.
    """
    if save_extractor_done.is_set():
        progressbar.set(0.5)
        print("Attempting to convert the save files...")
        threading.Thread(
            target=convert_save_files, args=(progressbar,), daemon=True
        ).start()
    else:
        window.after(1000, check_progress, progressbar)


def check_for_zip_files():
    """
    Checks for the presence of zip files in the current directory.

    If no zip files are found, it prints a message indicating that zip files
    are being fetched from the local directory and starts a new thread to run
    the save extractor.

    If zip files are found, it processes the zip files.
    """
    if not find_zip_files("./"):
        print("Fetching zip files from local directory...")
        threading.Thread(target=run_save_extractor, daemon=True).start()
    else:
        process_zip_files()


def process_zip_files():
    """
    Processes zip files in the current directory and extracts the first found zip file into the './saves' directory.

    This function performs the following steps:
    1. Checks if the './saves' folder is empty.
    2. If the folder is empty, it searches for zip files in the current directory.
    3. If a zip file is found, it extracts the first zip file into the './saves' directory.
    4. Sets a flag indicating that the save extraction is done.
    5. If no zip files are found, it prints an error message and quits the application.

    Note:
        - This function assumes the existence of the following helper functions:
            - is_folder_empty(folder_path): Checks if the specified folder is empty.
            - find_zip_files(directory): Finds and returns a list of zip files in the specified directory.
            - unzip_file(zip_file_path, extract_to_path): Extracts the specified zip file to the specified directory.
        - This function also assumes the existence of the following variables:
            - save_extractor_done: A threading event or similar flag to indicate the completion of save extraction.
            - window: A reference to the application window that can be quit.

    Raises:
        SystemExit: If no zip files are found and the application needs to quit.
    """
    if is_folder_empty("./saves"):
        zip_files = find_zip_files("./")
        print(zip_files)
        if zip_files:
            unzip_file(zip_files[0], "./saves")
            save_extractor_done.set()
        else:
            print(
                "No save files found on XGP please reinstall the game on XGP and try again"
            )
            window.quit()


def convert_save_files(progressbar):
    """
    Converts save files from a specified directory and updates a combobox with the converted save names.

    Args:
        progressbar: A progress bar widget that will be destroyed after the conversion process.

    Returns:
        None

    The function performs the following steps:
    1. Lists all folders in the "./saves" directory.
    2. If no save folders are found, prints a message and returns.
    3. Iterates through each save folder, converts the save file to JSON format, and appends the converted name to a list.
    4. Updates a combobox with the list of converted save names.
    5. Destroys the progress bar widget.
    6. Prints a message prompting the user to choose a save to convert.
    """
    save_folders = list_folders_in_directory("./saves")
    if not save_folders:
        print("No save files found")
        return
    save_list = list(filter(None, [
        convert_sav_to_json(name) for name in save_folders
    ]))
    update_combobox(save_list)
    progressbar.destroy()
    print("Choose a save to convert:")


def update_combobox(save_list):
    """
    Updates the combobox with the provided list of save files and sets up a button to convert the selected save.

    Args:
        save_list (list): A list of save file names to populate the combobox.

    Returns:
        None
    """
    if not save_list:
        return

    combobox = customtkinter.CTkComboBox(
        master=window, values=save_list, width=320, font=("Arial", 14)
    )
    combobox.place(relx=0.5, rely=0.5, anchor="center")
    combobox.set("Choose a save to convert:")
    button = customtkinter.CTkButton(
        window,
        width=200,
        text="Convert Save",
        command=lambda: convert_json_to_sav(combobox.get()),
    )
    button.place(relx=0.5, rely=0.8, anchor="center")


def run_save_extractor():
    """
    Executes the save extraction process by running an external Python script.

    This function determines the appropriate Python executable based on the operating system,
    constructs the command to run the `xgp_save_extract.py` script, and executes it. If the
    command runs successfully, it proceeds to process the extracted zip files. If there is an
    error during the command execution, it catches the exception and prints an error message.

    Returns:
        None
    """
    python_exe = (
        os.path.join("venv", "Scripts", "python.exe")
        if os.name == "nt"
        else os.path.join("venv", "bin", "python")
    )
    command = [python_exe, "./xgp_save_extract.py", "./"]
    try:
        subprocess.run(command, check=True)
        print("Command executed successfully")
        process_zip_files()
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")
        return None


def list_folders_in_directory(directory):
    """
    Lists all folders in the specified directory.

    If the directory does not exist, it will be created.

    Args:
        directory (str): The path to the directory to list folders from.

    Returns:
        list: A list of folder names in the specified directory.

    Raises:
        FileNotFoundError: If the directory does not exist.
        PermissionError: If there is no permission to access the directory.
    """
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"Directory {directory} created.")
        all_items = os.listdir(directory)
        return [
            item for item in all_items if os.path.isdir(os.path.join(directory, item))
        ]
    except FileNotFoundError:
        print(f"The directory {directory} does not exist.")
        return []
    except PermissionError:
        print(f"You don't have permission to access {directory}.")
        return []


def find_key_in_json(file_path, target_key):
    """
    Searches for a specific key in a JSON file and returns its value.

    Args:
        file_path (str): The path to the JSON file.
        target_key (str): The key to search for in the JSON file.

    Returns:
        The value associated with the target key if found, otherwise False.
        If the file is not found or the JSON is incomplete/invalid, returns False.

    Raises:
        FileNotFoundError: If the file at the specified path does not exist.
        ijson.common.IncompleteJSONError: If the JSON in the file is incomplete or invalid.
    """
    print("Now loading the json...")
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            parser = ijson.parse(f)
            value = None
            for _prefix, event, val in parser:
                if event == "map_key" and val == target_key:
                    _prefix, event, value = next(parser)
                    return value
            return value
    except FileNotFoundError:
        print(f"Error: File not found at path: {file_path}")
        return False
    except ijson.common.IncompleteJSONError:
        print(f"Error: Incomplete or invalid JSON in file: {file_path}")
        return False
    return False


def is_folder_empty(directory):
    """
    Checks if a given directory is empty. If the directory does not exist, it creates the directory.

    Args:
        directory (str): The path to the directory to check.

    Returns:
        bool: True if the directory is empty, False otherwise.

    Exceptions:
        FileNotFoundError: If the directory does not exist and cannot be created.
        PermissionError: If there is no permission to access the directory.
    """
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"Directory {directory} created.")
        all_items = os.listdir(directory)
        return len(all_items) == 0
    except FileNotFoundError:
        print(f"The directory {directory} does not exist.")
        return False
    except PermissionError:
        print(f"You don't have permission to access {directory}.")
        return False


def find_zip_files(directory):
    """
    Finds and returns a list of valid zip files in the specified directory.

    This function searches the given directory for files that have a ".zip"
    extension and start with "palworld_". It then checks if each found zip
    file is valid using the `is_valid_zip` function. If the directory does
    not exist, it prints an error message.

    Args:
        directory (str): The path to the directory to search for zip files.

    Returns:
        list: A list of valid zip file names found in the directory.
    """
    zip_files = []
    if os.path.exists(directory):
        for filename in os.listdir(directory):
            if filename.endswith(".zip") and filename.startswith("palworld_"):
                zip_file_path = os.path.join(directory, filename)
                if is_valid_zip(zip_file_path):
                    zip_files.append(filename)
    else:
        print(f"Directory {directory} does not exist.")
    return zip_files


def is_valid_zip(zip_file_path):
    """
    Checks if the given file path points to a valid ZIP file.

    Args:
        zip_file_path (str): The file path to the ZIP file to be checked.

    Returns:
        bool: True if the file is a valid ZIP file, False otherwise.
    """
    try:
        with zipfile.ZipFile(zip_file_path, "r") as zip_ref:
            zip_ref.testzip()
        return True
    except zipfile.BadZipFile:
        return False


def unzip_file(zip_file_path, extract_to_folder):
    """
    Unzips the specified zip file to the given folder.

    Args:
        zip_file_path (str): The path to the zip file to be extracted.
        extract_to_folder (str): The directory where the contents of the zip file will be extracted.

    Returns:
        None
    """
    print(f"Unzipping {zip_file_path} to {extract_to_folder}...")
    os.makedirs(extract_to_folder, exist_ok=True)
    with zipfile.ZipFile(zip_file_path, "r") as zip_ref:
        zip_ref.extractall(extract_to_folder)
        print(f"Extracted all files to {extract_to_folder}")


def convert_sav_to_json(save_name):
    """
    Converts a save file to JSON format and searches for a specific key in the JSON file.

    Args:
        save_name (str): The name of the save directory.

    Returns:
        str: A string containing the found key value and the save name if successful.
        None: If the save file does not exist or the conversion process fails.

    Raises:
        subprocess.CalledProcessError: If the subprocess running the conversion script fails.
    """
    save_path = f"./saves/{save_name}/Level/01.sav"
    if not os.path.exists(save_path):
        return None
    python_exe = (
        os.path.join("venv", "Scripts", "python.exe")
        if os.name == "nt"
        else os.path.join("venv", "bin", "python")
    )
    command = [python_exe, "./convert.py", save_path]
    try:
        subprocess.run(command, check=True)
        json_file_path = f"./saves/{save_name}/Level/01.sav.json"
        key_found = find_key_in_json(json_file_path, "player_name")
        return f"{key_found} - {save_name}"
    except subprocess.CalledProcessError:
        return None


def convert_json_to_sav(save_name):
    """
    Converts a JSON save file to a .sav file and moves it to the Steam save directory.

    Args:
        save_name (str): The name of the save file to be converted. The function extracts the relevant part of the save name after the first hyphen.

    Prints:
        The extracted save name.
        A message indicating the start of the conversion process.
        A message indicating successful execution of the command.
        A message indicating the deletion of the JSON file.

    Raises:
        subprocess.CalledProcessError: If the command execution fails.

    Side Effects:
        Executes a subprocess command to convert the JSON file to a .sav file.
        Deletes the original JSON file after conversion.
        Calls the move_save_steam function to move the converted save file to the Steam save directory.
    """
    save_name = save_name[save_name.find("-") + 2 :]
    print(save_name)
    print(f"Converting JSON file to .sav: {save_name}")
    python_exe = (
        os.path.join("venv", "Scripts", "python.exe")
        if os.name == "nt"
        else os.path.join("venv", "bin", "python")
    )
    command = [
        python_exe,
        "./convert.py",
        f"./saves/{save_name}/Level/01.sav.json",
        "--output",
        f"./saves/{save_name}/Level.sav",
    ]
    try:
        subprocess.run(command, check=True)
        print("Command executed successfully")
        os.remove(f"./saves/{save_name}/Level/01.sav.json")
        print(f"Deleted JSON file: ./saves/{save_name}/Level/01.sav.json")
        move_save_steam(save_name)
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")


def generate_random_name(length=32):
    """
    Generates a random string of the specified length consisting of uppercase letters and digits.

    Args:
        length (int): The length of the generated string. Default is 32.

    Returns:
        str: A randomly generated string of the specified length.
    """
    return "".join(random.choices(string.ascii_uppercase + string.digits, k=length))


def move_save_steam(save_name):
    """
    Moves a save file to both Steam and GamePassSave directories.

    This function performs the following steps:
    1. Checks if the SaveGames directory exists in the local app data path.
    2. Identifies the target folder within the SaveGames directory.
    3. Copies the save file from the source folder to the Steam target folder.
    4. Copies the save file from the source folder to the GamePassSave directory.
    5. Displays success or error messages based on the operation outcome.
    6. Deletes the original saves directory after copying.

    Args:
        save_name (str): The name of the save file to be moved.

    Raises:
        FileNotFoundError: If the SaveGames directory or subdirectories do not exist.
        OSError: If there is an error copying the save folder.
        Exception: For any other unexpected errors.
    """
    print("Moving save file to Steam and GamePassSave...")
    local_app_data_path = os.path.expandvars(r"%localappdata%\Pal\Saved\SaveGames")
    try:
        if not os.path.exists(local_app_data_path):
            raise FileNotFoundError(
                f"SaveGames directory does not exist at {local_app_data_path}"
            )
        subdirs = [
            d
            for d in os.listdir(local_app_data_path)
            if os.path.isdir(os.path.join(local_app_data_path, d))
        ]
        if not subdirs:
            raise FileNotFoundError(f"No subdirectories found in {local_app_data_path}")
        target_folder = os.path.join(local_app_data_path, subdirs[0])
        print(f"Detected Steam target folder: {target_folder}")
        source_folder = os.path.join("./saves", save_name)

        def ignore_folders(_, names):
            return {
                name for name in names if name in {"Level", "Slot1", "Slot2", "Slot3"}
            }

        new_name = generate_random_name()
        new_target_folder = target_folder + "/" + save_name
        if os.path.exists(new_target_folder):
            print(f"Original folder: {new_target_folder}")
            new_target_folder = target_folder + "/" + new_name
            print(f"Folder already exists in Steam. Renaming to: {new_target_folder}")
        shutil.copytree(
            source_folder, new_target_folder, dirs_exist_ok=True, ignore=ignore_folders
        )
        print(f"Save folder copied to Steam at {new_target_folder}")
        game_pass_save_path = os.path.join(os.getcwd(), "GamePassSave")
        if not os.path.exists(game_pass_save_path):
            os.makedirs(game_pass_save_path)
        new_gamepass_target_folder = os.path.join(game_pass_save_path, new_name)
        shutil.copytree(
            source_folder,
            new_gamepass_target_folder,
            dirs_exist_ok=True,
            ignore=ignore_folders,
        )
        print(f"Save folder copied to GamePassSave at {new_gamepass_target_folder}")
        messagebox.showinfo(
            "Success",
            "Your save is migrated to Steam. You may go ahead and open Steam PalWorld.",
        )
        shutil.rmtree("./saves")
        window.quit()
    except OSError as e:
        print(f"Error copying save folder: {e}")
        messagebox.showerror("Error", f"Failed to copy the save folder: {e}")
    except Exception as e: # pylint: disable=broad-exception-caught
        print(f"An unexpected {e.__class__.__name__} occurred: {e}")
        messagebox.showerror("Error", f"Unexpected {e.__class__.__name__} occurred: {e}")

def main():
    """
    Initializes and runs the main window for the PalWorld Save Converter application.

    This function sets up the main window with a title, icon, and geometry based on the screen size.
    It creates an overlay frame and adds labels with images for Xbox Game Pass and Steam.
    It also adds a button to get saves from the Game Pass, which triggers the `get_save_game_pass` function.

    The function uses the `customtkinter` library for custom widgets and the `Pillow` library for image handling.
    """
    window.title("PalWorld Save Converter")
    window.iconbitmap("./internal_libs/pal.ico")
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width // 2) - (APP_WIDTH // 2)
    y = (screen_height // 2) - (APP_HEIGHT // 2)
    window.geometry(f"{APP_WIDTH}x{APP_HEIGHT}+{x}+{y}")
    overlay_frame = customtkinter.CTkFrame(window, fg_color="transparent")
    overlay_frame.place(relx=0.5, rely=0.1, anchor="n")
    xgp = customtkinter.CTkImage(
        dark_image=Image.open("./internal_libs/xgp.png"), size=(80, 40)
    )
    steam = customtkinter.CTkImage(
        dark_image=Image.open("./internal_libs/steam.png"), size=(30, 30)
    )
    label = customtkinter.CTkLabel(overlay_frame, image=xgp, text="")
    label.pack(side="left", padx=10)
    label = customtkinter.CTkLabel(overlay_frame, image=steam, text="")
    label.pack(side="left", padx=10)
    get_saves_button = customtkinter.CTkButton(
        master=window,
        width=200,
        text="Get Saves",
        command=lambda: get_save_game_pass(get_saves_button),
    )
    get_saves_button.place(relx=0.5, rely=0.65, anchor="center")
    window.mainloop()

if __name__ == "__main__":
    main()
    