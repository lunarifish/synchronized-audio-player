# synchronized-audio-player
## server side
```
python main.py [client port] [controller port]
```
#### available commands
- list: list all connected clients
- status: show information of current playing audio
- ports [client ip(s)]: show used ports of specified client
- stop: stop server
## client side
```
python main.py [server ip] [server port]
```
