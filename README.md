# MLoC - Machine Learning on Cluster

Machine learning as a Service solution.

## Quickstart

```bash
python mloc/mloc.py
```

## Examples

### Model Configuration

```bash
curl -H "Content-Type: application/json" -X POST http://127.0.0.1:5000/networks --data @examples/densenet.json
```

### Model Initialization

```bash
curl -X POST http://127.0.0.1:5000/networks/5b72bbf767134c35bb13b5ad/init
```

### Model Fitting

```bash
curl -H "Content-Type: application/json" -X POST http://127.0.0.1:5000/networks/5b72bbf767134c35bb13b5ad/fit --data @examples/densefit.json
```

### Model Evaluation

```bash
curl -H "Content-Type: application/json" -X POST http://127.0.0.1:5000/networks/5b72bbf767134c35bb13b5ad/evaluate --data @denseeval.json
```

### Query Model

```bash
curl -H "Content-Type: application/json" -X POST http://127.0.0.1:5000/networks/5b72bbf767134c35bb13b5ad/predict --data @densepredict.json
```