import os.path
import subprocess

from src.settings import BASE_DIR


TEST_DIR = os.path.join(BASE_DIR, "tests")


def start_tests():
    subprocess.run(["python", "-m", "unittest", "discover", "tests"])
