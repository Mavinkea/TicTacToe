# TicTacToe

## How To Run

### Server Side

To run Tic Tac Toe, upload all files to an allv machine or another Linux server. This can be done with PSFTP or a similar SSH client.
One this is done and you are in the directory of the downloaded files, enter in the command line interface
```
python server.py
```

The server will now be up and running, and it will print "Listening", as such:

![img2](https://github.com/Mavinkea/TicTacToe/blob/master/images/img2.JPG)

*NOTE- The following error may occur. It can be fixed by simply restarting the SSH client and running the above again.

![img1](https://github.com/Mavinkea/TicTacToe/blob/master/images/img1.JPG)

### Client Side

Once the server is up and running, open up another SSH client and navigate to the same directory or a directory where all the required
files are present. Upon doing so, enter in the command line interface
```
python client.py hostname
```
*NOTE- hostname is the name of the server in which server.py is running. Entering a host name that is not the same will return an
error.

## User Documentation

Once a client is running, the following commands are available to you.

#### 1. login (username)
  * login allows you to log into an existing account, or create a new one if you don't have one. It takes one argument,a username.

#### 2. exit 
  * exit takes no arguments, and allows you to exit the server.

#### 3. play
  * play searches for an opponent, and waits until an opponent is found. Upon finding an opponent, it initiates a game with them.
  Note that play can only be called once logged in.

#### 4. place (num)
  * once in a game and it is indicated that it is your turn, you can play your move by entering place followed by a number
  between 0 and 8 inclusive. 


