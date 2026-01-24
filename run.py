from watchfiles import watch, Change
import subprocess


def relevant(changes):
    for change, path in changes:
        if path.endswith(".py") or path.endswith(".kv"):
            return True
    return False


for changes in watch("."):
    if relevant(changes):
        subprocess.run(["python", "-m", "examples.progressindicator"])
