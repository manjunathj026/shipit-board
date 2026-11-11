# ShipIt Board

![CI](https://github.com/manjunathj026/shipit-board/actions/workflows/ci.yml/badge.svg)

A small Python Flask app I'm taking through a complete DevSecOps pipeline,
from commit to Kubernetes on AWS. The page shows which version and commit
are running, so every deployment is visible.

## Run it locally

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt -r requirements-dev.txt
flask --app app run --port 8000
```

## Pipeline so far

- Linting with ruff
- Unit tests with a 90% coverage gate
- Docker image build, plus a smoke test of the running container
- `main` is protected: changes go through a pull request and must pass CI