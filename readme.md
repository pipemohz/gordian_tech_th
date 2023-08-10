# Gordian technical interview
Software take home for backend developer skills evaluation.

## Installation 🔧

Clone the repository in your work folder.

## Basic configuration

### Prerequisites

* Python 3.10.x

### Create a virtual environment
```sh
python -m venv .venv
```
### Activate virtual environment

#### Windows
```sh
.venv\Scripts\activate
```
#### Linux
```sh
source .venv/bin/activate
```
### Download all packages required
```sh
pip install -r requirements.txt
```
### Create an environment file

You must create and setting up an .env file for the project configuration with variables according to .env.example
```dosini
# Gordian API
GORDIAN_API_URL =
GORDIAN_API_KEY =
```
### Run tasks
```sh
python task_1/script.py
python task_2/seat_parser.py
```