import argparse
import socket
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

    settings = parser.parse_args()


    return settings
    

'''
Main Loop

Either listen to a port(be a client) or Connect to a client(be the C2 server)
'''
def server_loop(initial_settings):
    
    while True:
        if initial_settings.listening == True:
            incomming_connection(initial_settings)
        elif initial_settings.target and initial_settings.port:
            outgoing_connection(initial_settings)
        else:
            break
    
    

'''
The parser for the 2nd prompt
'''
def parser_server():
    print ("Empty")


def os_commands_execute(command):
    return ""


def incomming_connection(settings_user):
    print ("Empty In")

def outgoing_connection(settings_user):
    print ("Empty Out")

def command_shell(typeOfShell):
    if typeOfShell == 1:
        reverse_shell()
    else:
        bind_shell()


def reverse_shell():
    print ("Empty")


def bind_shell():
    print ("Empty")


def upload_file(file):
    print ("Empty")



def client_handler(client_socket,settings):
    if len(settings.upload):
        upload_file(settings.upload)
    elif len(settings.execute):
        command_shell(settings.shell)
    elif len(settings.command):
        output = os_commands_execute(settings.command)
        client_socket.send(output)
    


def client_send_data(buffer,target,port):
    client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

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
server_loop(mySettings)

