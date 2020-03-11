READ ME

Directory Tree:

Linux ---
|	|---Application -
|       		|--- Server ---
|			|      	       |- server.py
|       		|	       |- user_credentials.json
|			|
|			|--- Client1---
|			|	       |- client.py
|			|	       |- client_as_server.py
|			|	       |- gui.py
|	         	|	       |- file.py
|			|
|			|--- Client2 ---
|					|- client.py
|					|- client_as_server.py
|					|- gui.py
|					|- file.py
|
Windows ----
|---Application ---
		   |--- Server ---
			|      	       |- server.py
	       		|	       |- user_credentials.json
			|
			|--- Client1---
			|	       |- client.py
			|	       |- client_as_server.py
			|	       |- gui.py
	         	|	       |- file.py
			|
			|--- Client2 ---
					|- client.py
					|- client_as_server.py
					|- gui.py
					|- file.py


This program can run in most of the linux distros as well as windows.


FOR WINDOWS USERS:

Guide:
It is highly advised to use Anaconda on windows.
1.Download and install the appropriate version of Anaconda Manager from https://www.anaconda.com/.
2.Press windows key + s, search “anaconda prompt” and open it.
3.Create and activate environment using following commands:
	a)conda create --name cn python=3.6 tk (enter “y” when prompted)
	b)conda activate cn (activates the cn environment)
4.Now navigate to the application folder of the project, using cd command.
5.Now open 2 more anaconda prompts and navigate to Application folder. Make sure to activate cn environment using “conda activate cn” command.
6.Navigate from one terminal to client1 directory, one terminal to client2 directory and one to server directory.
7.Run the following Commands in order:
	a)Terminal in server directory, start the server with “python server.py” command.
	b)Terminals in client1 and client2 directory, start the client with “python gui.py” command.
8.You can use the application now.

This application is in very early stage so sometimes it can hang. To forcefully terminate the programs you can use the following key combinations:
1.ctrl+c
2.ctrl+break/pause
3.Go to Task Manager and find your program either in Processes or Details and click on end task.

For Linux Users:
Follow this for Ubuntu, (For other distros it doesn’t differs much).
1.Ubuntu comes with python 3.5 so all you have to do is make sure you have the pip3 installed if not then open terminal and enter  “sudo apt-get -y install python3-pip”.

2.Now installing the tkinter package by entering “sudo apt-get install python-tk”3 in a terminal.
3.Now navigate to the application folder of the project, using cd command.
4.Now open 2 more terminals and navigate to Application folder. 
5.Navigate from one terminal to client1 directory, one terminal to client2 directory and one to server directory.
6.Run the following Commands in order:
	a)Terminal in server directory, start the server with “python server.py” command.
	b)Terminals in client1 and client2 directory, start the client with “python gui.py” command.
7.You can use the application now.

To exit, if the program hangs, the command is “ctrl+c”.


Avilable IDs you can use:
ID: Ashok
Password: 1111

ID: Anil Kumar Swain
Password: kiit

ID: Gurdeep
Password: haribol
