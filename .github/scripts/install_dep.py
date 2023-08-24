import json
import volare
import argparse
import requests
import tarfile
import os


def get_tool_data(json_file):
    """Gets the designs from the JSON file."""
    with open(json_file) as f:
        data = json.load(f)
    return data


def install_tool(tool, version, url, tool_path):
    if tool == "pdk":
        volare.enable(f'{tool_path}/pdk', "sky130", version)
    else:
        get_tarball(f'{url}/tarball/{version}', tool)
        extract_tarball(tool, f'{tool_path}')


def get_tarball(url, tool):
    response = requests.get(url, stream=True)
    if response.status_code != 200:
        raise Exception('Failed to get tarball: {}'.format(response.status_code))

    with open(f'{tool}.tar.gz', 'wb') as f:
        for chunk in response.iter_content(chunk_size=1024):
            f.write(chunk)


def extract_tarball(tool, tool_path):
    with tarfile.open(f'{tool}.tar.gz', 'r:gz') as tar:
        tar.extractall(tool_path)
    os.remove(f'{tool}.tar.gz')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", help="The path to the json file.")
    parser.add_argument("--output", help="The path to the location of download")
    parser.add_argument("--dependency", help="Dependency to download")
    args = parser.parse_args()

    json_file = args.json
    output_path = args.output
    dependency = args.dependency
    tool_data = get_tool_data(json_file)

    for tool, value in tool_data.items():
        if tool == dependency:
            install_tool(tool, value['commit'], value['url'], output_path)


if __name__ == "__main__":
    main()
