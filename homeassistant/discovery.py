import ujson
import usocket
from . import HomeAssistant  # Assuming HomeAssistant is in the same directory

MCAST_IP = "224.0.0.123"  # Multicast IP address for the search
MCAST_PORT = 38123  # Multicast port for the search
TIMEOUT = 5  # Timeout for receiving a response in seconds

QUERY = 'Home Assistants Assemble!'.encode('utf-8')  # Search message encoded in UTF-8

# This function attempts to find a Home Assistant instance on the network
def get_instance(api_password=None):
    info = scan()  # Scan the network for Home Assistant instances
    return HomeAssistant(info.get('host'), info.get('api_password', api_password))

# This function performs the network scan for Home Assistant instances
def scan():
    sock = usocket.socket(usocket.AF_INET, usocket.SOCK_DGRAM)  # Create a UDP socket
    try:
        if hasattr(sock, 'settimeout'):
            sock.settimeout(TIMEOUT)  # Set the socket timeout

        addrs = usocket.getaddrinfo(MCAST_IP, MCAST_PORT)  # Get address information
        sock.sendto(QUERY, addrs[0][4])  # Send the search message to the multicast group
        data, addr = sock.recvfrom(1024)  # Wait for and receive the response
        return ujson.loads(data.decode('utf-8'))  # Decode the response as JSON
    finally:
        sock.close()  # Close the socket after using it
