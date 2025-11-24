import google.generativeai as genai 
import json

genai.configure(api_key='')

async def generate_playlist_suggestions(data):
    prompt = f"""
        Você é um especialista em curadoria musical. Sua tarefa é montar playlists altamente personalizadas com base nas preferências do usuário.

        Objetivo: Selecione exatamente {data.limit} músicas que combinem com os seguintes critérios:
        - Humor desejado: {data.mood}
        - Horário do dia: {data.time}
        - Objetivo do momento: {data.goal}
        - Gêneros preferidos: {data.genres}
        - Ritmo: {data.rhythm}
        - Nível de novidade das músicas: {data.novelty}
        - Idiomas desejados: {data.languages}
        - Tema adicional (opcional): {data.obs}

        Instruções:
        - Escolha músicas que combinem fortemente com essas características.
        - Priorize variedade dentro do estilo escolhido.
        - Caso alguma combinação faça sentido criativo, justifique brevemente no campo "why".
        - Crie um nome de até no máximo 2 palavras para essa playlist de acordo com as informações adquiridas e músicas escolhidas.

        Resposta obrigatória: Retorne apenas um JSON válido, seguindo exatamente este formato:
        [
        {{
            "name_playlist": "nome da playlist",
            "tracks": [
                {{
                    "title": "Nome da música",
                    "artist": "Artista",
                    "genre": "Gênero predominante",
                    "why": "Explicação curta sobre por que esta música combina com o perfil"
                }},
                {{
                    "title": "Nome da música",
                    "artist": "Artista",
                    "genre": "Gênero predominante",
                    "why": "Explicação curta sobre por que esta música combina com o perfil"
                }}
            ]
        }}
        ]

        NÃO inclua explicações fora do JSON, nem textos adicionais, nem markdown.
    """

    model = genai.GenerativeModel('gemini-2.0-flash')
    result = model.generate_content(prompt, generation_config={"response_mime_type": "application/json"})

    try:
        return json.loads(result.text)
    except json.JSONDecodeError:
        print("\nGemini retornou JSON inválido:")
        print(result)
        raise
