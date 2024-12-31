# PalWorldSaveTools: Working as of v0.4.12 patch.

- **Author:** MagicBear and cheahjs 
- **License:** MIT License  
- **Updated by:** Pylar and Techdude  
- **Map Pictures Provided by:** Kozejin 
- **Testers/Helpers:** Lethe

## Prerequisites

1. **Saves that were updated on/after the current patch.**

2. **[Official Python Installation](https://www.python.org/downloads)**
   - Download Python from the official website.
   - Before clicking **Install Now**, **CHECK** the box at the bottom that says:  
     **"Add Python to PATH"** 🟩  
     (*This is what makes Python accessible from the command line!*)  
     ![Add Python to PATH checkbox](https://i.imgur.com/SCJEkdJ.png)

3. **[VS Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)**
   - Download and install Visual Studio Build Tools.
   - During installation, **CHECK** the box that says:  
     **"Desktop development with C++"** 🟩  
     (*This is what makes `cityhash` installable!*)  
     ![CityHash Screenshot](https://i.imgur.com/RZGZ9So.png)


## Current Features:
- **Fast parsing/reading tool**—one of the quickest out there.
- Lists all players/guilds.
- Lists all pals.
- Shows last online time for players.
- Logs players and their relevant information into `players.log`.
- Sorts and deletes players based on level and last online time.
- Logs and sorts players by the number of pals they own.
- Deletes players based on the number of pals.
- Enables double-click functionality for save versions of files.
- Provides a base map view through `bases.cmd`.
- Transfers saves between dedicated server and single/coop world.
- Look up the palworld id via steam id by convertids.

## Transferring between servers/worlds(single/coop):
- Make sure to disable private locks on the "host" chests.

## Gamepass Saves

If you're playing Palworld through Xbox Game Pass, you'll need to extract and convert your save files using the **XGP-save-extractor** and **PalWorldSaveTools**. Follow the steps below to get everything working smoothly.

---

## XGP-save-extractor
- [XGP-save-extractor GitHub Repository](https://github.com/Z1ni/XGP-save-extractor)

---

## Steps

### 1. **Extract the Save Files:**
   - Download and unzip the **XGP-save-extractor**.
   - Run the program, follow the prompts in the command prompt, and it will output a ZIP file containing your Xbox Game Pass Palworld save files.

### 2. **Locate the Save File:**
   - Unzip the exported file.
   - Open the folder, navigate to the nested folder named **`Level`**, and find the file named **`01.sav`**.

### 3. **Rename the Save File:**
   - Rename **`01.sav`** to **`Level.sav`**.

### 4. **Prepare the Save Tools:**
   - Unzip the **PalWorldSaveTools** folder.

### 5. **Move the Save File:**
   - Move the renamed **`Level.sav`** file into the **PalWorldSaveTools** folder.

### 6. **Convert Save to JSON:**
   - Drag **`Level.sav`** onto the **`convert-sav-to-json.cmd`** file.
   - A new file named **`Level.sav.json`** will be created in the same folder.

### 7. **Delete the Original Save:**
   - Delete the **`Level.sav`** file you moved in earlier.

### 8. **Convert JSON Back to Save:**
   - Drag **`Level.sav.json`** onto the **`convert-json-to-sav.cmd`** file.
   - You should now have a newly converted **`Level.sav`** file ready to use.

---

## How to Automatically Delete Player Saves Based on Inactivity:
1. Copy everything from your server (`\Pal\Saved\SaveGames\0\RANDOMSERVERID\`) into the same location within the tool (`PalworldSaveTools\`).
2. Run `fix_save.cmd`.
3. Run `sort_players.cmd` and/or `delete_pals_save.cmd`.
4. Copy the `Players` folder from the tool.
5. Delete the original `Players` folder from the server (`\Pal\Saved\SaveGames\0\RANDOMSERVERID\`).
6. Paste the copied `Players` folder into the server folder.
7. Start the server up.
8. Reboot twice, once to clear the player out of Level.sav. Twice to clear the player out of ram. 
9. Profit?

## Additional Notes:
- **Days:** Tracks players inactive for a specified number of days (e.g., 30 days and older).
- **Level:** Tracks players up to a specified level (e.g., level 30 or lower).
- **Pals:** Deletes players based on the number of pals (e.g., 10 or fewer pals).