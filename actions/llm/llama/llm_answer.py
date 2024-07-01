import os
from groq import Groq
from llm.Utilities.utils_config import OPENAI_API_KEY, OPENAI_MODEL_NAME

def llm_llama_answer(prompt, question = "Determina lo mencionado", temperatura = 0.1) :
    """Predict using a Large Language Model."""    
    client = Groq(api_key=OPENAI_API_KEY)

    messages = [
        {
            "role": "system",
            "content": prompt
        },
        {
            "role": "user",
            "content": question
        }
    ]
    
    chat_completion = client.chat.completions.create(
        messages=messages,
        model=OPENAI_MODEL_NAME,
        temperature=temperatura,
        max_tokens=1024,
        top_p=1,
        stream=False
    )

    try:
        answer = chat_completion.choices[0].message.content
        return answer
    except ValueError as e:
        print("Ocurrio un error en el LLM: ", e)
    
    return -1