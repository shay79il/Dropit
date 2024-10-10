# Dropit Assignment

This repository contains the sample application for the [MongoDB and Express.js REST API tutorial](https://www.mongodb.com/languages/express-mongodb-rest-api-tutorial).


## Prerequisites

Ensure you have the following installed on your machine:

•   [Git](https://git-scm.com/downloads)

•   [Docker](https://docs.docker.com/get-started/)

•   [Minikube](https://minikube.sigs.k8s.io/docs/start/)

•	[Kubectl](https://kubernetes.io/docs/tasks/tools/)


## How To Run

1. Clone the repository

2. Start minikube
```bash
minikube start --driver=docker
```

3. Enable Ingress Addon
```bash
minikube addons enable ingress
```

4. Run minikube tunnel
```bash
minikube tunnel --cleanup
```

5. Apply K8S manifests
```bash
kubectl apply -f k8s-manifests
```

6. Add DNS record to /etc/hosts
```bash
sudo tee -a /etc/hosts > /dev/null <<< "127.0.0.1  dropit.local"
```

7. Access the Application
   Open your browser and navigate to [dropit.local](http://dropit.local/create)

8. Access Job output
```bash
minikube ssh
cd /tmp/hostpath-provisioner/default/csv-pvc
cat posts.csv
cat airports_data.csv
```

## Cleanup

To stop the application and clean up resources:
```bash
kubectl delete -f k8s-manifests/
minikube stop
```