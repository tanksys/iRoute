# Deploy and Test the IPC Version of Excamera

This guide walks through deploying the Excamera (IPC version) application functions, testing the workflow, and cleaning up.

---

## 1. Prepare Host Mount Directory for IPC

Create a directory on the host that will be mounted into the pods for IPC, and set ownership:

```bash
sudo mkdir -p /mnt/excamera
sudo chown 100:101 /mnt/excamera
```

This directory will be used by the Excamera functions to share IPC memory.

## 2. Deploy the Centralized Coordinator

Export the node name for deploying functions, i.e., the node for mounting in Step 1:

```bash 
export TARGET_NODE=<node_name>
```

Deploy the coordination function `excamera-cc`, which handles IPC-based direct connections between functions. Also, verify that the pod is running:

```bash
kubectl apply -f excamera-cc.yml
kubectl get pods | grep excamera-cc
```

Ensure the pod is in `Running` state.

## 3. Deploy Excamera Functions

Deploy all Excamera functions that communicate over IPC:

```bash
kubectl apply -f excamera-funcs.yml
kubectl get pods -n openfaas-fn
```

Check that all pods are in `Running` state before proceeding.

## 4. Deploy the Workflow Entry Function

Deploy the entry function of the workflow:

```bash
kubectl apply -f excamera-entry.yml
kubectl get pods | grep excamera-entry
```

Make sure the `excamera-entry` pod is running.

## 5. Test the Workflow Execution

Test the workflow by sending a POST request with JSON parameters:
- `n`: number of test requests
- `st`: interval between requests in seconds

```bash
curl -d '{"n": 10, "st": 1}' http://127.0.0.1:31112/function/excamera-entry
```

The function will return the average and P99 latency of the requests.

## 6. Remove Deployed Functions

Finally, remove all deployed functions to clean up the cluster:

```bash
kubectl delete -f excamera-entry.yml
kubectl delete -f excamera-cc.yml
kubectl delete -f excamera-funcs.yml
```

Remove the IPC mount directory on the host:
```bash
sudo rm -rf /mnt/excamera
```
