from import_libs import *
def download_from_github(repo_owner, repo_name, version, download_path):
    file_url = get_release_assets(repo_owner, repo_name, version)
    if file_url:
        response = requests.get(file_url, stream=True)
        if response.status_code == 200:
            file_name = file_url.split("/")[-1]
            file_path = os.path.join(download_path, file_name)
            with open(file_path, "wb") as f:
                for chunk in response.iter_content(1024): f.write(chunk)
            print(f"File '{file_name}' downloaded successfully to '{download_path}'")
            return file_path
        else: print(f"Error downloading file: {response.status_code}")
    else: print("Error: No valid asset found.")
    return None
def get_release_assets(repo_owner, repo_name, version):
    api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/releases/tags/{version}"
    response = requests.get(api_url)
    if response.status_code == 200:
        release_data = response.json()
        assets = release_data['assets']
        for asset in assets:
            print(f"Found asset: {asset['name']}")
            if "psp-windows" in asset['name'] and asset['name'].endswith('.zip'):
                return asset['browser_download_url']
        print("No matching assets found.")
        return None
    else:
        print(f"Error fetching release info: {response.status_code}")
        return None
def extract_zip(directory, partial_name, extract_to):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.zip') and partial_name in file:
                with zipfile.ZipFile(os.path.join(root, file), 'r') as zip_ref:
                    zip_ref.extractall(extract_to)
                print(f"Extracted {file} to {extract_to}")
def get_latest_version(repo_owner, repo_name):
    api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/releases/latest"
    response = requests.get(api_url)
    if response.status_code == 200:
        latest_release = response.json()
        version = latest_release['tag_name']
        return version
    else:
        print(f"Error fetching release info: {response.status_code}")
        return None
def main():
    file_path, download_file = "psp_windows/psp.exe", ""
    repo_owner = "oMaN-Rod"
    repo_name = "palworld-save-pal"
    version = get_latest_version(repo_owner, repo_name)
    if version:
        if os.path.exists(file_path):
            print("Opening Palworld Save Pal...")
            os.chdir("psp_windows")
            subprocess.Popen("psp.exe")
        else:
            print("Downloading Palworld Save Pal...")
            zip_file = download_from_github(repo_owner, repo_name, version, ".")
            if zip_file:
                extract_zip(".", "psp-windows", "psp_windows")
                os.remove(zip_file)
                print(f"Removed downloaded file: {zip_file}")
            if os.path.exists(file_path):
                print("Opening Palworld Save Pal...")
                os.chdir("psp_windows")
                subprocess.Popen("psp.exe")
            else: print("Failed to download Palworld Save Pal...")
    else: print("Unable to fetch latest release version.")
if __name__ == "__main__": main()