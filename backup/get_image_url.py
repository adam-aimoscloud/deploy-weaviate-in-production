import yaml
import os
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=str, required=True)
    args = parser.parse_args()
    config_path = args.config
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
    image_url = config["backup"]["image"]
    print(image_url)    