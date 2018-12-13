
PY        = python3
LOCALHOST = 127.0.0.1

IP        = $(LOCALHOST)
PORT      = 5050

GAME      = krig.py
ROUNDS    = 1
CLIENT    = client.py
SERVER    = server.py
NETWORK   = network.py


.PHONY: clean spill

spill:
	@echo 'Starting game...'
	$(PY) $(GAME) $(PORT) $(ROUNDS)

client: 
	@echo 'Connecting client to $(IP) on port $(PORT)'
	$(PY) $(CLIENT) $(PORT) $(IP)

server:
	@echo 'Running server on port $(PORT)'
	$(PY) $(SERVER) $(PORT)

network:
	@echo 'Running network file standalone.'
	$(PY) $(SERVER) $(NETWORK)

clean: 
	rm *.pyc