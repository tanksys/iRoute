# Deploy and Test the RDMA Version of Excamera

This guide walks through deploying the Excamera (RDMA version) application functions, testing the workflow, and cleaning up.

---


## 1. Deploy the Centralized Coordinator

Deploy the coordination function `excamera-cc`, which handles RDMA-based direct connections between functions. Also, verify that the pod is running.

If your RDMA device matches the expected default configuration (i.e., `mlx5_1`), simply deploy the function:

```bash
kubectl apply -f excamera-cc.yml
```

If the detected RDMA device is different, please update the value of `rdma.ib_dev` in `excamera-cc/workflow.json`, and replace `DOCKER_USERNAME` (i.e., `tjulym`) with yours, then build, push, and deploy using:

```bash
kubectl up -f excamera-cc.yml
```


Ensure the pod is in `Running` state.

```bash
kubectl get pods | grep excamera-cc
```


## 2. Deploy Excamera Functions

Deploy all Excamera functions that communicate over RDMA.

If your RDMA device matches the expected default configuration (i.e., `mlx5_1`), simply deploy the functions:

```bash
kubectl apply -f excamera-funcs.yml
```

If the detected RDMA device is different, please update the value of `rdma.ib_dev` in `workflow.json` of each function in `excamera-funcs.yml`, and replace `DOCKER_USERNAME` (i.e., `tjulym`) with yours, then build, push, and deploy using:

```bash
kubectl up -f excamera-funcs.yml
```

Check that all pods are in `Running` state before proceeding.

```bash
kubectl get pods -n openfaas-fn
```

## 3. Deploy the Workflow Entry Function

Deploy the entry function of the workflow:

```bash
kubectl apply -f excamera-entry.yml
kubectl get pods | grep excamera-entry
```

Make sure the `excamera-entry` pod is running.

## 4. Test the Workflow Execution

Test the workflow by sending a POST request with JSON parameters:
- `n`: number of test requests
- `st`: interval between requests in seconds

```bash
curl -d '{"n": 10, "st": 1}' http://127.0.0.1:31112/function/excamera-entry
```

The function will return the average and P99 latency of the requests.



## 5. Remove Deployed Functions

Finally, remove all deployed functions to clean up the cluster:

```bash
kubectl delete -f excamera-entry.yml
kubectl delete -f excamera-cc.yml
kubectl delete -f excamera-funcs.yml
```
