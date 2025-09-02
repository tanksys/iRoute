# Deploy and Test the RDMA Version of Financial Industry Regulatory Authority (FINRA)

This guide walks through deploying the FINRA (RDMA version) application functions, testing the workflow, and cleaning up.

---


## 1. Deploy the Centralized Coordinator

Deploy the coordination function `finra-cc`, which handles RDMA-based direct connections between functions. Also, verify that the pod is running.

If your RDMA device matches the expected default configuration (i.e., `mlx5_1`), simply deploy the function:

```bash
kubectl apply -f finra-cc.yml
```

If the detected RDMA device is different, please update the value of `rdma.ib_dev` in `finra-cc/workflow.json`, and replace `DOCKER_USERNAME` (i.e., `tjulym`) with yours, then build, push, and deploy using:

```bash
kubectl up -f finra-cc.yml
```


Ensure the pod is in `Running` state.

```bash
kubectl get pods | grep finra-cc
```


## 2. Deploy FINRA Functions

Deploy all FINRA functions that communicate over RDMA.

If your RDMA device matches the expected default configuration (i.e., `mlx5_1`), simply deploy the functions:

```bash
kubectl apply -f finra-funcs.yml
```

If the detected RDMA device is different, please update the value of `rdma.ib_dev` in `workflow.json` of each function in `finra-funcs.yml`, and replace `DOCKER_USERNAME` (i.e., `tjulym`) with yours, then build, push, and deploy using:

```bash
kubectl up -f finra-funcs.yml
```

Check that all pods are in `Running` state before proceeding.

```bash
kubectl get pods -n openfaas-fn
```

## 3. Deploy the Workflow Entry Function

Deploy the entry function of the workflow:

```bash
kubectl apply -f finra-entry.yml
kubectl get pods | grep finra-entry
```

Make sure the `finra-entry` pod is running.

## 4. Test the Workflow Execution

Test the workflow by sending a POST request with JSON parameters:
- `n`: number of test requests
- `st`: interval between requests in seconds

```bash
curl -d '{"n": 10, "st": 0.2}' http://127.0.0.1:31112/function/finra-entry
```

The function will return the average and P99 latency of the requests.



## 5. Remove Deployed Functions

Finally, remove all deployed functions to clean up the cluster:

```bash
kubectl delete -f finra-entry.yml
kubectl delete -f finra-cc.yml
kubectl delete -f finra-funcs.yml
```
