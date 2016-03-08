import socket
import sys


def create_socket_message(bit_length):
  number_bytes = (int) (bit_length / 8)

  if number_bytes == 0:
    number_bytes = 1
  elif bit_length % 2 == 1:
    number_bytes = number_bytes + 1

  bytes_list = [0] * number_bytes
  return "".join(map(chr, bytes_list))


def create_socket(ip, socket_string):
  sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  server_address = (ip, 12345)

  sock.connect(server_address)

  try:
    print("Sending bytes")
    sock.sendall(socket_string)
  finally:
    print("Closing socket")
    sock.close()


if __name__ == "__main__":
  cube_length = int(sys.argv[1])
  ip = sys.argv[2]

  socket_string = create_socket_message(2 ** cube_length)
  create_socket(ip, socket_string)