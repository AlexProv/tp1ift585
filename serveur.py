import msgs
import select
import socket
import sys
import subprocess

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
        clients[client] = Client(msg_conn["usager"])
    for sock_client, usager in clients.iteritems():
        if sock_client in pret:
            try:
                msg = msgs.recv(sock_client)
                if msg["op"] == "Command":
                    #bash = msg["texte"].split(' ',1)[1].rstrip()
                    bash = msg["texte"]
                    p = subprocess.Popen(bash, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT) 
                    for line in p.stdout.readlines():
                        for sock_dest, dest in clients.iteritems():
                            try:
                                msgs.send(
                                        sock_dest,
                                        dict(
                                            op = "Message",
                                            usager = "System",
                                            texte = line
                                            )
                                        )
                            except msgs.Erreur:
                                clients_en_deconnexion.add(sock_dest)
            except msgs.Erreur:
                clients_en_deconnexion.add(sock_client)
    for sock in clients_en_deconnexion:
        sock.close()
        del clients[sock]
# EOF