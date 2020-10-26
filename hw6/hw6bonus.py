import socket
import re
import os


def send_and_close(c, data_to_send):
    c.send(data_to_send.encode("utf-8"))
    c.close()


def parse_request(c):
    body = None
    data_str = ''
    while True:
        data = c.recv(1024)
        data_str += data.decode("utf-8")
        if data_str.endswith('\r\n\r\n'):
            break
    data_split = data_str.split('\r\n', 1)
    header = data_split[0]
    body = data_split[1] if len(data_split) > 1 else ''
    m = re.match("^((GET)|(PUT)|(DELETE)) /([a-zA-Z/_\.\-]+)$", header)
    if m is not None:
        req = m.group(1)
        filepath = m.group(5)
    else:
        return None, None, None
    return req, filepath, body


def get(c, filepath):
    if os.path.exists(filepath):
        data_to_send = "200 OK\r\n".encode("utf-8")
        with open(filepath, 'rb') as f:
            data_to_send += f.read()
        c.send(data_to_send)
        c.close()
    else:
        send_and_close(c, "404 Not found")


def put(c, filepath, body):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w') as f:
        f.write(body)
    send_and_close(c, '200 OK')


def delete(c, filepath):
    if os.path.exists(filepath):
        os.remove(filepath)
    send_and_close(c, '200 OK')


if __name__ == "__main__":
    s = socket.socket()
    port = 8080
    try:
        s.bind(("", port))
        s.listen()
        while True:
            c, addr = s.accept()
            req, filepath, body = parse_request(c)
            if req == 'GET':
                get(c, filepath)
            elif req == 'PUT':
                put(c, filepath, body)
            elif req == 'DELETE':
                delete(c, filepath)
            else:
                send_and_close(c, "400 Bad Request")
    finally:
        s.close()
