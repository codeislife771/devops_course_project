# Flask Task Manager on Kubernetes

This project demonstrates how to deploy a scalable **Flask-based Task Manager API** in a Kubernetes cluster using modern deployment practices. It includes configuration files for:

- A **Deployment** running 3 replicas of the Flask app for high availability
- A **LoadBalancer Service** for external access to the application
- A **ConfigMap** to inject environment variables
- A utility Pod (`user-pod`) for internal testing/debugging (using Alpine)

---

## 📁 Project Structure

```bash
k8s/
├── flask_app_deployment.yaml   # Deployment with 3 Flask app replicas
├── load_balancer.yaml          # LoadBalancer Service for external access
├── flask-configmap.yaml        # ConfigMap with environment variables
├── user_pod.yaml               # Alpine Pod for internal debugging
└── README.md                   # This documentation
```

---

## ⚙️ Prerequisites

- Kubernetes cluster (Minikube, Kind, EKS, GKE, etc.)
- `kubectl` CLI configured to access your cluster
- Internet access from the cluster to pull the image: `codeislife771/flask-task-manager:latest`

---

## 🚀 How to Deploy

1. **Apply the ConfigMap**:
   ```bash
   kubectl apply -f flask-configmap.yaml
   ```

2. **Deploy the Flask Application** (3 replicas):
   ```bash
   kubectl apply -f flask_app_deployment.yaml
   ```

3. **Expose the Application using LoadBalancer**:
   ```bash
   kubectl apply -f load_balancer.yaml
   ```

4. **(Optional) Deploy Debugging Pod**:
   ```bash
   kubectl apply -f user_pod.yaml
   ```

---

## 🌐 Accessing the Flask App

### Method 1: Direct Access via LoadBalancer

Once the LoadBalancer service is running, get the external IP:

```bash
kubectl get services flask-service
```

Wait for the `EXTERNAL-IP` to be assigned (may show `<pending>` initially), then access:

```bash
# Replace <EXTERNAL-IP> with the actual IP from the command above
curl http://<EXTERNAL-IP>/tasks
```

### Method 2: Access via ClusterIP (Internal)

Get the ClusterIP of the service:

```bash
kubectl get service flask-service -o jsonpath='{.spec.clusterIP}'
```

From within the cluster (e.g., using the debug pod):

```bash
kubectl exec -it user-pod -- sh
# Inside the pod:
wget -qO- http://<CLUSTER-IP>/tasks
```

### Method 3: Port Forwarding (Local Development)

Forward the service to your local machine:

```bash
# Forward service port 80 to local port 5000
kubectl port-forward --address 0.0.0.0 service/flask-service 5000:80
```

Then access locally:

```bash
curl http://localhost:5000/tasks
```

### Method 4: Alternative Exposure Methods

Depending on your environment, you can also use:

**For Minikube:**
```bash
# Enable tunnel for LoadBalancer support
minikube tunnel

# Or use NodePort temporarily
kubectl patch service flask-service -p '{"spec":{"type":"NodePort"}}'
minikube service flask-service --url
```

**For Cloud Providers:**
LoadBalancer services automatically provision cloud load balancers (ALB, GCE LB, etc.)

**Using ngrok (for external access from local clusters):**
```bash
kubectl port-forward service/flask-service 5000:80 &
ngrok http 5000
```

---

## 📦 Environment Variables (from ConfigMap)

Defined in `flask-configmap.yaml`:

```yaml
PORT: 5000
DEBUG: true
DB_HOST: localhost
```

These are automatically injected into all Flask container replicas using `envFrom`.

---

## 🔍 Health Checks & Scaling

The deployment includes:

- **3 replicas** for high availability and load distribution
- **Liveness probes** - Restart unhealthy containers
- **Readiness probes** - Only route traffic to ready containers
- **Automatic scaling** capabilities (can be enhanced with HPA)

Check deployment status:

```bash
kubectl get deployment flask-deployment
kubectl get pods -l app=flask
```

Scale replicas if needed:

```bash
kubectl scale deployment flask-deployment --replicas=5
```

---

## 🛠 Debug with Alpine Pod

Use the `user-pod.yaml` to create a simple Alpine container for testing internal connectivity:

```bash
kubectl exec -it user-pod -- sh
```

From inside, test the service:

```bash
# Test internal service discovery
wget -qO- http://flask-service/tasks

# Test specific pod IPs
kubectl get pods -l app=flask -o wide
wget -qO- http://<POD-IP>:5000/tasks
```

---

## 📊 Monitoring & Troubleshooting

**Check service endpoints:**
```bash
kubectl get endpoints flask-service
```

**View logs from all replicas:**
```bash
kubectl logs -l app=flask --tail=100
```

**Describe resources for troubleshooting:**
```bash
kubectl describe deployment flask-deployment
kubectl describe service flask-service
```

---

## ✅ Cleanup

To delete all created resources:

```bash
kubectl delete -f .
```

Or individually:

```bash
kubectl delete -f flask_app_deployment.yaml
kubectl delete -f load_balancer.yaml
kubectl delete -f flask-configmap.yaml
kubectl delete -f user_pod.yaml
```

---

## 📌 Notes

- **Deployment** ensures desired replica count and provides rolling updates
- **LoadBalancer Service** automatically provisions external load balancer (cloud-dependent)
- **Health probes** ensure only healthy pods receive traffic
- **Service discovery** allows internal communication via service name (`flask-service`)
- **ConfigMap** changes require pod restart to take effect

---

## 📄 License

This project is for educational and development purposes. No license included.
