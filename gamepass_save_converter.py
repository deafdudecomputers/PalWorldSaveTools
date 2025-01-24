from fix_save import *
def download_from_github(repo_owner, repo_name, file_name, download_path):
    url = f"https://github.com/{repo_owner}/{repo_name}/releases/latest/download/{file_name}"; response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(f"{download_path}/{file_name}", "wb") as f: [f.write(chunk) for chunk in response.iter_content(1024)]; print(f"File '{file_name}' downloaded successfully to '{download_path}'")
    else: print(f"Error downloading file: {response.status_code}")
def main():
    file_name = "GPSaveConverter.exe"; 
    if os.path.exists(file_name): 
        print("Opening Game Pass Save Converter Manager..."); subprocess.Popen(file_name)
    else: 
        print("Downloading Game Pass Save Converter Manager..."); download_from_github("Fr33dan", "GPSaveConverter", file_name, ".")
        if os.path.exists(file_name): 
            print("Opening Game Pass Save Converter Manager..."); subprocess.Popen(file_name)
        else: print("Failed to download Game Pass Save Converter Manager...")
if __name__ == "__main__": main()