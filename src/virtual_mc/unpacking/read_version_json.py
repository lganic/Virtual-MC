import zipfile
import json

def read_version_json(jar_path):
    with zipfile.ZipFile(jar_path, 'r') as jar:
        with jar.open('version.json') as file:
            return json.load(file)