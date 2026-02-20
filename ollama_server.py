import os
import json
import ollama
from http.server import HTTPServer, BaseHTTPRequestHandler

"""
~~~ Ollama model recommendations ~~~
NOTE: Models must be pulled outside this script using
ollama pull <model_name>

tinyllama : Very fast but minimally helpful AI assistant.
gemma3 : Standard AI assistant, modest size.
gemma3:1b : Reduces size gemma3 model for improved speed.
"""

context_file = "./context.txt"

def save_context_to_file(data_list, filename, silent=False):
    """Writes a list of dictionaries to a text file in JSON format."""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            # indent=4 makes the text file human-readable
            json.dump(data_list, f, indent=4)
        if not silent:
            print(f"Successfully saved context to {filename}")
    except Exception as e:
        print(f"Error saving file: {e}")

def load_context_from_file(filename):
    """Reads a JSON text file and returns it as a list of dictionaries."""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        print("File not found.")
        return []
    except Exception as e:
        print(f"Error loading file: {e}")
        return []
    
def ollama_chat(client_message, model_name="gemma3:1b"):
    """
    Call and response version of Ollama with preserved context.
    Note that context will be preserved after client disconnect
    as long as this server script continues running.
    
    :param client_message: Message to generate response to.
    :param model_name: LLM model for Ollama to use.
    """
    global messages
    messages.append({"role": "user", "content": client_message})
    response = ollama.chat(model=model_name, messages=messages)
    answer = response.message.content
    messages.append({"role": "assistant", "content": answer})
    return answer

class MessageHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        # 1. Read the incoming message
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        client_message = post_data.decode('utf-8')
        print(f"[RECEIVED]: {client_message}")

        # 2. Pass the message into your function
        result = ollama_chat(client_message)

        # 3. Send the result back to the client
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        
        # Write the returned string from my_function back to the client
        self.wfile.write(result.encode('utf-8'))
        print(f"[SENT BACK]:\n{result}")

def loop(server_class=HTTPServer, handler_class=MessageHandler, port: int=8000, context_fname=None):
    server_address = ('0.0.0.0', port)
    httpd = server_class(server_address, handler_class)
    print(f"Server listening on port {port}...")
    print("Awaiting client message.")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nClosing HTTP server!\n")
        if context_file is not None:
            save_context_to_file(messages, context_fname)
        httpd.server_close()


if __name__ == "__main__":

    # 'messages' and 'context_file' are in global namespace
    if os.path.exists(context_file):
        print(f"Found context file at {context_file}. Loading.")
        messages = load_context_from_file(context_file)
    else:
        # Initialize conversation with a system prompt (optional) and a user message
        messages = [
            {"role": "system", "content": "You are a helpful assistant. Make all responses brief."},
            #{"role": "user", "content": "Hello!"},
        ]

    print(messages)

    loop(context_fname=context_file)
