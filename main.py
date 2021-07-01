import os, sys, json
from art import tprint
from colorama import Fore, Style, Back

# 
# ToAdd:
# Searching for specific binary value
# Chunking the binary output into sections
# 

if not len(sys.argv) >= 2:
  raise Exception('Expected file as argument')

def WelcomeScreen():
  tprint("HexDUMP")
  print(f'\tCreated by MocaCDeveloper\n\tVersion: 1.0.1')
  print('\n\t\tCommands:\n\t\t1) --FR:\n\t\t\t- Find and highlight all references of a value\n\t\t2) --has:\n\t\t\t- Check and see if a specific value exists in the binary\n\t\t3) --FA:\n\t\t\t- Find all references to a value, along with the offset\n\t\t4) --CS:\n\t\t\t- Change chunk sizes. Default is 16\n\t\t5) --colored:\n\t\t\t- Change colored output of offsets.\n\t\t6) --store:\n\t\t\t- Store dump into file\n\t\t7) --endat:\n\t\t\t- End at a specific point\n\t\t8) --startat:\n\t\t\t- Start at a secific point\n\t\t9) --JD:\n\t\t\t- Print just the data\n\t\t10) --HW:\n\t\t\t- Highlight words\n\t\t11) --HHW:\n\t\t\t- Highlight hex values of the words\n\n\tTo run, type ./dump file_to_dump --[argname] [arg_param]\n\tYou can have as many arguments as you want!')

