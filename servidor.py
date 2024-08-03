import socket
import threading

#Asignacion de ip y puerto
host = '127.0.0.1'
port = 55555

#creacion y configuracion del socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

server.bind((host, port)) 
server.listen()
print(f"El servidor se esta ejecutando {host}:{port}")

clientes = [] 
usernames = [] 

#funcion de transmitir mensajes de todos los clientes
def transmitir(mensaje, _client): 
    for client in clientes:
        if client != _client:
            client.send(mensaje)

#funcion mensajes del cliente recibe mensaje del cliente y lo transmite a los demas
def manejar_mensajes(client):
    while True:
        try:
            mensaje = client.recv(1024) 
            transmitir(mensaje, client)
        except:
            index = clientes.index(client)
            username = usernames[index]
            transmitir(f"{username} Desconectado".encode('utf-8')) 
            clientes.remove(client)
            usernames.remove(username)
            client.close()
            break

#Acepta nuevos clientes y maneja la comunicacion inicial
def recibir_conexiones():
    while True:
        client, address = server.accept()

        client.send("@username".encode('utf-8'))
        username = client.recv(1024).decode('utf-8')

        clientes.append(client)
        usernames.append(username)

        print(f"{username} esta conectado con {str(address)}")

        mensaje = f"{username} Se conecto al chat!".encode('utf-8')
        transmitir(mensaje, client)
        client.send("Conectado al servidor".encode('utf-8'))

        thread = threading.Thread(target=manejar_mensajes, args=(client,))
        thread.start()

recibir_conexiones()

