import socket
import time

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 9999
INTERVAL = 3
TIMEOUT = 5
MAX_LOSS = 5

def start_client():
    loss_count = 0
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(TIMEOUT)
        try:
            s.connect((SERVER_HOST, SERVER_PORT))
            print("connected")
            while True:
                try:
                    s.sendall(b'ping')
                    data = s.recv(1024)
                    if data == b'pong':
                        print(" pong")
                        loss_count = 0
                    else:
                        print("???", data)
                except socket.timeout:
                    loss_count += 1
                    print(f"loss : {loss_count}")
                    if loss_count >= MAX_LOSS:
                        print("too many loss.")
                        break
                time.sleep(INTERVAL)
        except Exception as e:
            print(f"error {e}")
        finally:
            print("end")

if __name__ == "__main__":
    start_client()
