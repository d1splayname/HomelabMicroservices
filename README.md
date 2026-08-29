# HomelabMicroservices
Various useful microservices ran on my homelab

## Setup commands

```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Updating requirements

install new libraries, then:

```
pip freeze > requirements.txt
```

Requirements:
MariaDB Connector/C

Linux
```
sudo apt install libmariadb-dev libmariadb-dev-compat
```