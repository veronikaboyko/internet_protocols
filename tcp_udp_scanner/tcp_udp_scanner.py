import socket
import argparse


def scan_ports(host, start_port, end_port):
    open_tcp_ports = []
    open_udp_ports = []

    for port in range(start_port, end_port + 1):
        try:
            tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            tcp_sock.settimeout(1)

            tcp_result = tcp_sock.connect_ex((host, port))
            if tcp_result == 0:
                open_tcp_ports.append(port)

            tcp_sock.close()

            udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            udp_sock.settimeout(1)

            udp_sock.sendto(bytes("", "utf-8"), (host, port))
            udp_data, udp_addr = udp_sock.recvfrom(1024)
            if udp_addr:
                open_udp_ports.append(port)

            udp_sock.close()
        except socket.error:
            pass

    return open_tcp_ports, open_udp_ports


def read_inputs():
    parser = argparse.ArgumentParser(description='TCP and UDP port scanner')
    parser.add_argument('host', type=str, help='Target host')
    parser.add_argument('start_port', type=int, help='Start port number')
    parser.add_argument('end_port', type=int, help='End port number')

    return parser.parse_args()


def main():
    args = read_inputs()

    target_host = args.host
    start_port = args.start_port
    end_port = args.end_port

    if start_port > end_port:
        print('Error: Start port must be less than or equal to end port.')
        return

    if start_port < 1 or start_port > 65535 or end_port < 1 or end_port > 65535:
        print('Error: Ports must be between 1 and 65535.')
        return

    open_tcp_ports, open_udp_ports = scan_ports(target_host, start_port, end_port)

    if len(open_tcp_ports) == 0 and len(open_udp_ports) == 0:
        print(f'\nAll ports in range {start_port} to {end_port} are closed.\n')
    else:
        print('Open TCP ports:')
        if len(open_tcp_ports) != 0:
            for port in open_tcp_ports:
                print(port)
        else:
            print('-\n')

        print('Open UDP ports:')
        if len(open_udp_ports) != 0:
            for port in open_udp_ports:
                print(port)
        else:
            print('-\n')


if __name__ == '__main__':
    main()
