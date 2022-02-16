# synchronized-audio-player
[![State-of-the-art Shitcode](https://img.shields.io/static/v1?label=State-of-the-art&message=Shitcode&color=7B5804)](https://github.com/trekhleb/state-of-the-art-shitcode)
## server side
```
python main.py [server port] [controller port]
```
#### available commands
- list: list all connected clients
- status: show information of current playing audio
- ports [client ip(s)]: show used ports of specified client(s)
- stop: stop server
## client side
```
python main.py [server ip] [server port]
```
