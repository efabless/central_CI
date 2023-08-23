import json
import subprocess
import os
import threading


def get_designs(json_file):
    """Gets the designs from the JSON file."""
    with open(json_file) as f:
        data = json.load(f)
    designs = data["Designs"]
    return designs


def clone_repo(design, commit_hash):
    """Clones the repo for the specified design with the specified commit."""
    owner = "efabless"
    repo_name = design
    url = f"https://github.com/{owner}/{repo_name}.git"
    subprocess.run(['git', 'clone', f'{url}'])
    subprocess.run(['git', 'checkout', f'{commit_hash}'], cwd=design)
    files = find_lvs_config_files(design)
    f = open(f"{design}_tmp.txt", "w")
    for file_path in files:
        data = parse_lvs_config(file_path)
        for d in data:
            macro_name = d.split('/')[-1].split('.v')[0]
            if macro_name.startswith('$'):
                macro_name = 'user_project_wrapper'
            f.write(f"{macro_name} ")


def parse_lvs_config(file_path):
    """Parses the LVS config file at the specified path."""
    with open(file_path) as f:
        data = json.load(f)
    return data['LVS_VERILOG_FILES']


def find_lvs_config_files(root_dir):
    """Finds all LVS config files under the specified directory."""
    files = []
    for dir_path, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename == "lvs_config.json":
                path = os.path.join(dir_path, filename)
                files.append(path)
    return files


def main():
    json_file = f"{os.path.dirname(os.path.abspath(__file__))}/designs.json"
    designs = get_designs(json_file)
    threads = []
    for design, commit_hash in designs.items():
        thread = threading.Thread(target=clone_repo, args=(design, commit_hash))
        threads.append(thread)

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()


if __name__ == "__main__":
    main()
