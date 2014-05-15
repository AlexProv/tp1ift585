#doit communiquer avec le serveur pour envoyer le fichier en envoie direct, 
#et ce servir de la connection (adresse port) avec les variables d'environement avec os.environ

import os
import subprocess
import sys

env = dict(os.environ)

try:
    addr = env["addr"]
    port = env["port"]
    uid = env["id"]
except:
    sys.exit(-1)

p = subprocess.Popen("tee result", 
                    shell=True,
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT) 
p.communicate()#wait for tee to be done


conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
conn.connect((addr, port))
msgs.send(conn, dict(op = "Connexion", usager = usager))
#pret, _, _ = select.select([sys.stdin, conn], [], [])

try:
    fileltee = open('tee result','r+')
    msgs.send(conn,dict(
        op="SendFile",
        FileName = "Tee",
        Content = fileltee.read(), #contenu du fichier de ltee 
        id = uid
    ))
except: 
    sys.exit(-1)

