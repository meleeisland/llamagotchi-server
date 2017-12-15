import os
from src.LlamaClass import Llama

def new_game_message():
	return 'New Game';

# inizializzazione Llama
lama = Llama('Calogero')

saveFile = 'save.json';
if (os.path.isfile(saveFile)):
	lama.load(saveFile)
else:
	print new_game_message()
	print 'baaah'


while True :
	cmd = raw_input("LlamaGotchi $> ")
	print cmd
	if (cmd == 'setname'):
		name = raw_input("LlamaGotchi - Scegli il nome $> ")
		lama.setName(name)
		print 'Il nuovo nome: ' + lama.getName()
	if (cmd == 'newllama'):lama = Llama('')
	if (cmd == 'getname'):print lama.getName()
	if (cmd == 'save'):lama.save(saveFile)
	if (cmd == 'exit'):exit(0)
