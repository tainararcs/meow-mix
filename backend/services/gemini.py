import google.generativeai as genai 
import dotenv
import json
import os


dotenv.load_dotenv()
genai.configure(api_key=os.getenv('API_KEY'))

# Lista fixa de tags permitidas para a capa da playlist
possible_tags = [
    'angry', 'asleep', 'bobo', 'business', 'cute', 'dark', 'dunny', 'evil', 'fierce', 'focused', 
    'fluffy', 'happy', 'lazy', 'love', 'lovely', 'party', 'reading', 'relaxed', 'sad', 'sleep',
    'soft', 'summer', 'thinking', 'tummy', 'unhappy', 'valentine', 'working'
]

async def generate_playlist_suggestions(data) -> dict:
    '''
        Gera sugestões de playlist utilizando o modelo Gemini (Google Generative AI).
        Envia um prompt estruturado com as preferências do usuário e solicita que o modelo retorne um JSON contendo:
            - Nome da playlist
            - Uma tag visual (restrita a uma lista pré-definida)
            - Uma lista de músicas (título, artista e gênero)

        Args:
            data (PlaylistRequest): Objeto contendo todas as preferências selecionadas pelo usuário.

        Returns:
            dict: Objeto Python resultante da conversão do JSON retornado pelo modelo, no seguinte formato:
            {
                "playlist_name": str,
                "tag": str,
                "tracks": [
                    {
                        "title": str,
                        "artist": str,
                        "genre": str
                    }
                ]
            }

        Raises:
            json.JSONDecodeError: Caso o Gemini retorne uma resposta que não seja um JSON válido.
    '''
    allowed_tags = ", ".join(possible_tags)

    prompt = f'''
        Você é um especialista em curadoria musical. Sua tarefa é montar playlists altamente personalizadas com base nas preferências do usuário.

        Objetivo: Selecione exatamente {data.limit} músicas que combinem com os seguintes critérios:
        - Humor desejado: {data.mood}
        - Horário do dia: {data.timeOfDay}
        - Objetivo do momento: {data.goal}
        - Gêneros escolhidos: {data.genres}
        - Ritmo: {data.rhythm}
        - Nível de novidade das músicas: {data.novelty}
        - Idiomas desejados: {data.language}
        - Informações adicionais quanto à playlist (opcional): {data.obs}

        Instruções:
        - Escolha músicas que combinem fortemente com essas características.
        - Priorize variedade dentro do estilo escolhido.
        - Caso alguma combinação faça sentido criativo, justifique brevemente no campo "why".
        - Crie um nome criativo de até no máximo 3 palavras para essa playlist de acordo com as informações adquiridas e músicas escolhidas.
        - A tag deve ser escolhida EXCLUSIVAMENTE entre esta lista fixa de tags permitidas: {allowed_tags}.
          Você NÃO pode criar novas tags e NÃO pode usar nada fora dessa lista. Caso nenhuma tag combine perfeitamente, escolha a mais próxima DENTRO da lista.
        
        Resposta obrigatória: Retorne apenas um JSON válido, seguindo exatamente este formato:
        {{
            "playlist_name": "nome da playlist",
            "tag": "tag escolhida por você",
            "tracks": [
                {{
                    "title": "Nome da música",
                    "artist": "Artista",
                    "genre": "Gênero predominante",
                }},
                {{
                    "title": "Nome da música",
                    "artist": "Artista",
                    "genre": "Gênero predominante",
                }}
            ]
        }}

        NÃO inclua explicações fora do JSON, nem textos adicionais, nem markdown.
    '''

    model = genai.GenerativeModel('gemini-2.5-flash')
    result = model.generate_content(prompt, generation_config={'response_mime_type': 'application/json'})

    try:
        return json.loads(result.text)
    except json.JSONDecodeError:
        print('\nGemini retornou JSON inválido:\n')
        print(result)
        raise
