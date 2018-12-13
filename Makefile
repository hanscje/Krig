
PY        = python3
LOCALHOST = 127.0.0.1

IP        = $(LOCALHOST)
PORT      = 5050

CLIENT    = client.py
SERVER    = server.py
NETWORK   = network.py


.PHONY: clean

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