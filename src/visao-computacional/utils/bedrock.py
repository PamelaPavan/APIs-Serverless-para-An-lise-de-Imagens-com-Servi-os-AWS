import json 
from typing import Tuple

def prepare_bedrock(prompt: str) -> Tuple[str, str, str]:
    """
    Prepares the input prompt and configuration for the Amazon Titan text generation model.

    :param prompt (str): The input labels about a pet.

    :return Tuple[str, str, str]: A tuple containing the formatted prompt, model ID, and the JSON request string.
    """
    # Seta o model id
    model_id = "amazon.titan-text-premier-v1:0"

    # Define o prompt
    prompt = f"""
    Vou fornecer labels sobre um pet no fim do contexto. Esses labels acima foram retirados de uma resposta do aws rekognition. 
    Neles deve incluir um ou mais animais, o tipo do animal e seus sub-tipos, de acordo com cada representação de label que temos como resposta.
    Teremos um label que representa a raça desse animal. Com base em cada uma das raças, eu gostaria de uma resposta que contesse as seguintes informações:
    Nível de energia e necessidades de exercícios, Temperamento e Comportamento, Cuidados e Necessidades, Problemas de Saúde Comuns.
    Labels: {prompt}. 
    Para cada uma das raças encontradas nos labels acima, você deve me retornar uma resposta como a seguinte, trocando RAÇA pela raça encontrada no label e traduzida para pt-BR:
    Dicas sobre a RAÇA:
    Nível de energia: em pt-BR qual o nível de energia e quanto exercício diário é recomendado.
    Temperamento e Comportamento: em pt-BR qual o temperamento e comportamento.
    Cuidados e Necessidades: em pt-BR qual os cuidados e necessidades.
    Problemas de Saúde Comuns: em pt-BR qual os problemas de saúde comuns.
    """
    
    # Formata o request
    native_request = {
        "inputText": prompt,
        "textGenerationConfig": {
            "maxTokenCount": 1024,
            "temperature": 0.5,
        },
    }

    # Coverte o request para json
    request = json.dumps(native_request)

    return prompt, model_id, request