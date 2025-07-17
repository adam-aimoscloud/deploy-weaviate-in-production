cp config.yaml backup/
cd backup
image_url=$(python3 get_image_url.py --config ../config.yaml)
docker build -t $image_url .

read -p "Start deployment, Y/N: " confirm
if [[ "$confirm" != "y" && "$confirm" != "Y" ]]; then
    echo "Deployment exited."
    exit 0
fi

docker push $image_url