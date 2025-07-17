cd pv

python3 generate_yaml.py --config ../config.yaml --temp-dir ../temp_pv

read -p "Start deployment, Y/N: " confirm
if [[ "$confirm" != "y" && "$confirm" != "Y" ]]; then
    echo "Deployment exited."
    exit 0
fi

for file in ../temp_pv/*; do
    kubectl apply -f "$file"
done