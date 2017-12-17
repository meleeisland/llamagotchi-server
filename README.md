# llamagotchi
Llamagotchi è un'applicazione server-client dockerizzata basata su python2 in cui puoi gestire la vita di un Lama, dargli da mangiare etc tramite comandi testuali

- per costruire l'immagine del server:
 `docker build -t meleeisland/llamagotchi .`
- per eseguire l'immagine del server:
 `docker run -e PORT=8080 -p 8080:8080 -h 0.0.0.0 -d --name llamagotchi meleeisland/llamagotchi`

- per eseguire il client:
 `python2.7 main.py`

## Messaggi al server ##

		d,l = send(clientsocket,"new","",uid) # New llama
		d,l = send(clientsocket,"gname","",uid) #Get Name
		d,l = send(clientsocket,"sname",NEWNAME,uid) #Set Name
		d,l = send(clientsocket,"pet","",uid) #Pet
		d,l = send(clientsocket,"ghappy","",uid) #Get Happiness
		d,l = send(clientsocket,"save","",uid) #Save
		d,l = send(clientsocket,"logout","",uid) #Logout

## Todo ##
- Librerie per stampare llama a terminale
- Immagini docker per server e client

