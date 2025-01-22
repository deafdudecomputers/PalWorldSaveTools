```
______     _ _    _            _     _ _____               _____           _     
| ___ \   | | |  | |          | |   | /  ___|             |_   _|         | |    
| |_/ /_ _| | |  | | ___  _ __| | __| \ `--.  __ ___   _____| | ___   ___ | |___ 
|  __/ _` | | |/\| |/ _ \| '__| |/ _` |`--. \/ _` \ \ / / _ \ |/ _ \ / _ \| / __|
| | | (_| | \  /\  / (_) | |  | | (_| /\__/ / (_| |\ V /  __/ | (_) | (_) | \__ \
\_|  \__,_|_|\/  \/ \___/|_|  |_|\__,_\____/ \__,_| \_/ \___\_/\___/ \___/|_|___/
```
---

# Working as of v0.4.13 Patch

- **Author:** MagicBear and cheahjs  
- **License:** MIT License  
- **Updated by:** Pylar and Techdude  
- **Map Pictures Provided by:** Kozejin  
- **Testers/Helpers:** Lethe and xKillerMaverick  
- **Contact me on Discord:** Pylar1991

---

## Prerequisites

### 1. **Updated Saves**
- Ensure your saves were updated on/after the current patch.

### 2. **[Python Installation](https://www.python.org/downloads)**
- Download Python from the official website.  
- Before clicking **Install Now**, **CHECK** the box at the bottom that says:  
  **"Add Python to PATH"** 🟩  
  (*This ensures Python is accessible from the command line!*)  
  ![Add Python to PATH checkbox](https://i.imgur.com/SCJEkdJ.png)

### 3. **[Visual Studio Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)**
- Download and install Visual Studio Build Tools.  
- During installation, **CHECK** the box that says:  
  **"Desktop development with C++"** 🟩  
  (*This allows the `cityhash` library to install!*)  
  ![CityHash Screenshot](https://i.imgur.com/RZGZ9So.png)

---

## Features

- **Fast parsing/reading** tool—one of the quickest available.  
- Lists all players/guilds.  
- Lists all pals and their details.  
- Displays last online time for players.  
- Logs players and their data into `players.log`.  
- Sorts and deletes players based on level and inactivity.  
- Logs and sorts players by the number of pals owned.  
- Deletes players with fewer than a specified number of pals.  
- Includes double-click functionality for file save versions.  
- Provides a **base map view**.
- Provides automated killnearestbase commands to be used with palguard for inactive bases.
- Transfers saves between dedicated servers and single/coop worlds.  
- Includes Steam ID conversion.
- Includes coords conversion.  

---

## Transferring Saves Between Servers/Worlds

- Ensure you disable private locks on the "source" chests before transferring saves.

---

## Gamepass Saves

If you're playing Palworld through Xbox Game Pass, you must extract and convert your save files using the **XGP-save-extractor** and **PalWorldSaveTools**. Follow these steps:

### [XGP-save-extractor GitHub Repository](https://github.com/Z1ni/XGP-save-extractor)

### Steps

1. **Extract the Save Files**  
   - Download and unzip the **XGP-save-extractor**.  
   - Run the program, follow the prompts in the command prompt, and it will output a ZIP file containing your Xbox Game Pass Palworld save files.

2. **Locate the Save File**  
   - Unzip the exported file.  
   - Navigate to the nested folder named `Level` and locate the file named `01.sav`.

3. **Rename the Save File**  
   - Rename `01.sav` to `Level.sav`.

4. **Prepare the Save Tools**  
   - Unzip the **PalWorldSaveTools** folder.

5. **Move the Save File**  
   - Move the renamed `Level.sav` file into the **PalWorldSave** folder.

6. **Convert Save to JSON**  
   - Select Convert Level.sav file to Level.json.
   - A new file named `Level.sav.json` will be created in the same folder.

7. **Delete the Original Save**  
   - Delete the `Level.sav` file you moved earlier.

8. **Convert JSON Back to Save**  
   - Select Convert Level.json file back to Level.sav.  
   - You should now have a newly converted `Level.sav` file ready to use.

---

## Automatically Delete Player Saves Based on Inactivity

Follow these steps to delete inactive players based on your criteria (e.g., inactivity, level, or number of pals):

1. Copy all files from your server (`\Pal\Saved\SaveGames\0\RANDOMSERVERID\`) to the same location within the tool (`PalWorldSave`).  
2. Select Delete Inactive Players Saves.
3. Input your desired requirements, then let it finish.  
4. Copy the `Players` folder from the `PalWorldSave` folder.  
5. Delete the original `Players` folder from the server (`\Pal\Saved\SaveGames\0\RANDOMSERVERID\`).  
6. Paste the copied `Players` folder into the server folder.  
7. Restart the server:  
   - Reboot once to clear the player from `Level.sav`.  
   - Reboot a second time to clear the player from RAM.  
8. Profit?  

---

## Steps to Restore Your Map(Fog and icons)

### 1. Find the Old Server/World ID
- **Join your old server/world**.
- Open File Explorer and run the search for:  
  `%localappdata%\Pal\Saved\SaveGames\`
- Look for a folder with a **random ID** (this should be your **Steam ID**).
- Open that folder and **sort the subfolders by the "Last Modified" date**.
- Look for the folder that matches your **old server/world ID** (e.g., `FCC47F5F4DD6AC48D3C0E2B30059973D`). The folder with the most recent modification date is typically the one for your **old server/world**.
- Once you've found the correct folder, **copy** the `LocalData.sav` file from it.

### 2. Find the New Server/World ID
- **Join your new server/world**.
- Go back to the same folder path:  
  `%localappdata%\Pal\Saved\SaveGames\`
- Look for a folder with a **random ID** (this should be your **Steam ID**).
- Open that folder and **sort the subfolders by the "Last Modified" date**.
- Look for the folder that matches your **new server/world ID**.
- Once you've found the correct folder, **paste** the `LocalData.sav` file from the old server/world ID into this folder.
- If the `LocalData.sav` file already exists in the new folder, **confirm the overwrite** when prompted to replace the existing file.

### 3. Restore Your Map
- Now, go into your **new server/world**, and your map should be restored with the old world data.

Done! Your map is back in your **new server/world**!