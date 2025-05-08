import socket
import threading
import time
import random
import string

host = '0.0.0.0'
port = 9999
heartbeat_interval = 5
timeout = 10

def generate_token(length):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def handle_client(conn, addr):
    print('connected', addr)
    conn.settimeout(timeout)
    try:
        while True:
            token = generate_token(8)
            message = f'ping:{token}'
            conn.sendall(message.encode())

            try:
                data = conn.recv(1024)
                if not data:
                    print('no data', addr)
                    break

                expected = f'pong:{token}'
                if data.decode() == expected:
                    print('valid response from', addr)
                else:
                    print('invalid response from', addr, '-', data.decode())
                    break

            except socket.timeout:
                print('timeout from', addr)
                break

            time.sleep(heartbeat_interval)

    except Exception as e:
        print('error with', addr, '-', str(e))
    finally:
        conn.close()
        print('disconnected', addr)

def start_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    s.listen()
    print('server started')

    while True:
        conn, addr = s.accept()
        threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()

if __name__ == '__main__':
    start_server()
