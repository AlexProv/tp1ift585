import msgs
import select
import socket
import sys
import subprocess
import os
import uuid

class Client(object):

    def __init__(self, usager):
        super(Client, self).__init__()
        self.usager = usager


if len(sys.argv) < 3:
    print "Usage: {} <addr> <port>".format(__file__)
    sys.exit(1)
addr = sys.argv[1]
port = int(sys.argv[2])

ecouteur = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
ecouteur.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
ecouteur.bind((addr, port))
ecouteur.listen(5)
clients = { }

while True:
    clients_en_deconnexion = set([])
    pret, _, _ = select.select([ecouteur] + clients.keys(), [], [])
    if ecouteur in pret:
        client, _ = ecouteur.accept()
        msg_conn = msgs.recv(client)
        # set an id for the new client
        clients[client] = str(uuid.uuid4())
    for sock_client, client_id in clients.iteritems():
        if sock_client in pret:
            try:
                msg = msgs.recv(sock_client)
                if msg["op"] == "Command":
                    #bash = msg["texte"].split(' ',1)[1].rstrip()
                    bash = msg["texte"]

                    envi = dict(os.environ)
                    envi["addr"] = addr
                    envi["port"] = sys.argv[2]
                    envi["id"] = client_id
                    p = subprocess.Popen(bash, 
                                        shell=True,
                                        stdin=subprocess.PIPE,
                                        stdout=subprocess.PIPE,
                                        stderr=subprocess.STDOUT, 
                                        env = envi) 


                    for line in p.stdout.readlines():
                        msgs.send(
                                sock_client,
                                dict(
                                    op = "Message",
                                    texte = line
                                    )
                                )
                                
                #hack pour tester le file transfer. 
                if(msg["op"] == "ltee"):
                    filecontent = open(client_id + "_ltee")
                    msgs.send(sock_client,
                              dict(
                                  op = "FileDownload",
                                  FileName = "Tee",
                                  Content = filecontent.read()
                                  )
                              )
            except msgs.Erreur:
                clients_en_deconnexion.add(sock_client)
    for sock in clients_en_deconnexion:
        sock.close()
        del clients[sock]
# EOF