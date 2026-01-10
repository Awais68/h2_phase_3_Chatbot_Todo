# Todo Evolution - Kubernetes Troubleshooting Guide

Comprehensive troubleshooting guide for resolving common issues in the Todo Evolution Kubernetes deployment.

## Table of Contents

1. [Pod Issues](#pod-issues)
2. [Database Issues](#database-issues)
3. [Network Issues](#network-issues)
4. [Storage Issues](#storage-issues)
5. [Performance Issues](#performance-issues)
6. [Kafka/Event Issues](#kafkaevent-issues)
7. [Dapr Issues](#dapr-issues)
8. [Ingress/TLS Issues](#ingresstls-issues)
9. [Auto-Scaling Issues](#auto-scaling-issues)
10. [Monitoring & Logging](#monitoring--logging)

---

## Pod Issues

### Pods Stuck in Pending State

**Symptoms**: Pods show `Pending` status for extended period

**Diagnosis**:
```bash
kubectl describe pod <pod-name> -n todo-app
kubectl get events -n todo-app --sort-by='.lastTimestamp'
```

**Common Causes**:

1. **Insufficient Resources**
   ```bash
   # Check node resources
   kubectl top nodes
   kubectl describe nodes

   # Solution: Add more nodes or reduce resource requests
   kubectl scale deployment/<deployment> -n todo-app --replicas=1
   ```

2. **Storage Provisioning Issues**
   ```bash
   # Check PVC status
   kubectl get pvc -n todo-app

   # Solution: Verify storage class exists
   kubectl get storageclass
   ```

3. **Node Selector/Affinity Issues**
   ```bash
   # Check if nodes have required labels
   kubectl get nodes --show-labels

   # Solution: Remove or update node selectors
   ```

### Pods Crashing (CrashLoopBackOff)

**Symptoms**: Pods continuously restart

**Diagnosis**:
```bash
kubectl logs <pod-name> -n todo-app --previous
kubectl describe pod <pod-name> -n todo-app
```

**Common Causes**:

1. **Application Errors**
   ```bash
   # Check application logs
   kubectl logs <pod-name> -n todo-app -c <container-name>

   # Solution: Fix application code or configuration
   ```

2. **Missing Configuration**
   ```bash
   # Check ConfigMap and Secrets
   kubectl get configmap todo-app-config -n todo-app -o yaml
   kubectl get secret todo-app-secrets -n todo-app -o yaml

   # Solution: Verify all required environment variables are set
   ```

3. **Failed Health Checks**
   ```bash
   # Disable health checks temporarily
   kubectl edit deployment/<deployment> -n todo-app
   # Comment out livenessProbe and readinessProbe
   ```

### Pods in ImagePullBackOff

**Symptoms**: Cannot pull container image

**Diagnosis**:
```bash
kubectl describe pod <pod-name> -n todo-app | grep -A 10 Events
```

**Solutions**:

1. **Verify Image Name**
   ```bash
   # Check image name in deployment
   kubectl get deployment/<deployment> -n todo-app -o yaml | grep image:

   # Update if incorrect
   kubectl set image deployment/<deployment> <container>=<correct-image> -n todo-app
   ```

2. **Private Registry Authentication**
   ```bash
   # Create image pull secret
   kubectl create secret docker-registry regcred \
     --docker-server=<registry> \
     --docker-username=<username> \
     --docker-password=<password> \
     -n todo-app

   # Add to deployment
   kubectl patch serviceaccount default \
     -p '{"imagePullSecrets": [{"name": "regcred"}]}' \
     -n todo-app
   ```

---

## Database Issues

### Cannot Connect to PostgreSQL

**Symptoms**: Backend cannot connect to database

**Diagnosis**:
```bash
# Check PostgreSQL pod status
kubectl get pod -n todo-app -l component=postgres

# Check PostgreSQL logs
kubectl logs -n todo-app statefulset/postgres -c postgres

# Test connection from backend pod
kubectl exec -n todo-app deployment/backend -c backend -- \
  psql postgresql://postgres:password@postgres-service:5432/todo_db -c "SELECT 1;"
```

**Solutions**:

1. **PostgreSQL Not Ready**
   ```bash
   # Wait for PostgreSQL to be ready
   kubectl wait --for=condition=ready pod -l component=postgres -n todo-app --timeout=300s

   # Check startup logs
   kubectl logs -n todo-app statefulset/postgres -c postgres --tail=100
   ```

2. **Incorrect Credentials**
   ```bash
   # Verify secrets
   kubectl get secret todo-app-secrets -n todo-app -o yaml

   # Update DATABASE_PASSWORD if incorrect
   kubectl create secret generic todo-app-secrets \
     --from-literal=DATABASE_PASSWORD=newpassword \
     --dry-run=client -o yaml | kubectl apply -f -

   # Restart backend pods
   kubectl rollout restart deployment/backend -n todo-app
   ```

3. **Network Connectivity**
   ```bash
   # Test DNS resolution
   kubectl exec -n todo-app deployment/backend -c backend -- nslookup postgres-service

   # Test port connectivity
   kubectl exec -n todo-app deployment/backend -c backend -- nc -zv postgres-service 5432
   ```

### Database Migrations Failed

**Symptoms**: Alembic migration errors in backend logs

**Diagnosis**:
```bash
# Check migration status
kubectl exec -n todo-app deployment/backend -c backend -- alembic current

# Check migration logs
kubectl logs -n todo-app deployment/backend -c run-migrations
```

**Solutions**:

1. **Run Migrations Manually**
   ```bash
   # Run all pending migrations
   kubectl exec -n todo-app deployment/backend -c backend -- alembic upgrade head

   # Downgrade if needed
   kubectl exec -n todo-app deployment/backend -c backend -- alembic downgrade -1
   ```

2. **Reset Database (DANGER!)**
   ```bash
   # Only in development!
   kubectl exec -n todo-app statefulset/postgres -c postgres -- \
     psql -U postgres -c "DROP DATABASE todo_db;"

   kubectl exec -n todo-app statefulset/postgres -c postgres -- \
     psql -U postgres -c "CREATE DATABASE todo_db;"

   # Run migrations
   kubectl exec -n todo-app deployment/backend -c backend -- alembic upgrade head
   ```

### Database Performance Issues

**Symptoms**: Slow queries, high CPU usage

**Diagnosis**:
```bash
# Check PostgreSQL resource usage
kubectl top pod -n todo-app -l component=postgres

# Check slow queries
kubectl exec -n todo-app statefulset/postgres -c postgres -- \
  psql -U postgres todo_db -c "SELECT query, calls, mean_exec_time FROM pg_stat_statements ORDER BY mean_exec_time DESC LIMIT 10;"
```

**Solutions**:

1. **Increase Resources**
   ```bash
   # Edit PostgreSQL StatefulSet
   kubectl edit statefulset postgres -n todo-app

   # Increase CPU and memory limits
   resources:
     limits:
       cpu: 4000m
       memory: 4Gi
   ```

2. **Optimize Queries**
   - Add database indexes
   - Optimize N+1 queries
   - Use connection pooling

3. **Enable Connection Pooling**
   ```yaml
   env:
   - name: DATABASE_POOL_SIZE
     value: "20"
   - name: DATABASE_MAX_OVERFLOW
     value: "10"
   ```

---

## Network Issues

### Service Not Accessible

**Symptoms**: Cannot reach service from within cluster

**Diagnosis**:
```bash
# Check service
kubectl get svc -n todo-app
kubectl describe svc backend-service -n todo-app

# Check endpoints
kubectl get endpoints backend-service -n todo-app

# Test from another pod
kubectl run test-pod --rm -it --image=curlimages/curl -n todo-app -- \
  curl http://backend-service:8000/health
```

**Solutions**:

1. **No Endpoints**
   ```bash
   # Check if pods match service selector
   kubectl get pods -n todo-app -l component=backend

   # Verify selector labels
   kubectl get svc backend-service -n todo-app -o yaml | grep -A 5 selector
   kubectl get pods -n todo-app -l component=backend --show-labels
   ```

2. **Wrong Port**
   ```bash
   # Verify service ports
   kubectl get svc backend-service -n todo-app -o yaml | grep -A 10 ports

   # Update if incorrect
   kubectl edit svc backend-service -n todo-app
   ```

### DNS Resolution Issues

**Symptoms**: Cannot resolve service names

**Diagnosis**:
```bash
# Test DNS resolution
kubectl run test-dns --rm -it --image=busybox -n todo-app -- nslookup backend-service

# Check CoreDNS
kubectl get pods -n kube-system -l k8s-app=kube-dns
kubectl logs -n kube-system -l k8s-app=kube-dns
```

**Solutions**:

1. **Use Fully Qualified Names**
   ```yaml
   # Instead of: backend-service
   # Use: backend-service.todo-app.svc.cluster.local
   ```

2. **Restart CoreDNS**
   ```bash
   kubectl rollout restart deployment/coredns -n kube-system
   ```

---

## Storage Issues

### PVC Stuck in Pending

**Symptoms**: PersistentVolumeClaim not bound

**Diagnosis**:
```bash
kubectl get pvc -n todo-app
kubectl describe pvc <pvc-name> -n todo-app
kubectl get storageclass
```

**Solutions**:

1. **No Storage Class**
   ```bash
   # List available storage classes
   kubectl get storageclass

   # Set default storage class
   kubectl patch storageclass <class-name> \
     -p '{"metadata": {"annotations":{"storageclass.kubernetes.io/is-default-class":"true"}}}'
   ```

2. **Insufficient Storage**
   ```bash
   # Check node storage capacity
   kubectl describe nodes | grep -A 5 "Allocated resources"

   # Reduce PVC size or add more storage
   kubectl edit pvc <pvc-name> -n todo-app
   ```

### Data Loss After Pod Restart

**Symptoms**: Data disappears after pod restart

**Diagnosis**:
```bash
# Check if PVC is used
kubectl get pod <pod-name> -n todo-app -o yaml | grep -A 10 volumes

# Verify PVC is bound
kubectl get pvc -n todo-app
```

**Solutions**:

1. **Add Volume Mount**
   ```yaml
   volumeMounts:
   - name: data
     mountPath: /var/lib/postgresql/data
   volumes:
   - name: data
     persistentVolumeClaim:
       claimName: postgres-data
   ```

2. **Backup and Restore**
   ```bash
   # Backup data
   kubectl exec -n todo-app <pod> -- tar czf - /data > backup.tar.gz

   # Restore data
   kubectl exec -i -n todo-app <pod> -- tar xzf - -C / < backup.tar.gz
   ```

---

## Performance Issues

### High CPU Usage

**Symptoms**: Pods consuming excessive CPU

**Diagnosis**:
```bash
# Check CPU usage
kubectl top pods -n todo-app
kubectl top nodes

# Check HPA status
kubectl get hpa -n todo-app
```

**Solutions**:

1. **Scale Horizontally**
   ```bash
   # Increase replica count
   kubectl scale deployment/backend -n todo-app --replicas=5
   ```

2. **Optimize Application Code**
   - Profile application
   - Optimize hot code paths
   - Add caching

3. **Adjust CPU Limits**
   ```yaml
   resources:
     limits:
       cpu: 2000m  # Increase limit
   ```

### High Memory Usage

**Symptoms**: Pods being OOMKilled

**Diagnosis**:
```bash
# Check memory usage
kubectl top pods -n todo-app

# Check OOMKill events
kubectl get events -n todo-app | grep OOMKilled
```

**Solutions**:

1. **Increase Memory Limits**
   ```yaml
   resources:
     limits:
       memory: 2Gi  # Increase limit
   ```

2. **Fix Memory Leaks**
   - Profile memory usage
   - Fix leaks in code
   - Implement proper cleanup

---

## Kafka/Event Issues

### Kafka Pods Not Starting

**Symptoms**: Kafka brokers stuck in CrashLoopBackOff

**Diagnosis**:
```bash
kubectl logs -n todo-app kafka-0 -c kafka
kubectl logs -n todo-app zookeeper-0
```

**Solutions**:

1. **Wait for ZooKeeper**
   ```bash
   # Ensure ZooKeeper is running first
   kubectl wait --for=condition=ready pod -l component=zookeeper -n todo-app --timeout=300s
   ```

2. **Check Storage**
   ```bash
   # Verify PVCs are bound
   kubectl get pvc -n todo-app | grep kafka
   ```

### Events Not Being Published

**Symptoms**: No events in Kafka topics

**Diagnosis**:
```bash
# Check backend logs for publish errors
kubectl logs -n todo-app -l component=backend | grep "publish"

# List Kafka topics
kubectl exec -n todo-app kafka-0 -c kafka -- \
  kafka-topics.sh --bootstrap-server localhost:9092 --list

# Consume from topic
kubectl exec -n todo-app kafka-0 -c kafka -- \
  kafka-console-consumer.sh --bootstrap-server localhost:9092 \
  --topic task.created --from-beginning --max-messages 10
```

**Solutions**:

1. **Create Topics Manually**
   ```bash
   kubectl exec -n todo-app kafka-0 -c kafka -- \
     kafka-topics.sh --bootstrap-server localhost:9092 \
     --create --topic task.created --partitions 3 --replication-factor 3
   ```

2. **Check Dapr Configuration**
   ```bash
   kubectl get component -n todo-app
   kubectl describe component pubsub -n todo-app
   ```

### High Event Latency

**Symptoms**: Events processed slowly (>100ms p95)

**Diagnosis**:
```bash
# Check Kafka lag
kubectl exec -n todo-app kafka-0 -c kafka -- \
  kafka-consumer-groups.sh --bootstrap-server localhost:9092 \
  --describe --group todo-app-consumer-group

# Check Kafka metrics
kubectl port-forward -n todo-app kafka-0 9308:9308
curl http://localhost:9308/metrics | grep kafka
```

**Solutions**:

1. **Increase Partitions**
   ```bash
   kubectl exec -n todo-app kafka-0 -c kafka -- \
     kafka-topics.sh --bootstrap-server localhost:9092 \
     --alter --topic task.created --partitions 6
   ```

2. **Scale Consumers**
   ```bash
   # Increase backend replicas (more consumers)
   kubectl scale deployment/backend -n todo-app --replicas=5
   ```

---

## Dapr Issues

### Dapr Sidecar Not Injected

**Symptoms**: Pods missing Dapr sidecar container

**Diagnosis**:
```bash
# Check pod containers
kubectl get pod <pod-name> -n todo-app -o jsonpath='{.spec.containers[*].name}'

# Check Dapr installation
kubectl get pods -n dapr-system
```

**Solutions**:

1. **Verify Dapr Annotations**
   ```yaml
   annotations:
     dapr.io/enabled: "true"
     dapr.io/app-id: "backend"
     dapr.io/app-port: "8000"
   ```

2. **Reinstall Dapr**
   ```bash
   dapr uninstall --kubernetes
   dapr init --kubernetes --wait
   ```

### Dapr Service Invocation Fails

**Symptoms**: Cannot invoke services via Dapr

**Diagnosis**:
```bash
# Check Dapr components
kubectl get components -n todo-app

# Test Dapr invocation
kubectl exec -n todo-app deployment/backend -c backend -- \
  curl http://localhost:3500/v1.0/invoke/frontend/method/health
```

**Solutions**:

1. **Verify Dapr Configuration**
   ```bash
   kubectl get configuration dapr-config -n todo-app -o yaml
   ```

2. **Check Network Policies**
   ```bash
   # Ensure Dapr ports are allowed
   kubectl get networkpolicy -n todo-app
   ```

---

## Ingress/TLS Issues

### Ingress Not Getting External IP

**Symptoms**: Ingress `ADDRESS` field empty

**Diagnosis**:
```bash
kubectl get ingress -n todo-app
kubectl describe ingress todo-app-ingress -n todo-app
```

**Solutions**:

1. **Check Ingress Controller**
   ```bash
   kubectl get pods -n ingress-nginx
   kubectl logs -n ingress-nginx -l app.kubernetes.io/component=controller
   ```

2. **Verify Cloud Provider LoadBalancer**
   ```bash
   # Check LoadBalancer service
   kubectl get svc -n ingress-nginx
   ```

### TLS Certificate Not Issued

**Symptoms**: Certificate stuck in Pending

**Diagnosis**:
```bash
kubectl get certificate -n todo-app
kubectl describe certificate todo-app-tls -n todo-app
kubectl get certificaterequest -n todo-app
kubectl logs -n cert-manager -l app=cert-manager
```

**Solutions**:

1. **Check DNS Configuration**
   ```bash
   # Verify DNS points to ingress IP
   nslookup todo-app.example.com
   ```

2. **Use Staging First**
   ```yaml
   annotations:
     cert-manager.io/cluster-issuer: letsencrypt-staging
   ```

3. **Manually Trigger Renewal**
   ```bash
   kubectl delete certificaterequest -n todo-app --all
   kubectl delete secret todo-app-tls -n todo-app
   kubectl delete certificate todo-app-tls -n todo-app
   kubectl apply -f kubernetes-deployment.yaml
   ```

---

## Auto-Scaling Issues

### HPA Not Scaling

**Symptoms**: HPA exists but doesn't scale

**Diagnosis**:
```bash
kubectl get hpa -n todo-app
kubectl describe hpa frontend-hpa -n todo-app
```

**Solutions**:

1. **Metrics Server Not Installed**
   ```bash
   # Install metrics-server
   kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml

   # Verify installation
   kubectl top nodes
   ```

2. **Resource Requests Not Defined**
   ```yaml
   resources:
     requests:
       cpu: 100m  # Required for HPA
       memory: 256Mi
   ```

3. **Test Load**
   ```bash
   # Generate load to trigger scaling
   kubectl run load-generator --rm -it --image=busybox -n todo-app -- /bin/sh -c \
     "while true; do wget -q -O- http://backend-service:8000/health; done"
   ```

---

## Monitoring & Logging

### No Logs Visible

**Symptoms**: `kubectl logs` returns empty

**Solutions**:

```bash
# Check pod status
kubectl get pod <pod-name> -n todo-app

# Check previous container logs
kubectl logs <pod-name> -n todo-app --previous

# Check all containers in pod
kubectl logs <pod-name> -n todo-app --all-containers
```

### Metrics Not Available

**Symptoms**: Prometheus not scraping metrics

**Solutions**:

```bash
# Verify Prometheus annotations
kubectl get pod <pod-name> -n todo-app -o yaml | grep -A 3 prometheus.io

# Check ServiceMonitor
kubectl get servicemonitor -n todo-app
```

---

## Emergency Procedures

### Complete System Failure

```bash
# 1. Check cluster health
kubectl get nodes
kubectl get componentstatuses

# 2. Check critical pods
kubectl get pods -n kube-system

# 3. Restart critical components
kubectl rollout restart deployment/coredns -n kube-system
kubectl rollout restart deployment/metrics-server -n kube-system

# 4. Restart application
kubectl rollout restart deployment --all -n todo-app
```

### Rollback Deployment

```bash
# View deployment history
kubectl rollout history deployment/backend -n todo-app

# Rollback to previous version
kubectl rollout undo deployment/backend -n todo-app

# Rollback to specific revision
kubectl rollout undo deployment/backend -n todo-app --to-revision=2
```

---

## Support Contacts

- **Documentation**: https://todo-app.example.com/docs
- **GitHub Issues**: https://github.com/todo-app/issues
- **Email**: admin@todo-app.example.com
- **Slack**: #todo-app-support
- **On-Call**: +1-XXX-XXX-XXXX

---

**Last Updated**: 2024-12-26
**Version**: 2.0.0
