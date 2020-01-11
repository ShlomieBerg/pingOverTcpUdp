import socket
import time
import os
import sys

import config as cfg

"""
arguments validation
"""
# Required protocol
try:
    PROTOCOL = sys.argv[1]
except IndexError:
    print("Usage: pingClient.py PROTOCOL [TIMEOUT] [PACKET_SIZE] [PACKET_NUM]")
    sys.exit(1)

# Optional timeout
try:
    TIMEOUT = int(sys.argv[2])
except ValueError:
    print("Error: TIMEOUT Value Must be Integer:", sys.argv[3])
    sys.exit(1)
except IndexError:
    TIMEOUT = cfg.DEF_TIMEOUT
    pass

# Optional packet-size
try:
    PACKET_SIZE = int(sys.argv[3])
except ValueError:
    print("Error: PACKET_SIZE Value Must be Integer", sys.argv[3])
    sys.exit(1)
except IndexError:
    PACKET_SIZE = cfg.DEF_PACKET_SIZE
    pass

# Optional packet-number
try:
    PACKET_NUM = int(sys.argv[4])
except ValueError:
    print("Error: PACKET_NUM Value Must be Integer", sys.argv[3])
    sys.exit(1)
except IndexError:
    PACKET_NUM = cfg.DEF_PACKET_NUM
    pass


"""handler for UDP ping"""


def udp_ping():
    success = 0
    failure = 0
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    for pings in range(PACKET_NUM):
        message = os.urandom(PACKET_SIZE)
        sock.settimeout(TIMEOUT)
        send_time = time.time() * 1000
        sock.sendto(message, (cfg.HOST, cfg.UDP_PORT))
        try:
            data, addr = sock.recvfrom(cfg.BUFFER_SIZE)
            end_time = time.time()*1000
            diff = end_time - send_time
            if not data == message:
                raise ValueError("BAD RESPONSE")
            print("{} bytes from {} udp_seq={} time={} ms".format(PACKET_SIZE, cfg.HOST, pings+1, round(diff, 3)))
            success += 1
            time.sleep(1)
        except socket.timeout:
            print("PING REQUEST TIMEOUT")
            failure += 1

    return success, failure


"""handler for TCP ping"""


def tcp_ping():
    success = 0
    failure = 0
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((cfg.HOST, cfg.TCP_PORT))
        for pings in range(PACKET_NUM):
            message = os.urandom(PACKET_SIZE)
            send_time = time.time() * 1000
            sock.send(message)
            try:
                data = sock.recv(cfg.BUFFER_SIZE)
                end_time = time.time() * 1000
                diff = end_time - send_time
                if not data == message:
                    raise ValueError("BAD RESPONSE")
                print("{} bytes from {} tcp_seq={} time={} ms".format(PACKET_SIZE, cfg.HOST, pings + 1, round(diff, 3)))
                success += 1
                time.sleep(1)
            except socket.timeout:
                print("REQUEST TIMEOUT")
                failure += 1
        sock.close()
    except Exception as e:
        print("No TCP server in listen, {}".format(str(e)))

    return success, failure


"""main function"""


def main():
    success = 0
    failure = 0
    if PROTOCOL == "UDP":
        success, failure = udp_ping()
    elif PROTOCOL == "TCP":
        success, failure = tcp_ping()
    else:
        print("{} is not a valid option, please choose between TCP to UDP.".format(PROTOCOL))
        sys.exit(1)

    print("--- {} ping statistics ---".format(cfg.HOST))
    print("{} packets transmitted, {} received, {}% packet loss".format(success+failure, success, (100*failure/(success+failure))))


if __name__ == "__main__":
    main()
