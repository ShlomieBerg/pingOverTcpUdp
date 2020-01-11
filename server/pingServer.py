"""
Server to receive Pings over TCP/UDP
"""
import socket
import threading
import time

import config as cfg


def udp_server():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp_socket:
        udp_socket.bind((cfg.HOST, cfg.UDP_PORT))
        while True:
            data, addr = udp_socket.recvfrom(cfg.BUFFER_SIZE)
            print("{}: New UDP connection from: {}".format(time.asctime(time.localtime()), addr))
            udp_socket.sendto(data, addr)


def tcp_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as tcp_socket:
        tcp_socket.bind((cfg.HOST, cfg.TCP_PORT))
        tcp_socket.listen(1)
        while True:
            conn, addr = tcp_socket.accept()
            print("{}: New TCP connection from: {}".format(time.asctime(time.localtime()), addr))
            t = threading.Thread(target=tcp_conn, name="tcp", args=(conn,))
            t.daemon = True
            t.start()


"""
handle tcp connection with client
"""


def tcp_conn(conn):
    with conn:
        while True:
            data = conn.recv(cfg.BUFFER_SIZE)
            if not data:
                break
            conn.sendall(data)


"""
main, opens 2 threads, one for udp the other for tcp, close server with kill
"""


def main():
    print("Server is up, listening on host: {}".format(cfg.HOST))
    tcp_listener = threading.Thread(target=tcp_server, name="tcp_server")
    udp_listener = threading.Thread(target=udp_server, name="udp_server")
    tcp_listener.daemon = True
    udp_listener.daemon = True
    tcp_listener.start()
    udp_listener.start()

    while True:
        pass


if __name__ == "__main__":
    main()