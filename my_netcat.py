import argparse
import socket
import subprocess
import threading
import sys
from ipaddress import ip_address

'''
Parser for the initial program
'''
def setup_parser():

    parser = argparse.ArgumentParser(description="My own implementation of Netcat")


    parser.add_argument('-p','--port',dest='port',type=int, nargs='+',help='The port number to connect/listen to')
    parser.add_argument('-l','--listening', dest='listening', action='store_true',help='Listen for incoming traffic')
    parser.add_argument('-t','--target', dest='target',type=ip_address,help='The address to connect to')
    #parser.add_argument('--tcp',dest='tcp',type=bool, nargs='?',help='Set up a TCP connection')
    #parser.add_argument('--udp',dest='udp',type=bool, nargs='?',help='Set up a UDP connection')



    parser.add_argument('--upload',dest='upload',type=str,help='The destination of the file')
    parser.add_argument('--execute', dest='execute', type=int,help='Start a shell')
    parser.add_argument('--command', dest='command',type=str,help='Execute a command')


    settings = parser.parse_args()


    return settings
    

'''
Main Loop

Either listen to a port(be a client) or Connect to a client(be the C2 server)
'''
def me_terpreter(initial_settings):
    if initial_settings.listening == True:
        incomming_connection(initial_settings)
    elif initial_settings.target and initial_settings.port:
        buffer = sys.stdin.read()
        # CTRL-D
        outgoing_connection(buffer,str(initial_settings.target),initial_settings.port[0])



def os_commands_execute(command):
    ## Remove whitespaces
    command = command.rstrip()

    try:
        output = subprocess.check_output(command,stderr=subprocess.STDOUT,shell=True)
    except:
        output = "Failed to execute the command specified \r\n"

    return output


def incomming_connection(settings_user):
    target = "0.0.0.0"
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.bind((target,settings_user.port[0]))

    server.listen(5)

    print ("[*] Listening on %s:%d" % (target,settings_user.port[0]))
    while True:
        client_socket,addr = server.accept()

        print ("[*] Accepted connection from: %s:%d" %(addr[0],addr[1]))
        client_thread = threading.Thread(target=client_handler,args=(client_socket,))
        client_thread.start()

def shell(client_socket,settings_user):
    while True:
        client_socket.send("<Easy-terpreter:#> ")

        commandline_buffer = ""
        while "\n" not in commandline_buffer:
            commandline_buffer += client_socket.recv(1024)


        response = os_commands_execute(commandline_buffer)

        client_socket.send(response)
    


def upload_file(file):
    print ("Empty")


### call from second parser
def client_handler(client_socket,settings):
    if len(settings.upload):
        upload_file(settings.upload)
    elif len(settings.execute):
        shell(client_socket,settings)
    elif len(settings.command):
        output = os_commands_execute(settings.command)
        client_socket.send(output)
    


def outgoing_connection(buffer,target,port):
    client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    print("Target : %s and port %s" %(target,port))
    try:
        client.connect((target,port))
        if len(buffer):
            client.send(buffer)
        
        while True:
            recv_length = 1
            response = ""
            while recv_length:
                data = client.recv(4096)
                recv_length = len(data)
                response += data

                if recv_length < 4096:
                    break

            print (response)
            buffer = input("")
            buffer += "\n"


            client.send(buffer)

    except:
        print ("[*] Exception.Closing the program!")

        client.close()



mySettings = setup_parser()
me_terpreter(mySettings)

