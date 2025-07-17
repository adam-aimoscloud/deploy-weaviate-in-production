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
temp_dir = args.temp_dir
template_path = os.path.join(os.path.dirname(__file__), "app_template.yaml")

if os.path.exists(temp_dir):
    shutil.rmtree(temp_dir)
os.makedirs(temp_dir)

with open(config_path, "r") as f:
    config = yaml.safe_load(f)

app_name = config["app"]["name"]
pvc_name = config["app"]["pvc_name"]
namespace = config["namespace"]
storage = config["app"]["storage"]
replicas = config["app"]["replicas"]
image = config["app"]["image"]
init_image = config["app"]["init_image"]
request_cpu = config["app"]["request_cpu"]
request_memory = config["app"]["request_memory"]
limit_cpu = config["app"]["limit_cpu"]
limit_memory = config["app"]["limit_memory"]
lb_id = config["app"]["lb_id"]
api_key = config["app"]["api_key"]

result_path = os.path.join(temp_dir, f"{app_name}.yaml")
generate_yaml(
    template_path=template_path,
    result_path=result_path,
    app_name=app_name,
    pvc_name=pvc_name,
    namespace=namespace,
    storage=storage,
    replicas=replicas,
    image=image,
    init_image=init_image,
    request_cpu=request_cpu,
    request_memory=request_memory,
    limit_cpu=limit_cpu,
    limit_memory=limit_memory,
    lb_id=lb_id,
    api_key=api_key,
)
