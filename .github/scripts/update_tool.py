import argparse
import json
import os
import re
import subprocess
import requests


def get_latest_commit(repo, repo_url):
    if repo == "pdk":
        response = requests.get("https://api.github.com/repos/efabless/volare/releases/latest")
        sha = f'{response.json()["tag_name"].split("-")[-1]}'
    else:
        # from https://stackoverflow.com/questions/62525382/how-to-get-the-latest-commit-hash-on-remote-using-gitpython
        process = subprocess.Popen(["git", "ls-remote", repo_url], stdout=subprocess.PIPE)
        stdout, stderr = process.communicate()
        sha = re.split(r'\t+', stdout.decode('ascii'))[0]
    return sha


def export_env_default(key, value):
    print(os.getenv("GITHUB_ENV"))
    with open(os.getenv("GITHUB_ENV"), "a") as f:
        f.write("%s=%s\n" % (key, value))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", help="The path to the json file.")
    args = parser.parse_args()

    json_file = args.json
    json_files = [f"{json_file}/tools.json", f"{json_file}/.github/scripts/designs.json"]
    for json_file in json_files:
        with open(json_file) as f:
            data = json.load(f)

        for repo, repo_data in data.items():
            commit = repo_data["commit"]
            url = repo_data["url"]
            latest_commit = get_latest_commit(repo, url)

            if commit != latest_commit:
                repo_data["commit"] = latest_commit
                with open(json_file, "w") as f:
                    json.dump(data, f, indent=4)
                export_env_default('NO_UPDATE', '0')
            else:
                export_env_default('NO_UPDATE', '1')


if __name__ == "__main__":
    main()
