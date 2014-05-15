#doit communiquer avec le serveur pour envoyer le fichier en envoie direct, 
#et ce servir de la connection (adresse port) avec les variables d'environement avec os.environ

import os
import subprocess
import sys
import socket
import msgs
import select

env = dict(os.environ)

try:
    addr = env["addr"]
    port = int(env["port"])
    uid = env["id"]
except:
    sys.exit(-1)
tempName = 'result'+uid
bash = "tee " + tempName

#check what's in the pipe
#for line in sys.stdin:

con = sys.stdin.read()

fileltee = open(tempName,'w+')
fileltee.write(sys.stdin.read())

conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
conn.connect((addr, port))
msgs.send(conn, dict(op = "Connexion"))
try:
    fileltee = open(tempName,'r+')
    msgs.send(conn,dict(
        op="SendFile",
        FileName = "Tee",
        Content = con, #contenu du fichier de ltee 
        id = uid
    ))
    os.remove(tempName)
except: 
    sys.exit(-1)

"""
p = subprocess.Popen(bash,
                    shell=True,
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT)
out, err = p.communicate()#wait for tee to be done
"""