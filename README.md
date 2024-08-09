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

pip install --upgrade

pip install -r requirements.txt
```

### 3. Set credentials in your Environment Variables 

Replace "USR" and "PWD" with your actual credentials

```bash
export nornir_usr=USR
export nornir_pwd=PWD
```
