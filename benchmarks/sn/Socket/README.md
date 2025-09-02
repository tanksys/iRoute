# Deploy and Test the Socket Version of Social Network

This guide walks through deploying the Social Network (socket version) application functions, initializing the database, testing the workflow, and cleaning up.

---

## 1. Deploy Database Operation Function

Deploy `sn-db-op` function:

```bash
kubectl apply -f sn-db-op.yml
```

## 2. Initialize the Database

Use `curl` to initialize the database. Set the POST parameter to `1`:

```bash
curl -d 1 http://127.0.0.1:31112/function/sn-db-op
```

This will prepare the database for the Social Network application.

## 3. Deploy the Centralized Coordinator

Deploy the coordination function `sn-cc`, which handles socket-based direct connections between functions. Also, verify that the pod is running:

```bash
kubectl apply -f sn-cc.yml
kubectl get pods | grep sn-cc
```

Ensure the pod is in `Running` state.

## 4. Deploy Social Network Functions

Deploy all Social Network functions that communicate over sockets:

```bash
kubectl apply -f sn-funcs.yml
kubectl get pods -n openfaas-fn
```

Check that all pods are in `Running` state before proceeding.

## 5. Deploy the Workflow Entry Function

Deploy the entry function of the workflow:

```bash
kubectl apply -f sn-entry.yml
kubectl get pods | grep sn-entry
```

Make sure the `sn-entry` pod is running.

## 6. Test the Workflow Execution

Test the workflow by sending a POST request with JSON parameters:
- `n`: number of test requests
- `st`: interval between requests in seconds

```bash
curl -d '{"n": 10, "st": 0.2}' http://127.0.0.1:31112/function/sn-entry
```

The function will return the average and P99 latency of the requests.


## 7. Clean Up the Database

After testing, clean up the database by sending a POST request with `0`:

```bash
curl -d 0 http://127.0.0.1:31112/function/sn-db-op
```

This removes any generated test results from the database.

## 8. Remove Deployed Functions

Finally, remove all deployed functions to clean up the cluster:

```bash
kubectl delete -f sn-entry.yml
kubectl delete -f sn-cc.yml
kubectl delete -f sn-funcs.yml
kubectl delete -f sn-db-op.yml
```
