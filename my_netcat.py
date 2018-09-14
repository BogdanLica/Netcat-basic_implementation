import argparse
from ipaddress import ip_address

def setup_parser():

    parser = argparse.ArgumentParser(description="My own implementation of Netcat")


    parser.add_argument('port_number',metavar='-p',type=int, nargs='+',help='The port number to connect/listen to')
    parser.add_argument('-l', dest='listeningMod', action='store_true',help='Listen for incoming traffic')
    parser.add_argument('-t', dest='target',type=ip_address,help='The address to connect to')


    parser.parse_args()



setup_parser()