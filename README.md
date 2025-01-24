```
______     _ _    _            _     _ _____               _____           _     
| ___ \   | | |  | |          | |   | /  ___|             |_   _|         | |    
| |_/ /_ _| | |  | | ___  _ __| | __| \ `--.  __ ___   _____| | ___   ___ | |___ 
|  __/ _` | | |/\| |/ _ \| '__| |/ _` |`--. \/ _` \ \ / / _ \ |/ _ \ / _ \| / __|
| | | (_| | \  /\  / (_) | |  | | (_| /\__/ / (_| |\ V /  __/ | (_) | (_) | \__ \
\_|  \__,_|_|\/  \/ \___/|_|  |_|\__,_\____/ \__,_| \_/ \___\_/\___/ \___/|_|___/
```
---

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

## Features:

- **Fast parsing/reading** tool—one of the quickest available.  
- Lists all players/guilds.  
- Lists all pals and their details.  
- Displays last online time for players.  
- Logs players and their data into `players.log`.  
- Sorts and deletes players based on level and inactivity.  
- Logs and sorts players by the number of pals owned.  
- Deletes players with fewer than a specified number of pals.   
- Provides a **base map view**.
- Provides automated killnearestbase commands to be used with palguard for inactive bases.
- Transfers saves between dedicated servers and single/coop worlds.  
- Includes Steam ID conversion.
- Includes coords conversion.  
- Includes GamePass ⇔ Steam conversion.
- Slot injector, a simple tool to increase slots each player can have on world/server. Works with Bigger PalBox mod.

---

## Transferring Saves Between Servers/Worlds:

- Ensure you disable private locks on the "source" chests before transferring saves.

## Automatically Delete Player Saves Based on Inactivity:

Follow these steps to delete inactive players based on your criteria (e.g., inactivity, level, or number of pals):

1. Copy Players folder and Level.sav from your server (`\Pal\Saved\SaveGames\0\RANDOMSERVERID\`) to the (`PalWorldSave`) folder. 
2. Select Scan Save via PalWorldSaveToolsMenu.cmd.
3. Select Delete Inactive Players Saves via PalWorldSaveToolsMenu.cmd.
4. Input your desired requirements, then let it finish.  
5. Copy the `Players` folder from the `PalWorldSave` folder.  
6. Delete the original `Players` folder from the server (`\Pal\Saved\SaveGames\0\RANDOMSERVERID\`).  
7. Paste the copied `Players` folder into the server folder.  
8. Restart the server:  
   - Reboot once to clear the player from `Level.sav`.  
   - Reboot a second time to clear the player from RAM.  
9. Profit?  

---

## Steps to Restore Your Map(Fog and icons):

### 1. Find the Old Server/World ID:
- **Join your old server/world**.
- Open File Explorer and run the search for:  
  `%localappdata%\Pal\Saved\SaveGames\`
- Look for a folder with a **random ID** (this should be your **Steam ID**).
- Open that folder and **sort the subfolders by the "Last Modified" date**.
- Look for the folder that matches your **old server/world ID** (e.g., `FCC47F5F4DD6AC48D3C0E2B30059973D`). The folder with the most recent modification date is typically the one for your **old server/world**.
- Once you've found the correct folder, **copy** the `LocalData.sav` file from it.

### 2. Find the New Server/World ID:
- **Join your new server/world**.
- Go back to the same folder path:  
  `%localappdata%\Pal\Saved\SaveGames\`
- Look for a folder with a **random ID** (this should be your **Steam ID**).
- Open that folder and **sort the subfolders by the "Last Modified" date**.
- Look for the folder that matches your **new server/world ID**.
- Once you've found the correct folder, **paste** the `LocalData.sav` file from the old server/world ID into this folder.
- If the `LocalData.sav` file already exists in the new folder, **confirm the overwrite** when prompted to replace the existing file.

### 3. Restore Your Map
- Now, go into your **new server/world**, and your map should be restored with the old server/world data.

Done! Your map is back in your **new server/world**!

## Where to find the save files:

The save files are usually located at `C:\Users\YOURUSERNAME\AppData\Local\Pal\Saved\SaveGames\YOURSTEAMID\RANDOMID` for co-op saves.
For server saves, go to the dedicated server's file location through steam.
You need at least 4 files to complete the transfer:
```
- The source player character save file in Players folder
- The source world's level.sav file
- The target player character save file in Players folder
- The target world's Level.sav file
```

## How to use Transfer Character:

Let's say we want to transfer the character from a coop world of a friend to our own world.
The friend's world would be the source, our own world the destination.

SaveGames folder of our friend:
```
SaveGames
└── <steam-id>
    └── <source-world-id>
        ├── backup
        ├── Level.sav  ----------  <- The source world save-file
        ├── LevelMeta.sav
        ├── Players
        │   ├── 00000...0001.sav
        │   └── 12345...6789.sav   <- character save-file we want to transfer
        └── WorldOption.sav
```
Our SaveGames folder:
```
SaveGames
└── <steam-id>
    └── <destination-world-id>
        ├── backup
        ├── Level.sav  ----------  <- The target world save-file
        ├── LevelMeta.sav
        ├── Players
        │   ├── 00000...0001.sav   <- the target player-placeholder save-file
        │   └── 98765...4321.sav
        └── WorldOption.sav
```

### Transferring from Host to Server (or vice versa):

1. **Create a New Character**  
   - Use the same `Level.sav` file on the world or server after transferring it.
2. **Wait for Autosave**  
   - Autosave typically happens within 30 seconds. To be safe, wait at least 1 minute. You can trigger autosave by unlocking Fast Travel or picking up items.
3. **Copy the Files**  
   - Copy the `Level.sav` and `Players` folder to a temporary folder.
4. **Use the Transfer Character Tool**  
   - Load the exact same Level.sav for Source and Target.
   - Select the old character as source.
   - Select the new character as target.   
5. **Optional: Keep Old Guild ID**  
   - If you want to keep old bases, tick the option **Keep Old Guild ID After Transfer**.
6. **Start Transfer**  
   - Press **Start Transfer!** You can repeat this for multiple players if needed.
7. **Copy Transferred Files**  
   - Once transferred, copy the `Level.sav` and `Players` folder.
8. **Paste Files into Target Folder**  
   - Paste them into the destination world or server folder.
Enjoy your old character!