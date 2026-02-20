#!/home/dok/env/bin/python3

import ollama

if __name__ == "__main__":

    # Choose a chat-capable model (ensured it is pulled)
    model_name = 'llama2'

    print(f"Starting model {model_name}. Return empty prompt to quit.")

    # Initialize conversation with a system prompt (optional) and a user message
    messages = [
        {"role": "system", "content": "You are a helpful assistant. Make all responses brief."},
        {"role": "user", "content": "Hello!"},
    ]

    # First response from the bot
    response = ollama.chat(model=model_name, messages=messages)
    print("🤖:", response.message.content)

    # Continue the conversation:
    while True:
        user_input = input("👤: ")
        if not user_input:
            break  # exit loop on empty input
        messages.append({"role": "user", "content": user_input})
        response = ollama.chat(model=model_name, messages=messages)
        answer = response.message.content
        print("🤖:", answer)
        messages.append({"role": "assistant", "content": answer})
