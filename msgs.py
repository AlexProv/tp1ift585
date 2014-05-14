import json
import struct


class Erreur(Exception):
    pass

def serial(msg):
  msg_json = json.dumps(msg)
  taille = len(msg_json)
  return struct.pack("!H", taille) + msg_json

def send(sock, msg):
  msg_json = serial(msg)
  while len(msg_json) > 0:
    n = sock.send(msg_json)
    if n == 0:
        raise Erreur()
    msg_json = msg_json[n:]

def recv_exact(sock, n):
  r = ""
  while n > 0:
    s = sock.recv(n)
    if len(s) == 0:
        raise Erreur()
    r += s
    n -= len(s)
  return r

def recv(sock):
  H = recv_exact(sock, 2)
  taille = struct.unpack("!H", H)[0]
  msg_json = recv_exact(sock, taille)
  return json.loads(msg_json)

