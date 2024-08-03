import socket
import threading

username = input("Introduzca su nombre: ")

host = '127.0.0.1'
port = 55555

#creacion del socket del cliente y conexion al servidor
cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    cliente.connect((host, port))
    print("Connected to the server")
except Exception as e:
    print(f"Unable to connect: {e}")

#funcion para recibir mensajes
def recibir_mensajes():
    while True:
        try:
            mensaje = cliente.recv(1024).decode('utf-8')
            if mensaje == "@username":
                cliente.send(username.encode("utf-8"))
            else:
                print(mensaje)
        except Exception as e:
            print(f"Error receiving messages: {e}")
            cliente.close()
            break

#funcion para escribir y enviar mensajes
def escribir_mensajes():
    while True:
        mensaje = f"{username}: {input('')}"
        try:
            cliente.send(mensaje.encode('utf-8'))
        except Exception as e:
            print(f"Error sending messages: {e}")
            cliente.close()
            break

#creacion y arranque de hilos
recibir_thread = threading.Thread(target=recibir_mensajes)
recibir_thread.start()

escribir_thread = threading.Thread(target=escribir_mensajes)
escribir_thread.start()