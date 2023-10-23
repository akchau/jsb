import subprocess


def start_tests():
    subprocess.run(["python", "-m", "unittest", "discover", "tests"])
