

def number_bytes(bit_length):
    number_bytes = (int)(bit_length / 8)

    if number_bytes == 0:
        number_bytes = 1
    elif bit_length % 2 == 1:
        number_bytes = number_bytes + 1
    return number_bytes

def bytes_array(array):
    return array.array('B', array)

def arr_from_bit_len(bit_length):
    bytess = number_bytes(bit_length)
    bytes_list = [0] * bytess
    #return "".join(map(chr, bytes_list))
    return bytearray(bytes_list) + bytearray([255, 255])
