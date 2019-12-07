# cs3331_project
this project is coming from 19T3, it wll be great if you found it helpful! :-)

It is a chat software, contain both server and client.



User Guide

In a terminal, type following commands:
python3 server.py 5000 5000 5000

This is how you open a server, these numbers are used for: server_port, block_duration, timeout
You can set block_duration and timeout as long as possible if you just want to play around, but pick a free port for server.

And open another terminal, type following commands:
python3 client.py 127.0.0.1 5000
It will connect you to server. And you can log in and start talk!(You can only talk to yourself because they all run on the same machine :)

I include assignment specification. You may find some helpful guides inside. 

Tips
It is not a solid program so bug happen sometimes. And application protocol is a String. I may tranfer it into JSON but i dont have time right now.
And i used too much thread in code. Beware of your gear!
