# MLoC - Machine Learning on Cluster

Machine learning as a Service solution.

## Quickstart

```bash
python mloc/mloc.py
```

## Examples

### Model Definition

```bash
curl -H "Content-Type: application/json" -X POST http://127.0.0.1:5000/networks --data @examples/densenet.json
```

### Model Fitting

```bash
curl -H "Content-Type: application/json" -X POST http://127.0.0.1:5000/fits --data @examples/densefit.json
```

### Model Evaluation

```bash
curl -H "Content-Type: application/json" -X POST http://127.0.0.1:5000/evaluations --data @examples/denseeval.json
```

### Query Model

```bash
curl -H "Content-Type: application/json" -X POST http://127.0.0.1:5000/predictions --data @examples/densepredict.json
```

## Documentation

To build documentation run `make html` in the [docs](./docs) directory.