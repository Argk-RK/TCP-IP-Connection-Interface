import tarfile
import subprocess

file = tarfile.open('Flask-0.10.1.tar.gz')
file.extractall()
file.close()
dir_name = 'Flask-0.10.1'

subprocess.call(['pip', 'install', dir_name, 'processing'])
