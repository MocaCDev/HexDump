import os, sys

if not len(sys.argv) == 2:
  raise Exception('Expected file as argument')
if len(sys.argv) > 2:
  raise Exception("Too many arguments applied")

def validate_hex(file):

  hex_value = ''
  ascii_val = ''
  mem_addr = 0

  f = open(file, 'rb').read()
  
  for byte in f:
    # if str(b) > 'a' and str(b) < 'z' or str(b) > 'A' and b < 'Z':
    #   ascii_val += b
    # else:
    #   ascii_val += '.'
    if ord(chr(byte)) >= 0x41 and ord(chr(byte)) <= 0x5A or ord(chr(byte)) >= 0x61 and ord(chr(byte)) <= 0x7A:
      ascii_val += chr(byte)
    else:
      ascii_val += '.'

    if mem_addr % 16 == 0:
      print(format(mem_addr, '06X'), end = ' | ')
      if len(str(hex(byte).replace('0x', ''))) == 1:print('0'+hex(byte).replace('0x', ''), end = ' ')
      else: print(hex(byte).replace('0x', ''), end = ' ')
    elif mem_addr % 16 == 15:
      if len(str(hex(byte).replace('0x', ''))) == 1:print('0'+hex(byte).replace('0x', ''), end = ' ')
      else: print(hex(byte).replace('0x', ''), end = ' ')
      print('| '+ ascii_val)
      # print(ascii_val, end = '\n')
      ascii_val = ''
    else:
      if len(str(hex(byte).replace('0x', ''))) == 1:print('0'+hex(byte).replace('0x', ''), end = ' ')
      else: print(hex(byte).replace('0x', ''), end = ' ')
    mem_addr += 1

  return hex_value

def open_and_read():

  if os.path.isfile(sys.argv[1]):
    return validate_hex(sys.argv[1])
  
if __name__ == '__main__':
  open_and_read()