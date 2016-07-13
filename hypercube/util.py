

def number_bytes(bit_length):
    number_bytes = (int)(bit_length / 8)

    if number_bytes == 0:
        number_bytes = 1
    elif bit_length % 2 == 1:
        number_bytes = number_bytes + 1

    return number_bytes

def bytes_array(array):
    return array.array('B', array)