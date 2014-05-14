#! mettre le path de python ici

#doit communiquer avec le serveur pour envoyer le fichier en envoie direct, 
#et ce servir de la connection (adresse port) avec les variables d'environement avec os.environ

path = "ltee"
fileopen = open(path,'r+')
for(line in fileopen):
    print line    