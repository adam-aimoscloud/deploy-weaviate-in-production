cd backup
python3 generate_backup_yaml.py --config ../config.yaml --temp-dir ../temp_backup

read -p "Start deployment, Y/N: " confirm
if [[ "$confirm" != "y" && "$confirm" != "Y" ]]; then
    echo "Deployment exited."
    exit 0
fi

kubectl apply -f ../temp_backup/weaviate-backup-pv.yaml
kubectl apply -f ../temp_backup/weaviate-backup-pvc.yaml
kubectl apply -f ../temp_backup/weaviate-backup.yaml