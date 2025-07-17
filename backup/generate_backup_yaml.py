import yaml
import argparse
import os
import shutil
from typing import List, Dict
import json


def generate_pv_yaml(template_path: str, output_path: str, src_dirs: List[Dict[str, str]]):
    with open(template_path, 'r') as file:
        template = file.read()
    result = ''
    for src_dir in src_dirs:
        temp = template.replace("{pv_name}", src_dir["pv"])
        temp = temp.replace("{storage}", src_dir["storage"])
        temp = temp.replace("{server}", src_dir["server"])
        temp = temp.replace("{path}", src_dir["subpath"])
        result += temp
        result += '\n---\n'
    with open(output_path, 'w') as file:
        file.write(result)

    
def generate_pvc_yaml(template_path: str, output_path: str, src_dirs: List[Dict[str, str]], namespace: str):
    with open(template_path, 'r') as file:
        template = file.read()
    result = ''
    for src_dir in src_dirs:
        temp = template.replace("{pv_name}", src_dir["pv"])
        temp = temp.replace("{storage}", src_dir["storage"])
        temp = temp.replace("{namespace}", namespace)
        result += temp
        result += '\n---\n'
    with open(output_path, 'w') as file:
        file.write(result)


def generate_app_yaml(template_path: str, output_path: str, src_dirs: List[Dict[str, str]], name: str, image: str, namespace: str):
    with open(template_path, 'r') as file:
        template = file.read()
    volumes = []
    for src_dir in src_dirs:
        volumes.append({
            "name": src_dir["pv"],
            "persistentVolumeClaim": {
                "claimName": src_dir["pv"]
            }
        })
    volume_mounts = []
    for src_dir in src_dirs:
        volume_mounts.append({
            "name": src_dir["pv"],
            "mountPath": src_dir["dir"],
            "readOnly": True
        })
    template = template.replace("{name}", name)
    template = template.replace("{volumes}", json.dumps(volumes))
    template = template.replace("{volume_mounts}", json.dumps(volume_mounts))
    template = template.replace("{image}", image)
    template = template.replace("{namespace}", namespace)
    with open(output_path, 'w') as file:
        file.write(template)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=str, required=True)
    parser.add_argument("--temp-dir", type=str, required=True)
    args = parser.parse_args()
    config_path = args.config
    temp_dir = args.temp_dir
    pvc_template_path = os.path.join(os.path.dirname(__file__), "templates/pvc.yaml")
    app_template_path = os.path.join(os.path.dirname(__file__), "templates/backup_template.yaml")
    pv_template_path = os.path.join(os.path.dirname(__file__), "templates/pv.yaml")
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    os.makedirs(temp_dir)
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
    namespace = config["namespace"]
    name = config["backup"]["name"]
    image = config["backup"]["image"]
    src_dirs = config["backup"]["src_dirs"]   
    generate_pv_yaml(pv_template_path, os.path.join(temp_dir, f"{name}-pv.yaml"), src_dirs)
    generate_pvc_yaml(pvc_template_path, os.path.join(temp_dir, f"{name}-pvc.yaml"), src_dirs, namespace)
    generate_app_yaml(app_template_path, os.path.join(temp_dir, f"{name}.yaml"), src_dirs, name, image, namespace)