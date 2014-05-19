import msgs
import select
import socket
import sys
import os
import subprocess


if len(sys.argv) < 3:
    print "Usage: {} <addr> <port>".format(__file__)
    sys.exit(1)
addr = sys.argv[1]
port = int(sys.argv[2])

conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
conn.connect((addr, port))
msgs.send(conn, dict(op = "Connexion"))
while True:
    pret, _, _ = select.select([sys.stdin, conn], [], [])
    if sys.stdin in pret:
        ligne = sys.stdin.readline()
        if len(ligne) == 0:
            conn.close()
            break
        elif ligne.startswith("./lcat"):
            envi = dict(os.environ)
            envi["addr"] = addr
            envi["port"] = sys.argv[2]
            envi["command"] = ligne

            p = subprocess.Popen(ligne,
                                shell=True,
                                stdin=subprocess.PIPE,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT,
                                env = envi)
            p.wait()

            client_server_split = ligne.split('>')
            server_split = client_server_split[1].replace(' ', '').replace('\n','')
            tempName = 'lcat_result'
            filecat = open(tempName,'r')
            msgs.send(conn,dict(
                op="UploadFile",
                FileName = server_split,
                Content = filecat.read()
            ))
            filecat.close()
            os.remove(tempName)
        else:    
            msgs.send(conn, dict(op = "Command", texte = ligne))

    if conn in pret:
        try:
            msg = msgs.recv(conn)
            #pour faire du download de fichier. 
            if msg["op"] == "FileDownload":
                fileName = msg["FileName"]
                con = msg["Content"]
                print con
                f = open(fileName,'w+')
                f.write(con)
                f.close()
            else:
                print msg["texte"].rstrip()

        except msgs.Erreur:
            print "*** Serveur down! ***"
            conn.close()
            break
# EOF