import ollama

if __name__ == "__main__":
    result = ollama.generate(
        model='gemma3', 
        prompt="Pick a random noun and write a haiku with that as the topic. Return only the poem."
        )
    print(f"{result['response']}")
