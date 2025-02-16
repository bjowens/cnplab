import socket
import os
import hashlib  # needed to verify file hash

IP = '127.0.0.1'  # change to the IP address of the server
PORT = 12000  # change to a desired port number
BUFFER_SIZE = 1024  # change to a desired buffer size


def get_file_info(data: bytes) -> (str, int):
    return data[8:].decode(), int.from_bytes(data[:8], byteorder= 'big')


def upload_file(server_socket: socket, file_name: str, file_size: int):
    # create a SHA256 object to verify file hash
    # TODO: section 1 step 5 in README.md file
    sha256_object = hashlib.sha256()

    # create a new file to store the received data
    with open(file_name + '.temp', 'wb') as file:
        # TODO: section 1 step 7a - 7e in README.md file
        file_received = 0
        while file_received < file_size:
            message, clientAddress = server_socket.recvfrom(BUFFER_SIZE)
            file.write(message)
            sha256_object.update(message)
            server_socket.sendto("received".encode('utf-8'), clientAddress)
            file_received += len(message)

    # get hash from client to verify
    # TODO: section 1 step 8 in README.md file
    hash_result, clientAddress = server_socket.recvfrom(BUFFER_SIZE)
    # TODO: section 1 step 9 in README.md file
    if hash_result == sha256_object.digest():
        server_socket.sendto("success".encode('utf-8'), clientAddress)
    else:
        server_socket.sendto("failed".encode('utf-8'), clientAddress)


def start_server():
    # create a UDP socket and bind it to the specified IP and port
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((IP, PORT))
    print(f'Server ready and listening on {IP}:{PORT}')

    try:
        while True:
            # TODO: section 1 step 2 in README.md file
            message, clientAddress = server_socket.recvfrom(BUFFER_SIZE)
            # expecting an 8-byte byte string for file size followed by file name
            # TODO: section 1 step 3 in README.md file
            message_8_byte_int = get_file_info(message)
            file_name = message_8_byte_int[0]
            file_size = message_8_byte_int[1]
            # TODO: section 1 step 4 in README.md file
            server_socket.sendto("go ahead".encode('utf-8'), clientAddress)
            upload_file(server_socket, file_name, file_size)
    except KeyboardInterrupt as ki:
        pass
    except Exception as e:
        print(f'An error occurred while receiving the file:str {e}')
    finally:
        server_socket.close()


if __name__ == '__main__':
    start_server()