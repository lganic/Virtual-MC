import requests
import zipfile
import json
import os
import shutil

# URL of the JSON version manifest
url = "https://launchermeta.mojang.com/mc/game/version_manifest.json"

server_abspath = os.path.join(os.path.dirname(__file__), 'server.jar')

def get_json_from_url(url):
    response = requests.get(url)
    # Check if the request was successful
    if response.status_code == 200:
        return response.json()
    else:
        raise ValueError(f"Failed to retrieve data. Status code: {response.status_code}")

def get_most_recent_version():
    data = get_json_from_url(url)

    latest_version = data.get('latest', {}).get('release', {})

    return latest_version

def get_server_download(target_version):
    metadata = get_json_from_url(url)

    # Search for the target version in the versions list
    version_url = None
    for version in metadata.get("versions", []):
        if version.get("id") == target_version:
            version_url = version.get("url")
            break
    
    if version_url:
        version_data = get_json_from_url(version_url)

        download_link = version_data.get('downloads', {}).get('server', {}).get('url', '')

        if download_link:
            return download_link
        else:
            print('Failed to find download link')
    else:
        print(f"Version {target_version} not found.")

def get_minecraft_version(jar_path):
    if not os.path.exists(jar_path):
        return 'No Server!'
    with zipfile.ZipFile(jar_path, 'r') as jar:
        # Attempt to locate version.json
        if 'version.json' in jar.namelist():
            with jar.open('version.json') as version_file:
                version_data = json.load(version_file)
                return version_data.get('name', 'Unknown version')
        # Fallback to MANIFEST.MF
        elif 'META-INF/MANIFEST.MF' in jar.namelist():
            with jar.open('META-INF/MANIFEST.MF') as manifest_file:
                for line in manifest_file:
                    line = line.decode('utf-8').strip()
                    if line.startswith('Implementation-Version'):
                        return line.split(': ')[1]
    return 'Unknown version'

def ensure_up_to_date(server_jar_path):
    current_version = get_minecraft_version(server_jar_path)

    latest_version = get_most_recent_version()

    print(f'Server is currently running: {current_version}, Latest version is: {latest_version}')

    if current_version != latest_version:
        # server is out of date, update!
        print('Updating server...')

        download_url = get_server_download(latest_version)

        print('Successfully resolved download link')

        # Send a GET request to download the file
        response = requests.get(download_url, stream=True)

        print('Pulling file...')
        # Check if the request was successful
        if response.status_code == 200:
            # Write the content to a file
            with open(server_jar_path, 'wb') as file:
                for chunk in response.iter_content(chunk_size=1024):
                    file.write(chunk)
            print(f"Downloaded new server jar successfully.")
        else:
            print(f"Failed to download file. Status code: {response.status_code}")

def unpack_server():

    # java -DbundlerMainClass="net.minecraft.data.Main" -jar server.jar --server

    ensure_up_to_date(server_abspath)

    os.system(f'java -DbundlerMainClass="net.minecraft.data.Main" -jar {server_abspath} --all')

def cleanup():

    build_location = os.path.dirname(server_abspath)

    paths_to_remove = ['generated', 'libraries', 'logs', 'versions']

    for path in paths_to_remove:

        print(f'Cleaning up directory: {path}')
        shutil.rmtree(os.path.join(build_location, path))

if __name__ == '__main__':
    cleanup()