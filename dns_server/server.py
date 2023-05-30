import socket
import json
import datetime
import dns.resolver


AUTHORITY_SERVER = '213.180.193.1'  # ns1.yandex.ru
CACHE_FILE = 'dns_cache.json'
HOST = 'localhost'
PORT = 1234


def check_internet_connection():
    try:
        socket.create_connection((AUTHORITY_SERVER, 80))
        return True
    except OSError:
        return False


def load_cache():
    try:
        with open(CACHE_FILE, 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def save_cache(cache):
    with open(CACHE_FILE, 'w') as file:
        json.dump(cache, file)


def get_dns_record(domain, record_type):
    cache = load_cache()

    if f'({domain}, {record_type})' in cache:

        if not check_internet_connection():
            print('Loaded from cache')
            return cache[f'({domain}, {record_type})']

        timestamp_str = cache[f'({domain}, {record_type})']['time']
        timestamp = datetime.datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S.%f')
        time_diff = datetime.datetime.now() - timestamp
        if time_diff.total_seconds() < cache[f'({domain}, {record_type})']['ttl']:
            print('Loaded from cache')
            return cache[f'({domain}, {record_type})']

    return None


def update_dns_record(domain, record_type, data):
    cache = load_cache()
    if data['info'] != 'Unknown domain name':
        print('Updated cache')
        cache[f'({domain}, {record_type})'] = data
        save_cache(cache)


def process_data(data):
    query = data.decode('utf-8').strip().split()
    if len(query) == 2:
        domain = query[0]
        record_type = query[1].lower()
        if record_type not in ['ns', 'a', 'aaaa', 'soa']:
            return b'Unknown record type'
        print(domain, record_type)

        response = resolve_dns_query(domain, record_type)

        if response:
            return response['info'].encode('utf-8')

    return b'Invalid query'


def resolve_dns_query(domain, record_type):
    data = get_dns_record(domain, record_type)

    if data is not None:
        return data

    if not check_internet_connection():
        return {'info': 'No internet connection'}

    response = request_data(domain, record_type)

    if response:
        update_dns_record(domain, record_type, response)

    return response


def request_data(host, request_type):
    resolver = dns.resolver.Resolver()
    resolver.nameservers = [AUTHORITY_SERVER]

    data = {}

    try:
        response = resolver.resolve(host, request_type)
    except dns.resolver.NoNameservers:
        data['info'] = 'Unknown domain name'
        return data
    except dns.resolver.NoAnswer:
        return {}
    except dns.resolver.NXDOMAIN:
        return 'no servers'
    except dns.resolver.Timeout:
        return 'timeout'

    if request_type == 'ns':
        data = handle_ns(response)
    elif request_type == 'a':
        data = handle_a_aaaa(response)
    elif request_type == 'aaaa':
        data = handle_a_aaaa(response)
    elif request_type == 'soa':
        data = handle_soa(response)

    data['time'] = str(datetime.datetime.now())
    data['ttl'] = response.rrset.ttl

    return data


def handle_ns(response):
    data = {'info': 'Server:  ns1.yandex.ru\nAddress:  213.180.193.1\n\nNon-authoritative answer:\n',
            'time': '',
            'ttl': 0}
    for ns in response:
        ns_name = str(ns.target)
        data['info'] += f'nameserver = {ns_name[:-1]}\n'

    return data


def handle_a_aaaa(response):
    data = {'info': 'Server:  ns1.yandex.ru\nAddress:  213.180.193.1\n\nNon-authoritative answer:\nAddresses:\n',
            'time': '', 'ttl': 0}
    for rr in response:
        data['info'] += f'\t{rr.to_text()}\n'
    return data


def handle_soa(response):
    data = {'info': 'Server:  ns1.yandex.ru\nAddress:  213.180.193.1\n\nNon-authoritative answer:\n', 'time': '',
            'ttl': 0}

    for rr in response:
        info = rr.to_text().split()
    data['info'] += f'primary name server = {info[0][:-1]}\n' \
                    f'responsible mail addr = {info[1][:-1]}\n' \
                    f'serial = {info[2]}\n' \
                    f'refresh = {info[3]}\n' \
                    f'retry = {info[4]}\n' \
                    f'expire = {info[5]}\n' \
                    f'default TTL = {info[6]}\n'
    return data


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((HOST, PORT))
    sock.listen(1)

    while True:
        conn, addr = sock.accept()
        try:
            data = conn.recv(1024)
            if data == b'exit':
                break
            response = process_data(data)
            conn.sendall(response)
        finally:
            conn.shutdown(socket.SHUT_RDWR)
            conn.close()


if __name__ == '__main__':
    main()
