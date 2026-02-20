import os
import sys
import json
import ollama

model = "gemma3:1b"
haiku_prompt="Pick a random noun and write a haiku with that as the topic. Return only the poem."
context_file = "./haiku_context.txt"

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

def ollama_chat(prompt: str, model_name: str="gemma3:1b"):
    """
    Call and response version of Ollama with preserved context.
    Note that context will be preserved after client disconnect
    as long as this server script continues running.
    
    :param client_message: Message to generate response to.
    :param model_name: LLM model for Ollama to use.
    """
    global messages
    messages.append({"role": "user", "content": prompt})
    response = ollama.chat(model=model_name, messages=messages)
    answer = response.message.content
    messages.append({"role": "assistant", "content": answer})
    return answer


if __name__ == "__main__":

    # Pull model.
    try:
        ollama.pull(model)
    except Exception as e:
        print(e)
        sys.exit(1)

    # Check for haiku context file.
    if os.path.exists(context_file):
        messages = load_context_from_file(context_file)
    else:
        # Start new context file.
        messages = [\
            {"role": "system", "content": "You are a haiku poet. Make all responses brief."},
        ]
    response = ollama_chat(haiku_prompt, model_name=model)
    print("Model Response:")
    print(response)
    save_context_to_file(messages, context_file, silent=True)
