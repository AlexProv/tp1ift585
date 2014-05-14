import msgs
import select
import socket
import sys
import subprocess

class Client(object):

    def __init__(self, usager):
        super(Client, self).__init__()
        self.usager = usager
        self.groupe = "lobby"


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
                if msg["op"] == "Message":
                    for sock_dest, dest in clients.iteritems():
                        if dest.groupe == usager.groupe:
                            try:
                                msgs.send(
                                        sock_dest,
                                        dict(
                                            op = "Message",
                                            usager = usager.usager,
                                            texte = msg["texte"]
                                            )
                                        )
                            except msgs.Erreur:
                                clients_en_deconnexion.add(sock_dest)
                elif msg["op"] == "Groupe":
                    usager.groupe = msg["groupe"]
                elif msg["op"] == "Command":
                    bash = msg["texte"].split(' ',1)[1].rstrip()
                    teeSave = " | tee temp_result"
                    p = subprocess.Popen(bash+teeSave, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT) 
                    for line in p.stdout.readlines():
                        for sock_dest, dest in clients.iteritems():
                            if dest.groupe == usager.groupe:
                                try:
                                    msgs.send(
                                            sock_dest,
                                            dict(
                                                op = "Message",
                                                usager = "System",
                                                texte = line
                                                )
                                            )
                                    
                                #code to read file ltee
                                path = "ltee"
                                fileopen = open(path,'r+')
                                for(line in fileopen):
                                    print line    
                                #send line ? 

                                except msgs.Erreur:
                                    clients_en_deconnexion.add(sock_dest)
                elif msg["op"] == "Liste":
                    try:
                        msgs.send(
                                sock_client,
                                dict(
                                    op = "Message",
                                    usager = "MASTER",
                                    texte = "\n".join(set([u.groupe for u in clients.itervalues()]))
                                    )
                                )
                    except msgs.Erreur:
                        clients_en_deconnexion.add(sock_client)
            except msgs.Erreur:
                clients_en_deconnexion.add(sock_client)
    for sock in clients_en_deconnexion:
        sock.close()
        del clients[sock]


# EOF