import subprocess
import unittest


def start_tests():
    subprocess.run(["python", "-m", "unittest", "discover", "tests"])