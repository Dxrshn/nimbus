# Runbook: Debugging

## Check pod status

```bash
kubectl get pods
kubectl describe pod <pod-name>
kubectl logs <pod-name>
kubectl logs <pod-name> --previous  # if pod crashed
