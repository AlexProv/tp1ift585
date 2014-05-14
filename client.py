import msgs
import select
import socket
import sys


if len(sys.argv) < 4:
    print "Usage: {} <addr> <port> <usager>".format(__file__)
    sys.exit(1)
addr = sys.argv[1]
port = int(sys.argv[2])
usager = sys.argv[3]

conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
conn.connect((addr, port))
msgs.send(conn, dict(op = "Connexion", usager = usager))
while True:
    pret, _, _ = select.select([sys.stdin, conn], [], [])
    if sys.stdin in pret:
        ligne = sys.stdin.readline()
        if len(ligne) == 0:
            conn.close()
            break
        else:
            if ligne.lstrip().startswith("#test"):
                #hack pour etre capable de tester le file transfere. c'est un bon example de comment faire.
                msgs.send(conn,dict(op = "test"))
            else:
                msgs.send(conn, dict(op = "Command", texte = ligne))

    if conn in pret:
        try:
            msg = msgs.recv(conn)
            #pour faire du download de fichier. 
            if msg["op"] == "FileDownload":
                fileName = msg["FileName"]
                teeFile = open(fileName,'w')
                teeFile.write(msg["Content"])
            else:
                print msg["usager"], "--", msg["texte"].rstrip()

        except msgs.Erreur:
            print "*** Serveur down! ***"
            conn.close()
            break
# EOF