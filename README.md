# PalWorldSaveTools: Working as of v0.4.12 patch.

- **Author:** MagicBear and cheahjs 
- **License:** MIT License  
- **Updated by:** Pylar and Techdude  
- **Map Pictures Provided by:** Kozejin 
- **Testers/Helpers:** Lethe

## Important Installation Note
- Please make sure to use the official version of Python via [python.org/downloads](https://www.python.org/downloads), NOT the WindowsApps version of Python. Otherwise, you may encounter issues due to downloading and installing packages. 
- If you encounter any issues even after using the official version of Python, please install the Visual C++ Redistributable AIO from:  
[Visual C++ Redistributable AIO](https://github.com/abbodi1406/vcredist/releases).
- If the cityhash hasn't been installed, you will need to download the [VS build tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/). *Make sure to tick the option that says: Desktop development with C++ as shown below.*
![CityHash Screenshot](https://i.imgur.com/RZGZ9So.png)

## Current Features
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

## Transferring Local Saves to Server
- Make sure to disable private locks on the "host" chests.
- If you are trying to use GamePass saves(Xbox Platform), make sure to use XPG save extractor then convert it to json. Then reconvert json back to Level.sav. Then use the tool.

## How to Automatically Delete Player Saves Based on Inactivity
1. Copy everything from your server (`\Pal\Saved\SaveGames\0\RANDOMSERVERID\`) into the same location within the tool (`PalworldSaveTools\`).
2. Run `fix_save.cmd`.
3. Run `sort_players.cmd` and/or `delete_pals_save.cmd`.
4. Copy the `Players` folder from the tool.
5. Delete the original `Players` folder from the server (`\Pal\Saved\SaveGames\0\RANDOMSERVERID\`).
6. Paste the copied `Players` folder into the server folder.
7. Start the server up.
8. Reboot twice, once to clear the player out of Level.sav. Twice to clear the player out of ram. 
9. Profit?

## Additional Notes
- **Days:** Tracks players inactive for a specified number of days (e.g., 30 days and older).
- **Level:** Tracks players up to a specified level (e.g., level 30 or lower).
- **Pals:** Deletes players based on the number of pals (e.g., 10 or fewer pals).