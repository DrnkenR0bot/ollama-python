import http.client

# Use the IP address of the server computer
SERVER_IP = 'vision.lan' 
PORT = 8000

def send_message():
    while True:
        msg = input("\nEnter text to process (or 'q' to quit): ")
        if msg.lower() == 'q':
            break

        try:
            conn = http.client.HTTPConnection(SERVER_IP, PORT)
            headers = {'Content-type': 'text/plain'}
            
            # Sending the request
            conn.request('POST', '/', msg.encode('utf-8'), headers)

            # Receiving the processed result
            response = conn.getresponse()
            server_output = response.read().decode('utf-8')
            
            print("--- Result from Server ---")
            print(server_output)
            
            conn.close()
        except Exception as e:
            print(f"Connection error: {e}")

if __name__ == "__main__":
    send_message()
