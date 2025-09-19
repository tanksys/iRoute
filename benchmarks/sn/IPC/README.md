# Deploy and Test the IPC Version of Social Network

This guide walks through deploying the Social Network (IPC version) application functions, initializing the database, testing the workflow, and cleaning up.

---

## 1. Deploy Database Operation Function

Deploy `sn-db-op` function:

```bash
faas-cli deploy -f sn-db-op.yml
```

## 2. Initialize the Database

Use `curl` to initialize the database. Set the POST parameter to `1`:

```bash
curl -d 1 http://127.0.0.1:31112/function/sn-db-op
```

This will prepare the database for the Social Network application.

## 3. Prepare Host Mount Directory for IPC

Create a directory on the host that will be mounted into the pods for IPC, and set ownership:

```bash
sudo mkdir -p /mnt/sn
sudo chown 100:101 /mnt/sn
```

This directory will be used by the Social Network functions to share IPC memory.

## 4. Deploy the Centralized Coordinator

Export the node name for deploying functions, i.e., the node for mounting in Step 3:

```bash 
export TARGET_NODE=<node_name>
```

Deploy the coordination function `sn-cc`, which handles IPC-based direct connections between functions. Also, verify that the pod is running:

```bash
faas-cli deploy -f sn-cc.yml
kubectl get pods -n openfaas-fn | grep sn-cc
```

Ensure the pod is in `Running` state.

## 5. Deploy Social Network Functions

Deploy all Social Network functions that communicate over IPC:

```bash
faas-cli deploy -f sn-funcs.yml
kubectl get pods -n openfaas-fn
```

Check that all pods are in `Running` state before proceeding.

## 6. Deploy the Workflow Entry Function

Deploy the entry function of the workflow:

```bash
faas-cli deploy -f sn-entry.yml
kubectl get pods -n openfaas-fn | grep sn-entry
```

Make sure the `sn-entry` pod is running.

## 7. Test the Workflow Execution

Test the workflow by sending a POST request with JSON parameters:
- `n`: number of test requests
- `st`: interval between requests in seconds

```bash
curl -d '{"n": 10, "st": 0.2}' http://127.0.0.1:31112/function/sn-entry
```

The function will return the average and P99 latency of the requests.


## 8. Clean Up the Database

After testing, clean up the database by sending a POST request with `0`:

```bash
curl -d 0 http://127.0.0.1:31112/function/sn-db-op
```

This removes any generated test results from the database.

## 9. Remove Deployed Functions

Finally, remove all deployed functions to clean up the cluster:

```bash
faas-cli delete -f sn-entry.yml
faas-cli delete -f sn-cc.yml
faas-cli delete -f sn-funcs.yml
faas-cli delete -f sn-db-op.yml
```

Remove the IPC mount directory on the host:
```bash
sudo rm -rf /mnt/sn
```
