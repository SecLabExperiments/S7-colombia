#!/usr/bin/env python3

'''
Documentation, License etc.

@package S7_colombia
'''
import socket
import snap7
import threading
import netaddr
from time import sleep
socket.setdefaulttimeout(5)

def lookupPLC(ip, nada = None):
  '''
  Return True if in that ip maybe is hosted a S7 PLC
  List of: http://ipverse.net/ipblocks/data/countries/co.zone
  '''
  try:
    s = socket.socket()
    s.connect((ip, 102))
    print("[+] Possible PLC at: " + ip + "!")
  except:
    pass
  
def readIpBlocks(file_name):
  '''
  Read a file with ip's blocks
  '''
  ips = []
  f = open(file_name, 'rb')
  data = f.read().decode('utf-8')
  f.close()
  for line in data.splitlines():
    if '#' not in line:
      rangee = netaddr.glob_to_iprange(netaddr.cidr_to_glob(line))
      ips.append(rangee)
  return ips

def ipRange(start_ip, end_ip):
   start = list(map(int, start_ip.split(".")))
   end = list(map(int, end_ip.split(".")))
   temp = start
   ip_range = []
   
   ip_range.append(start_ip)
   while temp != end:
      start[3] += 1
      for i in (3, 2, 1):
         if temp[i] == 256:
            temp[i] = 0
            temp[i-1] += 1
      ip_range.append(".".join(map(str, temp)))    
      
   return ip_range


def main():
  lista = readIpBlocks('co.zone')
  # Starting with block 1:
  block_number = int(input("Input the block number to scan: "))
  block = lista[block_number - 1]
  ip_list = ipRange(str(block._start), str(block._end))
  print("[i] Will be scanned " + str(block.size) + " ip addresses.")
  threads_list = []
  for ip in ip_list:
    threads_list.append(threading.Thread(target=lookupPLC, args=(ip, None)))
  # Now the controlled threading start:
  max_threads = int(input(">>Enter the maximum number of threads: "))
  counter = 0
  while counter != block.size:
    if len(threading.enumerate()) <= max_threads:
      threads_list[counter].start()
      counter = counter + 1
      if counter % 100 == max_threads:
        print("[i] Already " + str(counter - max_threads) + " has been scanned")
      sleep(0.5)
  while len(threading.enumerate()) != 1:
    sleep(0.5)
  print("Finished!")
  print(counter)
  
if __name__ == "__main__":
  main()
