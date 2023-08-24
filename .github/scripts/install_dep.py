import json
import volare
import argparse
import requests
import tarfile
import os
import subprocess


def get_tool_data(json_file):
    """Gets the designs from the JSON file."""
    with open(json_file) as f:
        data = json.load(f)
    return data


def install_tool(tool, version, url, tool_path):
    if tool == "pdk":
        volare.enable(f'{tool_path}/pdk', "sky130", version)
    else:
        ps = subprocess.Popen(['curl', '-L', f'{url}/tarball/{version}'], cwd=tool_path, stdout=subprocess.PIPE)
        subprocess.check_output(['tar', '-xvzC', '.', '--strip-components=1'], cwd=tool_path, stdin=ps.stdout)
        ps.wait()


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
