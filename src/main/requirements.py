import subprocess
import sys

required = ['pandas', 'openpyxl', 'jinja2']

for package in required:
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])
