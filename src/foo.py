
import subprocess


script = "main.py -n={} -c={} -s={}".format('Naomi', 'Red', 'L')
proc = subprocess.Popen(['gnome-terminal', '-x', 'python', script], shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT,
          close_fds=False)
proc.wait()