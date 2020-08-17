import subprocess
import time

proc = subprocess.Popen('pelican')
time.sleep(2)
proc.kill()