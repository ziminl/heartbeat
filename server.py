import socket
import threading
import time

HOST = '0.0.0.0'
PORT = 9999
TIMEOUT = 10

clients = {}

def client_handler(conn, addr):
    print(f"connected {addr}")
    conn.settimeout(TIMEOUT)
    last_heartbeat = time.time()
    try:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            message = data.decode()
            if message == 'ping':
                conn.sendall(b'pong')
                last_heartbeat = time.time()
                print(f"beat {addr} -> ping/pong")
            elif time.time() - last_heartbeat > TIMEOUT:
                print(f"timeout {addr}")
                break
    except socket.timeout:
        print(f"[타임아웃 예외] {addr}")
    except Exception as e:
        print(f"error {addr} - {e}")
    finally:
        conn.close()
        print(f"end {addr}")

def start_server():
    print("start")
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    try:
        while True:
            conn, addr = server_socket.accept()
            thread = threading.Thread(target=client_handler, args=(conn, addr), daemon=True)
            thread.start()
    finally:
        server_socket.close()

if __name__ == "__main__":
    start_server()
