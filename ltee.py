#doit communiquer avec le serveur pour envoyer le fichier en envoie direct, 
#et ce servir de la connection (adresse port) avec les variables d'environement avec os.environ

import os
import subprocess
import sys

env = dict(os.environ)
try:
    addr = env["addr"]
    port = env["port"]
except:
    sys.exit(-1)

p = subprocess.Popen("tee result", 
                    shell=True,
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT) 

fileltee = open('tee result','r+')

