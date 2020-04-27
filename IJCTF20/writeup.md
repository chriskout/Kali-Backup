# CTF: IJCTF
### Problem: PWN/Input
**This writeup assumes you have knowledge/skills in: Radare2 (or some equivalent reverse enginnering tool), PWNTools, Stack Smashing
Author: chriskout**

The problem gives us one file named input. Running our basic ```File``` and ```Checksec``` on it tells us it is a 64bit ELF binary, with Partial Relro, NX, but no stack canary.

Next I ran the file with ltrace

```$ ltrace ./input```

This showed us that the file was recieving input with getchar(). Meaning it only recieves one character at a time from our input.

Next we view the binary in radare2.

```$ r2 input```

Upon analyzing the file (running aaa) and running afl (anylizing the function list), we see that there is no main. OH NO, WHERE DO WE START!?

There are two functions of interest to us. First is getchar() which is used to get our input, and second is execve(), which will act as a win function.

This seems like a stack smash problem, with the location of execve() being a substitute for the win function, and get_char() demanding we write our payload on character at a time. Both of these functions are located rather close together, so I took a look at this area.

Upon scanning the binary, this is cofirmed. Our input is initially stored at a address of ebp - 0x430, inside a for loop that only ends when the value at address ebp-0x18 is greater then 0x441. This value increases by 1 each time the loop is ran.

From here it seems like writing a simple stack smash, with one catch, when we overwrite ebp-0x18, we must make sure to to not overwrite it with a value that breaks the for loop. For simplicity I chose to overwrite it with its
current value, effectively not changing how the for loop was working. It is already long enough for us to overwrite the return function. A cool extension to this problem would have been for the user to overwrite this value to give
themeslevs enough room to overwrite the return function.

From here it is just knowing some pwn tool tricks, here are the big ones:
* Use ```send()``` not ```sendline()```. The latter does not work because of funcky stdin buffering cause by getchar().
* Send win function and ebp-0x18 value with the following: 
	```python
	win = p64(0xdeadbeef)
	for c in win:
	    r.send(chr(c).encode())
	```
* If you do not get shell, you might just be one character off. Try typing ```ls``` a couple times.

Happy PWNing nerd.

