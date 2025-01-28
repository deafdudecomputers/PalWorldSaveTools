import os, subprocess, sys
def setup_environment():
    if sys.platform != "win32":
        import resource
        resource.setrlimit(resource.RLIMIT_NOFILE, (65535, 65535))
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Setting up your environment...")
    os.makedirs("PalWorldSave/Players", exist_ok=True)
    if not os.path.exists("venv"): subprocess.run([sys.executable, "-m", "venv", "venv"])
    pip_executable = os.path.join("venv", "Scripts", "pip") if os.name == 'nt' else os.path.join("venv", "bin", "pip")
    subprocess.run([pip_executable, "install", "-r", "requirements.txt"])
def run_menu():
    python_exe = os.path.join("venv", "Scripts", "python.exe") if os.name == 'nt' else os.path.join("venv", "bin", "python")
    menu_script = os.path.join(os.getcwd(), "Menu.py")
    subprocess.run([python_exe, menu_script])
if __name__ == "__main__":
    setup_environment()
    run_menu()