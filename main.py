import os, sys
from colorama import Fore, Style

# 
# ToAdd:
# Searching for specific binary value
# Chunking the binary output into sections
# 

if not len(sys.argv) >= 2:
  raise Exception('Expected file as argument')
if len(sys.argv) > 8:
  raise Exception("Too many arguments applied")

def validate_hex(file):

  hex_value = ''
  ascii_val = ''
  mem_addr = 0
  find_reference = ''
  has_value = ''
  find_all = ''
  store_output = False

  if len(sys.argv) >= 2:
    for i in range(len(sys.argv)):
      try:
        if sys.argv[i] == '--FR':
          find_reference = sys.argv[i+1]
          i += 1
        if sys.argv[i] == '--has':
          has_value = sys.argv[i + 1]
          i += 1
        if sys.argv[i] == '--FA':
          find_all = sys.argv[i + 1]
          i += 1
        if sys.argv[i] == '--store':
          store_output = True
      except:
        raise Exception("Error happened")

  f = open(file, 'rb').read()
  size = len(f)
  all_ = []

  if store_output:
    file = open('output.txt', 'w')
  
  for byte in f:
    # if str(b) > 'a' and str(b) < 'z' or str(b) > 'A' and b < 'Z':
    #   ascii_val += b
    # else:
    #   ascii_val += '.'
    if ord(chr(byte)) >= 0x41 and ord(chr(byte)) <= 0x5A or ord(chr(byte)) >= 0x61 and ord(chr(byte)) <= 0x7A:
      ascii_val += chr(byte)
    else:
      ascii_val += '.'

    if has_value == '' and find_all == '':
      if mem_addr % 16 == 0:
        print(format(mem_addr, '06X'), end = ' | ')
        if store_output:
          file.write(format(mem_addr, '06X') + ' | ')
        if len(str(hex(byte).replace('0x', ''))) == 1:
          if not find_reference == '' and '0'+hex(byte).replace('0x', '') == find_reference:
            print(Fore.GREEN+'0'+hex(byte).replace('0x', '')+Style.RESET_ALL, end = ' ')
          else: print('0'+hex(byte).replace('0x', ''), end = ' ')

          if store_output:
            file.write('0'+hex(byte).replace('0x', '') + ' ')
        else:
          if not find_reference == '' and hex(byte).replace('0x', '') == find_reference:
            print(Fore.GREEN+hex(byte).replace('0x', '')+Style.RESET_ALL, end = ' ')
          else: print(hex(byte).replace('0x', ''), end = ' ')

          if store_output:
            file.write(hex(byte).replace('0x', '') + ' ')
      elif mem_addr % 16 == 15:
        if len(str(hex(byte).replace('0x', ''))) == 1:
          if not find_reference == '' and '0'+hex(byte).replace('0x', '') == find_reference:
            print(Fore.GREEN+'0'+hex(byte).replace('0x', '')+Style.RESET_ALL, end = ' ')
          else:print('0'+hex(byte).replace('0x', ''), end = ' ')

          if store_output:
            file.write('0'+hex(byte).replace('0x', '') + ' ')
        else:
          if not find_reference == '' and hex(byte).replace('0x', '') == find_reference:
            print(Fore.GREEN+hex(byte).replace('0x', '')+Style.RESET_ALL, end = ' ')
          else: print(hex(byte).replace('0x', ''), end = ' ')

          if store_output:
            file.write(hex(byte).replace('0x', '') + ' ')
        print('| '+ ascii_val)
        if store_output:
          file.write('| ' + ascii_val + '\n')
        # print(ascii_val, end = '\n')
        ascii_val = ''
      else:
        if len(str(hex(byte).replace('0x', ''))) == 1:
          if not find_reference == '' and '0'+hex(byte).replace('0x', '') == find_reference:
            print(Fore.GREEN+'0'+hex(byte).replace('0x', '')+Style.RESET_ALL, end = ' ')
          else:print('0'+hex(byte).replace('0x', ''), end = ' ')

          if store_output:
            file.write('0'+hex(byte).replace('0x', '') + ' ')
        else:
          if not find_reference == '' and hex(byte).replace('0x', '') == find_reference:
            print(Fore.GREEN+hex(byte).replace('0x', '')+Style.RESET_ALL, end = ' ')
          else: print(hex(byte).replace('0x', ''), end = ' ')

          if store_output:
            file.write(hex(byte).replace('0x', '') + ' ')
      mem_addr += 1
    else:
      if len(str(hex(byte).replace('0x', ''))) == 1:
        all_.append('0'+hex(byte).replace('0x', ''))
      else:
        all_.append(hex(byte).replace('0x', ''))
      
      if len(all_) == size:
        if not find_all == '':
          info = {find_all: []}
          for x in range(len(all_)):
            mem_addr += 1
            if all_[x] == find_all: info[find_all].append('0x'+format(mem_addr, '06X'))
          print(info)
        if not has_value == '':
          mem_addr = 0
          found = ''
          for x in range(len(all_)):
            if x == len(all_) - 1:
              print(False)
              break
            found = all_[x] + all_[x+1]

            if found == has_value or has_value in found:
              mem_addr += 1
              print(str(True) + ', found at offset 0x' + format(mem_addr, '06X') + f'({int(mem_addr)})')
              break 
            mem_addr += 1


  return hex_value

def open_and_read():

  if os.path.isfile(sys.argv[1]):
    return validate_hex(sys.argv[1])
  
if __name__ == '__main__':
  open_and_read()