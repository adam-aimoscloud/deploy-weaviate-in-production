helm repo add weaviate https://weaviate.github.io/weaviate-helm
helm repo update
helm show values weaviate/weaviate > values.yaml