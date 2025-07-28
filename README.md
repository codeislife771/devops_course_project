# 📝 Flask Task Manager – With Kubernetes Deployment

A simple, modern, and containerized web application for managing tasks. It features a lightweight Flask backend, a clean frontend, RESTful API support, and full Kubernetes deployment configuration for scaling in production environments.

---

## 🚀 Overview

This project includes two parts:

1. **Flask Task Manager App**:
   - A web-based task manager with CRUD operations
   - REST API and responsive UI
   - Stores tasks in a JSON file
   - Can be run locally or in Docker

2. **Kubernetes Deployment**:
   - Runs the Flask app in 3 replicas
   - Exposes the app via LoadBalancer
   - Uses ConfigMap for environment variables
   - Includes an Alpine-based debugging pod

---

## 📁 Project Structure

```
devops_course_project/
   └── flask-task-manager/
      ├── app.py                 # Flask application
      ├── requirements.txt       # Python dependencies
      ├── Dockerfile             # Docker container configuration
      ├── tasks.json             # JSON data storage
      ├── templates/
         └── index.html         # HTML user interface
         
   └── k8s/                   # Kubernetes manifests
      ├── flask_app_deployment.yaml   # Deployment: runs 3 replicas of the Flask app
      ├── load_balancer.yaml          # Service: exposes the app externally using LoadBalancer
      ├── flask-configmap.yaml        # ConfigMap: stores environment variables for the app
      └── user_pod.yaml               # Debug pod: Alpine container for testing inside the cluster
```

---

## 💡 Features

- ✅ **Task Management**: Create, update, delete, and view tasks
- 🌐 **REST API**: JSON-based API endpoints
- 🎨 **Modern UI**: HTML & CSS frontend with vanilla JS
- 📦 **Lightweight Storage**: File-based `tasks.json`
- 🐳 **Docker Support**: Containerized for consistency
- ☁️ **Kubernetes Ready**: Scalable and configurable via manifests

---

## 🧪 Quick Start – Local Development

1. **Clone the Repository**
   ```bash
   git clone <your-repo-url>
   cd flask-task-manager
   ```

2. **Create a Virtual Environment**
   ```bash
   python -m venv venv
   venv\Scripts\activate     # On Windows
   # source venv/bin/activate  # On macOS/Linux
   ```

3. **Install Dependencies and Run**
   ```bash
   pip install -r requirements.txt
   python app.py
   ```

4. **Visit the App**
   ```
   http://localhost:5000
   ```

---

## 🐳 Docker Deployment

### Build and Run

```bash
docker build -t flask-task-manager .
docker run -p 5000:5000 flask-task-manager
```

### Persistent Storage Options

```bash
# Mount local tasks.json (for development)
docker run -p 5000:5000 -v ${PWD}/tasks.json:/app/tasks.json flask-task-manager

# Named Docker volume (for production)
docker volume create task-data
docker run -p 5000:5000 -v task-data:/app flask-task-manager
```

---

## ☸️ Kubernetes Deployment

### Prerequisites

- Kubernetes cluster (Minikube, Kind, EKS, GKE, etc.)
- `kubectl` CLI
- Internet access to pull Docker image:  
  `codeislife771/flask-task-manager:latest`

### Steps to Deploy

```bash
# 1. Create ConfigMap
kubectl apply -f k8s/flask-configmap.yaml

# 2. Deploy Flask App (3 replicas)
kubectl apply -f k8s/flask_app_deployment.yaml

# 3. Expose with LoadBalancer
kubectl apply -f k8s/load_balancer.yaml

# 4. (Optional) Add a Debug Pod
kubectl apply -f k8s/user_pod.yaml
```

---

### 🌐 Accessing the App

**Option 1: LoadBalancer (Production)**  
```bash
kubectl get service flask-service
curl http://<EXTERNAL-IP>/tasks
```

**Option 2: Port Forwarding (Development)**  
```bash
kubectl port-forward --address 0.0.0.0 service/flask-service 5000:80
curl http://localhost:5000/tasks
```

**Option 3: Minikube Tunnel**
```bash
minikube tunnel
minikube service flask-service --url
```

---

## 🔗 API Endpoints

| Method | Endpoint           | Description              |
|--------|--------------------|--------------------------|
| GET    | `/api/tasks`       | Get all tasks            |
| POST   | `/tasks`           | Create a task            |
| PUT    | `/tasks/<name>`    | Update a task            |
| DELETE | `/tasks/<name>`    | Delete a task            |
| GET    | `/health`          | Health check             |

---

## 🛠 Debugging with Alpine Pod

```bash
kubectl exec -it user-pod -- sh
wget -qO- http://flask-service/tasks
```

---

## 🧩 ConfigMap Variables

From `k8s/flask-configmap.yaml`:

```yaml
PORT: 5000
DEBUG: true
DB_HOST: localhost
```

---

## 📋 Health, Scaling & Logs

```bash
# View status
kubectl get pods -l app=flask
kubectl get deployment flask-deployment

# Scale up/down
kubectl scale deployment flask-deployment --replicas=5

# View logs
kubectl logs -l app=flask --tail=100
```

---

## ❌ Cleanup

To remove all Kubernetes resources:

```bash
kubectl delete -f k8s/
```

---

## 📄 License

This project is open for educational and development use.  
No official license included.
