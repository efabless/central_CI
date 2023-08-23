import json
import subprocess
import volare
import argparse
import threading


def get_tool_data(json_file):
    """Gets the designs from the JSON file."""
    with open(json_file) as f:
        data = json.load(f)
    return data


def install_tool(tool, version, url, tool_path):
    if tool == "pdk":
        volare.enable(f'{tool_path}/pdk', "sky130", version)
    else:
        subprocess.run(['git', 'clone', f'{url}', f'{tool}', f'{tool_path}/{tool}'])
        subprocess.run(['git', 'checkout', f'{version}'], cwd=f'{tool_path}/{tool}')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", help="The path to the json file.")
    parser.add_argument("--output", help="The path to the location of download")
    args = parser.parse_args()

    json_file = args.json
    output_path = args.output
    tool_data = get_tool_data(json_file)

    threads = []
    for tool, value in tool_data.items():
        thread = threading.Thread(target=install_tool, args=(tool, value['commit'], value['url'], output_path))
        threads.append(thread)

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()


if __name__ == "__main__":
    main()
