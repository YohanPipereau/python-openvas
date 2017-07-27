import os, socket, time, sys, select

def SocketConnect(message,timer,verbose=False,unixsocket_path = '/var/run/openvassd.sock'):
    #unixsocket_path is the socket of openvassd which it uses to communicate with redis and any manager
    outputVar=""
    try:
        #Check the existence of the socket
        os.path.isfile(unixsocket_path)
    except OSError:
        print(" This unixsocket does not exist ... default is /var/run/openvassd.sock ")

    ##Instantiate the socket and connect the client to it (the server is openvas-scanner)
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    sock.connect(unixsocket_path)
    #sock.setblocking(False)
    for line in message.splitlines(True):
        if line == "< OTP/2.0 >\n":
            sock.send(line)
            time.sleep(1)
        else:
            sock.send(line)
            time.sleep(0.01)
    if verbose == False:
        while True:
            try:
                sock.settimeout(timer)
                data = sock.recv(1024)
                sock.settimeout(None)
                outputVar += data
                if "<|> BYE" in data:
                    return(outputVar)
            except socket.timeout:
                return(outputVar)
    else:
        while True:
            try:
                sock.settimeout(timer)
                data = sock.recv(1024)
                sock.settimeout(None)
                outputVar += data
                if "<|> BYE" in data:
                    return(outputVar)
                print(data)
            except socket.timeout:
                print("timeout")
                return(outputVar)
