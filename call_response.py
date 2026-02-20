#!/home/dok/env/bin/python3

import sys
import ollama

if __name__ == "__main__":
    question = sys.argv[1]
    print(f"Your question: {question}")

    # Use the generate function for a one-off prompt
    result = ollama.generate(model='llama2', prompt=question)
    print(f"My response: {result['response']}")
