# nr-utils

Steps to setup and run Nornir utilities on a new linux installation

## Prerequisites

Ensure you have the following installed on your system:

- Python 3.x
- pip (Python package installer)

## Setting Up the Project

### 1. Clone the repository

```bash
git clone https://github.com/JTIE-6EE7/nr-utils.git

cd nr-utils
```
### 2. Create Virtual Environment and install Python modules
```bash
python3 -m venv nornir

source nornir/bin/activate

pip install --upgrade pip

pip install -r requirements.txt
```

### 3. Set credentials in your Environment Variables 

Replace "USR" and "PWD" with your actual credentials

```bash
export nornir_usr=USR
export nornir_pwd=PWD
```
### 4: Update inventory in hosts.yaml

```yaml
---
n9k-core-1:
  hostname: 10.95.0.1
n9k-core-2:
  hostname: 10.95.0.11
```
### 5: Update platform in hosts.yaml (if needed)

```yaml
---
  platform: nxos
```
