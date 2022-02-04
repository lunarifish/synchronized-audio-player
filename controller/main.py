import tkinter as tk
import variables as gl
from backend import sendData

gl._init()
window = tk.Tk()

server_ip_text = tk.Label(window, text = "Host").grid()
server_ip = tk.Entry(window)
server_ip.grid()

server_port_text = tk.Label(window, text = "Port").grid()
server_port = tk.Entry(window)
server_port.grid()

song_url_text = tk.Label(window, text = "URL").grid()
song_url = tk.Entry(window)
song_url.grid()


def connect():
    gl.set("ip", server_ip.get())
    gl.set("port", server_port.get())
    print("Host information set")

def update():
    print("Message sent")
    try:
        sendData(gl.get("ip"), int(gl.get("port")), song_url.get())
    except:
        print("No reply from server")

connect = tk.Button(window, text = "Connect", command = connect).grid()
update = tk.Button(window, text = "Update", command = update).grid()

tk.mainloop()