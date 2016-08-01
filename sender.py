import socket
import sys
import array

def create_socket_message(bit_length):
  number_bytes = (int) (bit_length / 8)

  if number_bytes == 0:
    number_bytes = 1
  elif bit_length % 2 == 1:
    number_bytes = number_bytes + 1

  bytes_list = [0] * number_bytes
  #return "".join(map(chr, bytes_list))
  return bytes_list

def create_socket(ip, socket_string):
  sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
  server_address = (ip, 12345)

  try:
    print("Sending bytes")
    #sock.sendall(socket_string)
    sock.sendto(socket_string, server_address)
  finally:
    print("Closing socket")
    sock.close()


if __name__ == "__main__":
  cube_length = int(sys.argv[1])
  ip = sys.argv[2]

  socket_string = array.array('B', create_socket_message(2 ** cube_length))
  create_socket(ip, socket_string)
