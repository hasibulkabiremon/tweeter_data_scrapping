import socket

def get_device_ip():
    try:
        # Create a socket object and connect to an external server (e.g., Google's DNS server)
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(0)
        # Connect to an external server (Google's DNS: 8.8.8.8)
        s.connect(('8.8.8.8', 80))
        # Get the local address used to connect (this is the external IP)
        ip = s.getsockname()[0]
        print(f"Real Public IP: {ip}")
        return ip
    except Exception as e:
        return f"Error: {e}"
    finally:
        s.close()


    # try:
    #     # Get the hostname of the device
    #     hostname = socket.gethostname()
    #     # Get the IP address associated with the hostname
    #     ip_address = socket.gethostbyname(hostname)
    #     print(ip_address)
    #     return ip_address
    # except Exception as e:
    #     return f"Error: {e}"

def get_device_hostname():
    try:
        # Get the hostname of the device
        hostname = socket.gethostname()
        print(hostname)
        
        return hostname
    except Exception as e:
        return f"Error: {e}"

# Get and print the device's IP address
# device_ip = get_device_ip()
# print(f"Device IP Address: {device_ip}")
