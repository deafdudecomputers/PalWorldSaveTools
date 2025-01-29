```
______     _ _    _            _     _ _____               _____           _     
| ___ \   | | |  | |          | |   | /  ___|             |_   _|         | |    
| |_/ /_ _| | |  | | ___  _ __| | __| \ `--.  __ ___   _____| | ___   ___ | |___ 
|  __/ _` | | |/\| |/ _ \| '__| |/ _` |`--. \/ _` \ \ / / _ \ |/ _ \ / _ \| / __|
| | | (_| | \  /\  / (_) | |  | | (_| /\__/ / (_| |\ V /  __/ | (_) | (_) | \__ \
\_|  \__,_|_|\/  \/ \___/|_|  |_|\__,_\____/ \__,_| \_/ \___\_/\___/ \___/|_|___/
```
![image](https://github.com/user-attachments/assets/d9c1579b-54f9-4f4b-aab3-26f333441b77)

---

- **Author:** MagicBear and cheahjs  
- **License:** MIT License  
- **Updated by:** Pylar and Techdude  
- **Map Pictures Provided by:** Kozejin  
- **Testers/Helpers:** Lethe, rcioletti and xKillerMaverick  
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
  
### 4. ***Start Menu.cmd***

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

## Automatically Delete Player Saves Based on Inactivity:

Follow these steps to delete inactive players based on your criteria (e.g., inactivity, level, or number of pals):

1. Copy Players folder and Level.sav from your server (`\Pal\Saved\SaveGames\0\RANDOMSERVERID\`) to the (`PalWorldSave`) folder. 
2. Select Scan Save.
3. Select Delete Inactive Players Saves.
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

### This only applies if you do NOT want to use the "Restore Map" option.

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
- The source player character save in Players folder
- The source world's Level.sav
- The target player character save in Players folder
- The target world's Level.sav
```

## How to use Transfer Character:

⚠️WARNING⚠️: Make sure to disable the private locks on the "source" chests before transferring saves!!!

Let's say we want to transfer the character from a coop world of a friend to our own world.
The friend's world would be the source, our own world the destination.

SaveGames folder of our friend:
```
SaveGames
└── <steam-id>
    └── <source-world-id>
        ├── backup
        ├── Level.sav  ----------  <- The source world save
        ├── LevelMeta.sav
        ├── Players
        │   ├── 00000...0001.sav
        │   └── 12345...6789.sav   <- The source player save
        └── WorldOption.sav
```
Our SaveGames folder:
```
SaveGames
└── <steam-id>
    └── <destination-world-id>
        ├── backup
        ├── Level.sav  ----------  <- The target world save
        ├── LevelMeta.sav
        ├── Players
        │   ├── 00000...0001.sav   <- The target player save
        │   └── 98765...4321.sav
        └── WorldOption.sav
```

### Transferring from Host to Server (or vice versa):

1. **Make a copy of your "host" or "server" saves.**
    - *Solo/Co-op world:*
	    - Open PalWorld game.
		- Load into your world.
		- Open File Explorer and run the search for:  
		  `%localappdata%\Pal\Saved\SaveGames\`
		- Look for a folder with a **random ID** (this should be your **Steam ID**).
		- Open that folder and **sort the subfolders by the "Last Modified" date**.
		- The folder with the most recent modification date is typically the one for your **world**.
		- Open that folder.
		- Copy these: 
			- Level.sav
			- Players folder
			*Optional*
			- LocalData.sav
			- WorldOption.sav
		- Create a new temporary folder.
		- Paste the copied files/folders into that folder.
	- *Dedicated Server:*
		- Open the server save folder:
			- Default installation usually set to this path: `steamapps\common\Palworld\Pal\Saved\SaveGames\0\RANDOMSERVERID\`
		- Copy these:
			- Level.sav
			- Players folder
		- Create a new temporary folder.
		- Paste the copied files/folders into that folder.
2. **Transferring the copied solo/co-op world or server:**
    - *Solo/Co-op world to Server:
		- Start the server up.
		- Wait up to 2 minutes for the auto save.
		- Shut the server down.
		- Copy from Solo/Co-op temporary copied folder.
		- Go into `steamapps\common\Palworld\Pal\Saved\SaveGames\0\RANDOMSERVERID\`
		- Paste the copied files/folders from Solo/Co-op temporary copied folder.
		- Start the server up.
		- Join the server. 
		- Create new character.
		- Wait up to 2 minutes for the auto save after making the character.
		- Shut down the server.
		- Copy the updated files/folders from `steamapps\common\Palworld\Pal\Saved\SaveGames\0\RANDOMSERVERID\`.
		- Create new temporary folder if you desire and paste into that new temporary folder, or simply paste into former temporary folder you created earlier.
	- *Server to solo/co-op world:
		- Copy these from `steamapps\common\Palworld\Pal\Saved\SaveGames\0\RANDOMSERVERID\`:
			- Level.sav
			- Players folder
		- Create new temporary folder.
		- Paste the copied files/folders into the created temporary folder.
		- Start the game.
		- Create new world.
		- Create new character.
		- Wait up to 2 minutes for the auto save.
		- Close the game.
		- Copy the files/folders from the created temporary folder.
		- Open File Explorer and run the search for:  
		  `%localappdata%\Pal\Saved\SaveGames\`
		- Look for a folder with a **random ID** (this should be your **Steam ID**).
		- Open that folder and **sort the subfolders by the "Last Modified" date**.
		- The folder with the most recent modification date is typically the one for your **world**.
		- Open that folder.
		- Paste the copied files/folders from the created temporary folder.
		- Start the game.
		- Rejoin the same world you just made.
		- Remake the new character again.
		- Wait up to 2 minutes for the auto save after making the character.
		- Close the game.
		- Open File Explorer and run the search for:  
		  `%localappdata%\Pal\Saved\SaveGames\`
		- Look for a folder with a **random ID** (this should be your **Steam ID**).
		- Open that folder and **sort the subfolders by the "Last Modified" date**.
		- The folder with the most recent modification date is typically the one for your **world**.
		- Open that folder.
		- Check the Players folder, you should see two different files:
			- 0001.sav, which is the solo/co-op save - aka, the host save.
			- RANDOMID....000.sav, which is YOUR regular save.
		- Copy these:
			- Players folder
			- Level.sav
		- Create new temporary folder if you desire and paste into that new temporary folder, or simply paste into former temporary folder you created earlier.
3. **Use the Fix Host Save**  
	- Click on Browse button:
		- Nagivate to the created temporary folder from above steps.
		- Select the Level.sav in that temporary folder.
	- After it loads the Level.sav data:
		- Select your old character as old GUID.
		- Select your new character as new GUID.
	- After you confirm and everything looks right, you may go ahead and press the Migrate button.
4. **Updating the solo/co-op or server saves**
	- Open the temporary folder you just migrated.
	- Copy these:
		- Players folder
		- Level.sav
	**Server to solo/co-op**
		- Open File Explorer and run the search for:  
		  `%localappdata%\Pal\Saved\SaveGames\`
		- Look for a folder with a **random ID** (this should be your **Steam ID**).
		- Open that folder and **sort the subfolders by the "Last Modified" date**.
		- The folder with the most recent modification date is typically the one for your **world**.
		- Open that folder.
		- Paste the copied files/folders into that folder.
		- Start the game.
		- Load the world.
		- Enjoy your old character, with all of bases/inventory/pals/etc intact.
	**Solo/co-op to server**
		- Go into `steamapps\common\Palworld\Pal\Saved\SaveGames\0\RANDOMSERVERID\`
		- Paste the copied files/folders into that folder.
		- Start the game.
		- Join the server.
		- Enjoy your old character, with all of bases/inventory/pals/etc intact.