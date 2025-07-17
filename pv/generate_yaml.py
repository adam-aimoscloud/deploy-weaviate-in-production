import yaml
import os
import argparse
import shutil

def generate_yaml(template_path: str, result_path: str, **kwargs):
    with open(template_path, "r") as f:
        template = f.read()
    for k, v in kwargs.items():
        template = template.replace(f"{{{k}}}", str(v))
    with open(result_path, "w") as f:
        f.write(template)


parser = argparse.ArgumentParser()
parser.add_argument("--config", type=str, required=True)
parser.add_argument("--temp-dir", type=str, required=True)
args = parser.parse_args()
config_path = args.config
template_path = os.path.join(os.path.dirname(__file__), "pv_template.yaml")
with open(config_path, "r") as f:
    config = yaml.safe_load(f)
namespace = config["namespace"]
app_name = config["app"]["name"]
pvc_name = config["app"]["pvc_name"]
pvs = config["pv"]

if os.path.exists(args.temp_dir):
    shutil.rmtree(args.temp_dir)
os.makedirs(args.temp_dir)

for i, pv in enumerate(pvs):
    pv_name = pv["name"]
    storage = pv["storage"]
    server = pv["server"]
    path = pv["path"]
    
    result_path = os.path.join(args.temp_dir, f"{pv_name}.yaml")
    generate_yaml(
        template_path=template_path,
        result_path=result_path,
        namespace=namespace,
        app_name=app_name,
        pv_name=pv_name,
        pvc_name=pvc_name,
        storage=storage,
        server=server,
        path=path,
        index=i,
    )
