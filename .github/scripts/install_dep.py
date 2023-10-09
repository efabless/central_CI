import json
import os
import tarfile
import requests
import volare
import argparse
import ipm


def get_tool_data(json_file):
    """Gets the designs from the JSON file."""
    with open(json_file) as f:
        data = json.load(f)
    return data


def install_tool(tool, version, url, tool_path):
    if tool == "pdk":
        volare.enable(f'{tool_path}/pdk', "sky130", version)
    else:
        name = url.split("/")[-1]
        owner = url.split("/")[-2]
        print(f"downloading {tool}")
        response = requests.get(f'{url}/tarball/{version}')
        if response.status_code != 200:
            raise Exception(f"Failed to download {tool}")
        with open(f'{tool_path}/{version}.tar.gz', 'wb') as file:
            file.write(response.content)
        print(f"extracting {tool_path}/{version}.tar.gz")

        tar = tarfile.open(f'{tool_path}/{version}.tar.gz', 'r:gz')
        tar.extractall(path=tool_path)
        tar.close()
        os.rename(f'{tool_path}/{owner}-{name}-{version[0:7]}', f'{tool_path}/{tool}')
        os.remove(f'{tool_path}/{version}.tar.gz')
        if os.path.exists(f"{tool_path}/{tool}/ip/dependencies.json"):
            ipm.install_deps(f"{tool_path}/{tool}/ip", f"{tool_path}/{tool}/ip")


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
