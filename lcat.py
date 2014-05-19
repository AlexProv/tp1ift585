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
    command_line = env["command"]
except:
    sys.exit(-1)
tempName = 'lcat_result'
client_server_split = command_line.split('>')
client_split = client_server_split[0].replace("./lcat", "cat")
server_split = client_server_split[1].replace(' ', '')

p = subprocess.Popen(
        client_split + " > " + tempName,
        shell = True,
        stdin = subprocess.PIPE,
        stdout = subprocess.PIPE,
        stderr = subprocess.STDOUT
        )
p.wait()

#check what's in the pipe
#for line in sys.stdin:
"""
conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
conn.connect((addr, port))
msgs.send(conn, dict(op = "Connexion"))
try:
    while True:
        pret, _, _ = select.select([conn], [], [])
        if conn in pret:
            filecat = open(tempName,'r')
            msgs.send(conn,dict(
                op="UploadFile",
                FileName = server_split,
                Content = "MACACA IS WATCHING YOU"#filecat.readall()
            ))
            filecat.close()
            #os.remove(tempName)
            break
except:
    sys.exit(-1)
    """

"""
p = subprocess.Popen(bash,
                    shell=True,
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT)
out, err = p.communicate()#wait for tee to be done
"""