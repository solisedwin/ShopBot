import subprocess

proc1 = subprocess.Popen(['gnome-terminal', '-x', 'python', 'main.py'])
proc2 = subprocess.Popen(['gnome-terminal', '-x', 'python', 'main.py'])
proc1.wait()
proc2.wait()