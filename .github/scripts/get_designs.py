import argparse
import json
import os


def parse_lvs_config(file_path):
    """Parses the LVS config file at the specified path."""
    with open(file_path) as f:
        data = json.load(f)
    return data


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--design", help="The path to the design.")
    args = parser.parse_args()
    if os.path.exists(f"{args.design}/lvs/user_project_wrapper/lvs_config.json"):
        config_file = f"{args.design}/lvs/user_project_wrapper/lvs_config.json"
    elif os.path.exists(f"{args.design}/lvs/openframe_project_wrapper/lvs_config.json"):
        config_file = f"{args.design}/lvs/openframe_project_wrapper/lvs_config.json"
    data = parse_lvs_config(config_file)
    f = open("harden_sequence.txt", "w")
    for d in data['LVS_VERILOG_FILES']:
        macro_name = d.split('/')[-1].split('.v')[0]
        if macro_name.startswith('$'):
            macro_name = data[f'{macro_name.split("$")[1]}']
        if os.path.exists(f"{args.design}/openlane/{macro_name}/config.json"):
            f.write(f"{macro_name} ")
    f.close()


if __name__ == "__main__":
    main()
