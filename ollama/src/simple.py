import ollama

response = ollama.generate(model='stablelm2:12b',
prompt='what is a qubit?')
print(response['response'])