def validate_hex(file):
  tprint("HexDUMP")
  print('\t\tBy MocaCDeveloper\n\n' + f'{"_"*67}')
  hex_value = ''
  ascii_val = ''
  mem_addr = 0
  find_reference = ''
  has_value = ''
  find_all = ''
  store_output = False
  CS = 16
  color = None
  end_at = 0
  start_at = 0
  just_data = False
  highlight_words = False
  highlight_hex_words = False
  print_under = False
  special_val = '.'
  spacing = 1
  mark_all_vals = []

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
        if sys.argv[i] == '--CS':
          CS = int(sys.argv[i + 1])
          i += 1
        if sys.argv[i] == '--endat':
          end_at = int(sys.argv[i + 1])
          i += 1
        if sys.argv[i] == '--startat':
          start_at = int(sys.argv[i + 1])
          i += 1
        if sys.argv[i] == '--JD':
          just_data = True
        if sys.argv[i] == '--HW':
          highlight_words = True
        if sys.argv[i] == '--HHW':
          highlight_hex_words = True
        if sys.argv[i] == '--PU':
          print_under = True
        if sys.argv[i] == '--special':
          if sys.argv[i + 1] == 'empty': special_val = ' '
          else: special_val = sys.argv[i + 1]
          i += 1
        if sys.argv[i] == '--spacing':
          spacing = int(sys.argv[i + 1])
          i += 1
        if sys.argv[i] == '--MA':
          i += 1
          while ',' in sys.argv[i] or ',' in sys.argv[i-1]:
            mark_all_vals.append(sys.argv[i].replace(',',''))
            if i == len(sys.argv) -1:break
            i += 1
        if sys.argv[i] == '--colored':
          if sys.argv[i + 1] == 'C': color = Fore.CYAN
          if sys.argv[i + 1] == 'B': color = Fore.BLUE
          if sys.argv[i + 1] == 'M': color = Fore.MAGENTA
          if sys.argv[i + 1] == 'Y': color = Fore.YELLOW
      except:
        raise Exception(f"Error occurred: Most likely missing a command for {sys.argv[i]}, or the command {sys.argv[i]} did not expect a command.")

  f = open(file, 'rb').read()
  size = len(f)
  if end_at == 0: end_at = size
  all_ = []

  if store_output:
    file = open('output.txt', 'w')
  
  last_val = ''
  count = 0
  for byte in f:

    if mem_addr == end_at:
      break
    if not mem_addr >= start_at:
      mem_addr += 1
      continue

    if ord(chr(byte)) >= 0x41 and ord(chr(byte)) <= 0x5A or ord(chr(byte)) >= 0x61 and ord(chr(byte)) <= 0x7A:
      if highlight_words:
        ascii_val += f'{Back.CYAN}{chr(byte)}{Style.RESET_ALL}'
      else: ascii_val += chr(byte)
    else:
      ascii_val += special_val

    count += 1
    if mem_addr % CS == 0 or mem_addr == start_at:
      if not just_data:
        print(f'{Style.BRIGHT + Back.WHITE + color if not color == None else Style.BRIGHT + Fore.WHITE}' + '\x1B[3m' + format(mem_addr, '06X') + f'{Style.RESET_ALL}', end = '|')
      if store_output:
        file.write(format(mem_addr, '06X') + '|')
      if len(str(hex(byte).replace('0x', ''))) == 1:
        if not find_reference == '' and '0'+hex(byte).replace('0x', '') == find_reference or '0'+hex(byte).replace('0x', '') in mark_all_vals:
          print(Fore.GREEN+'0'+hex(byte).replace('0x', '')+Style.RESET_ALL, end = f'{" " if count == spacing else ""}')
        else: 
          if not ascii_val[len(ascii_val)-1] == '.':
            if highlight_hex_words:
              print(Back.YELLOW + '0'+hex(byte).replace('0x', '') + Style.RESET_ALL, end = f'{" " if count == spacing else ""}')
            else: print('0'+hex(byte).replace('0x', ''), end = f'{" " if count == spacing else ""}')
          else: print('0'+hex(byte).replace('0x', ''), end = f'{" " if count == spacing else ""}')

        if store_output:
          file.write('0'+hex(byte).replace('0x', '') + f'{" " if count == spacing else ""}')
        all_.append('0'+hex(byte).replace('0x', ''))
      else:
        if not find_reference == '' and hex(byte).replace('0x', '') == find_reference or hex(byte).replace('0x', '') in mark_all_vals:
          print(Fore.GREEN+hex(byte).replace('0x', '')+Style.RESET_ALL, end = f'{" " if count == spacing else ""}')
        else: 
          if not ascii_val[len(ascii_val)-1] == '.':
            if highlight_hex_words:
              print(Back.YELLOW + hex(byte).replace('0x', '') + Style.RESET_ALL, end = ' ')
            else: print(hex(byte).replace('0x', ''), end = f'{"" if count < spacing else " "}')
          else: print(hex(byte).replace('0x', ''), end = f'{"" if count < spacing else " "}')
        if store_output:
          file.write(hex(byte).replace('0x', '') + f'{"" if count < spacing else " "}')
        all_.append(hex(byte).replace('0x', ''))
    elif mem_addr % CS == CS - 1:
      if len(str(hex(byte).replace('0x', ''))) == 1:
        if not find_reference == '' and '0'+hex(byte).replace('0x', '') == find_reference or '0'+hex(byte).replace('0x', '') in mark_all_vals:
          print(Fore.GREEN+'0'+hex(byte).replace('0x', '')+Style.RESET_ALL, end = '')
        else:
          if not ascii_val[len(ascii_val)-1] == '.':
            if highlight_hex_words:
              print(Back.YELLOW + '0'+hex(byte).replace('0x', '') + Style.RESET_ALL, end = '')
            else: print('0'+hex(byte).replace('0x', ''), end = '')
          else: print('0'+hex(byte).replace('0x', ''), end = '')

        if store_output:
          file.write('0'+hex(byte).replace('0x', '') + '')
        all_.append('0'+hex(byte).replace('0x', ''))
      else:
        if not find_reference == '' and hex(byte).replace('0x', '') == find_reference or hex(byte).replace('0x', '') in mark_all_vals:
          print(Fore.GREEN+hex(byte).replace('0x', '')+Style.RESET_ALL, end = '')
        else: 
          if not ascii_val[len(ascii_val)-1] == '.':
            if highlight_hex_words:
              print(Back.YELLOW + hex(byte).replace('0x', '') + Style.RESET_ALL, end = '')
            else: print(hex(byte).replace('0x', ''), end = '')
          else: print(hex(byte).replace('0x', ''), end = '')

        all_.append(hex(byte).replace('0x', ''))

      if store_output:
        file.write(hex(byte).replace('0x', '') + '')
      if print_under:
        print('\n\t   |', end = '')
        c = 0
        for i in range(len(ascii_val)):
          if i == len(ascii_val) - 1: last_val = ascii_val[i]

          if c >= 1: 
            if not ascii_val[i] == '.':
              if not ascii_val[i-1] == '.':print('  ' + ascii_val[i], end = '')
              else: print(' [' + ascii_val[i], end = '')
            else:
              if not ascii_val[i-1] == '.':print('] ' + ascii_val[i], end = '')
              else:print('  ' + ascii_val[i], end = '')
          else: 
            if ascii_val[i] == '.' and not last_val == '.':print(' ]' + ascii_val[i], end = '')
            else: print('  ' + ascii_val[i], end = '')
          c += 1
        print()
        # print('\n\t   | '+ Style.BRIGHT + Fore.WHITE + ascii_val + Style.RESET_ALL, end = '\n')
      else:
        print('|'+ Style.BRIGHT + Fore.WHITE + ascii_val + Style.RESET_ALL, end = '\n')
      if store_output:
        file.write('|' + ascii_val + '\n')
      # print(ascii_val, end = '\n')
      ascii_val = ''
    else:
      if len(str(hex(byte).replace('0x', ''))) == 1:
        if not find_reference == '' and '0'+hex(byte).replace('0x', '') == find_reference or '0'+hex(byte).replace('0x', '') in mark_all_vals:
          print(Fore.GREEN+'0'+hex(byte).replace('0x', '')+Style.RESET_ALL, end = f'{"" if count < spacing else " "}')
        else:
          if not ascii_val[len(ascii_val)-1] == '.':
            if highlight_hex_words:
              print(Back.YELLOW + '0'+hex(byte).replace('0x', '') + Style.RESET_ALL, end = ' ')
            else: print('0'+hex(byte).replace('0x', ''), end = f'{"" if count < spacing else " "}')
          else: print('0'+hex(byte).replace('0x', ''), end = f'{"" if count < spacing else " "}')

        if store_output:
          file.write('0'+hex(byte).replace('0x', '') + f'{"" if count < spacing else " "}')
        all_.append('0'+hex(byte).replace('0x', ''))
      else:
        if not find_reference == '' and hex(byte).replace('0x', '') == find_reference or hex(byte).replace('0x', '') in mark_all_vals:
          print(Fore.GREEN+hex(byte).replace('0x', '')+Style.RESET_ALL, end = f'{"" if count < spacing else " "}')
        else: 
          if not ascii_val[len(ascii_val)-1] == '.':
            if highlight_hex_words: 
              print(Back.YELLOW + hex(byte).replace('0x', '') + Style.RESET_ALL, end = ' ')
            else: print(hex(byte).replace('0x', ''), end = f'{"" if count < spacing else " "}')
          else: print(hex(byte).replace('0x', ''), end = f'{"" if count < spacing else " "}')

        if store_output:
          file.write(hex(byte).replace('0x', '') + f'{"" if count < spacing else " "}')
        all_.append(hex(byte).replace('0x', ''))
    mem_addr += 1
    if count == spacing: count = 0
    if mem_addr == size:
      mem_addr = 0
      if not has_value == '' or not find_all == '':
        if len(all_) == size:
          if not find_all == '':
            info = {find_all: []}
            for x in range(len(all_)):
              mem_addr += 1
              if all_[x] == find_all: info[find_all].append('0x'+format(mem_addr, '06X'))
            
            with open('find.json', 'w') as f:
              f.write(json.dumps(info, indent = 2))
              f.close()
            
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

  print('' + f'{"_"*67}')

def open_and_read():

  if os.path.isfile(sys.argv[1]):
    return validate_hex(sys.argv[1])
  
if __name__ == '__main__':
  if sys.argv[1] == '--h': WelcomeScreen()
  else: open_and_read()