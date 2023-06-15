import socket
import ssl
import json
import argparse


HOST_ADDRESS = 'api.vk.com'
HTTPS_PORT = 443


def processing_data(id, data, token):
    with socket.create_connection((HOST_ADDRESS, HTTPS_PORT)) as client_socket:
        ssl_context = ssl.create_default_context()
        ssl_client_socket = ssl_context.wrap_socket(client_socket, server_hostname=HOST_ADDRESS)

    if data == 'friends':
        get_friends(id, ssl_client_socket, token)
    elif data == 'albums':
        get_albums(id, ssl_client_socket, token)


def get_friends(id, ssl_client_socket, token):
    friends_data = get_vk_data('friends.get', {'user_id': id, 'count': 5000}, ssl_client_socket, token)
    friend_ids = friends_data['response']['items']

    users = get_vk_data('users.get', {'user_ids': ','.join(map(str, friend_ids))}, ssl_client_socket, token)
    print_friends(users)


def get_albums(id, ssl_client_socket, token):
    albums_data = get_vk_data('photos.getAlbums', {'user_id': id}, ssl_client_socket, token)
    albums = albums_data['response']['items']

    print_albums(albums)


def get_vk_data(method, params, socket, token):
    request_data = {
        'method': 'GET',
        'url': f'/method/{method}',
        'version': '1.1',
        'headers': {'host': HOST_ADDRESS},
        'body': None
    }

    params['access_token'] = token
    params['v'] = '5.131'
    request_data['url'] += '?' + '&'.join([f'{key}={value}' for key, value in params.items()])

    request_message = get_prepared_message(request_data)
    response_data = send_request(socket, request_message)

    if 'response' in response_data:
        return response_data
    elif 'error' in response_data:
        error_code = response_data['error']['error_code']
        error_message = response_data['error']['error_msg']
        raise Exception(f'API Error: {error_code} - {error_message}')
    else:
        raise Exception('Invalid response from API')


def send_request(socket, request_message):
    socket.send(request_message.encode())

    response = b''
    while True:
        recv_data = socket.recv(4096)
        response += recv_data

        if b'\r\n\r\n' in response:
            json_start = response.index(b'\r\n\r\n') + 4
            json_response = response[json_start:].decode('utf-8')

            try:
                parsed_response = json.loads(json_response)
            except json.JSONDecodeError:
                continue

            return parsed_response

        if not recv_data:
            break

    raise Exception('Invalid response from API')


def get_prepared_message(data):
    message = data['method'] + ' ' + data['url'] + ' ' \
              + 'HTTP/' + data['version'] + '\n'
    for header, value in data['headers'].items():
        message += f'{header}: {value}\n'
    if data['body']:
        pass
    message += '\n'
    return message


def print_friends(users):
    if 'response' in users:
        print('Список друзей:')
        for user in users['response']:
            first_name = user.get('first_name', 'Unknown')
            last_name = user.get('last_name', 'Unknown')
            print(f'{first_name} {last_name}')
    else:
        print('У пользователя нет друзей.')


def print_albums(albums):
    if 'response' in albums:
        print('Список фотоальбомов:')
        for album in albums:
            title = album.get('title', 'Unknown')
            print(title)
    else:
        print('У пользователя нет фотоальбомов.')


def read_input():
    parser = argparse.ArgumentParser(description='VK API Data')
    parser.add_argument('user_id', type=int, help='User ID')
    parser.add_argument('data', choices=['friends', 'albums'], help='Type of data to retrieve')
    return parser.parse_args()


def main():
    with open('token.txt', 'r') as file:
        token = file.readline().strip()
    input_data = read_input()
    processing_data(input_data.user_id, input_data.data, token)


if __name__ == '__main__':
    main()
