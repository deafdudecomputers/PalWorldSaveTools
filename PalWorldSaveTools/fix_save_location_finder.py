from fix_save import *
def get_number_in_range(min_value, max_value):
  while True:
    try:
      number = int(input(f"Enter a number between {min_value} and {max_value}: "))
      if min_value <= number <= max_value:
        return number
      else:
        print("Number is out of range. Try again.")
    except ValueError:
      print("Invalid input. Please enter an integer.")
def repair_save(level_file):
    print(f"Now starting the tool...")
    global output_file, output_path, args, gui, playerMapping
    if not os.path.exists(level_file):
        logging.info(f"{level_file} does not exist.")
        exit(1)
    if not os.path.isfile(level_file):
        logging.info(f"{level_file} is not a file.")
        exit(1)
    t1 = time.time()
    try:
        input_file_size = os.path.getsize(level_file)
        logging.info(f"Size Level.sav: {input_file_size} bytes")
        LoadFile(level_file)
    except Exception as e:
        logging.info("Corrupted Save File", exc_info=True)
        sys.exit(0)
    try:
        logging.info(f"Now checking the data...")
        ShowPlayers()
        logging.info("Data has been fully checked...\n")
    except KeyError as e:
        traceback.print_exception(e)
        logging.info("Corrupted Save File", exc_info=True)
        sys.exit(0)
    print("Total time taken: %.2fs" % (time.time() - t1))
    print("\n")
    output_path = level_file
    return None
def main():
    level_file = "PalWorldSave/Level.sav"
    repair_save(level_file)
if __name__ == "__main__":
    main()