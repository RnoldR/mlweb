import ollama

def translate_into_english(prompt: str, model: str) -> str:
    prompt = 'Vertaal in het Engels: ' + prompt
    response = ollama.generate(model=model,
                            prompt=prompt)

    return response['response']

### translate_into_english ###


def translate_into_duits(prompt: str, model: str) -> str:
    prompt = 'Vertaal in het Duits: ' + prompt
    response = ollama.generate(model=model,
                            prompt=prompt)

    return response['response']

### translate_into_english ###


def generate_response(prompt: str, model: str) -> str:

        
    response = ollama.generate(model=model,
                            prompt=prompt)

    return response['response']

### generate_response ###


antwoord = generate_response('Geef kort je mening over Spinoza',
                             'stablelm2:12b')
print(antwoord)
print('\n-----\n')

for i in range(1, 4):
    antwoord = generate_response('Parafraseer kort: ' + antwoord, 'glm4')
    print('***', i, "***", antwoord)
    print('\n-----\n')

"""
antwoord = translate_into_english(antwoord, 'stablelm2:12b')
print(antwoord)
print('\n-----\n')

antwoord = translate_into_duits(antwoord, 'stablelm2:12b')
print(antwoord)
print('\n-----\n')
"""

