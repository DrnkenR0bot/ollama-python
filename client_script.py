#!/home/dok/env/bin/python3

import http.client

# Replace this with the ACTUAL IP address of your server computer
# Example: '192.168.1.15'
SERVER_IP = 'vision.lan' 
PORT = 8000

def send_message():
    while True:
        msg = input("Enter message to send (or 'q' to quit): ")
        if msg.lower() == 'q':
            break

        try:
            # Establish connection
            connection = http.client.HTTPConnection(SERVER_IP, PORT)
            
            # Send the POST request
            headers = {'Content-type': 'text/plain'}
            connection.request('POST', '/', msg.encode('utf-8'), headers)

            # Get the response from the server
            response = connection.getresponse()
            print(f"Status: {response.status}, Server says: {response.read().decode()}")
            
            connection.close()
        except Exception as e:
            print(f"Error connecting to server: {e}")

if __name__ == "__main__":
    send_message()
