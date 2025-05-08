import socket

server_host = '127.0.0.1'
server_port = 9999
recv_timeout = 10

def start_client():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(recv_timeout)
        try:
            s.connect((server_host, server_port))
            print('client connected')

            while True:
                try:
                    data = s.recv(1024)
                    if not data:
                        break

                    msg = data.decode()
                    if msg.startswith('ping:'):
                        token = msg.split(':')[1]
                        reply = f'pong:{token}'
                        s.sendall(reply.encode())
                        print('replied with', reply)
                    else:
                        print('unknown message', msg)

                except socket.timeout:
                    print('server timeout')
                    break

        except Exception as e:
            print('error', str(e))
        finally:
            print('client exited')

if __name__ == '__main__':
    start_client()
