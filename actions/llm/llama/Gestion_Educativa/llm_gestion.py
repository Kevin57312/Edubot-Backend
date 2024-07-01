from llm.llama.llm_answer import llm_llama_answer
from llm.llama.llm_prompts import questions_prompts
import re


def search_docente(contenido, docentes):
    define_prompts = questions_prompts()
    prompt = define_prompts.EXTRACT_TEACHER_NAME(contenido, docentes)
    answer = llm_llama_answer(prompt, temperatura= 0.5)

    clean_answer = answer.replace("\n", "")
    patron = r'\[Docente\]:\s*(.+)'
    resultado = re.search(patron, clean_answer)

    if resultado:
        resultado = resultado.group(1)
        return resultado
    
    print("No se encontró un docente")
    return -1

def search_grado(contenido):
    define_prompts = questions_prompts()
    prompt = define_prompts.EXTRACT_GRADO(contenido)
    answer = llm_llama_answer(prompt, temperatura= 0.5)

    clean_answer = answer.replace("\n", "")
    patron = r'\[Grado\]:\s*(.+)'
    resultado = re.search(patron, clean_answer)

    if resultado:
        resultado = resultado.group(1)
        return resultado
    
    print("No se encontró un Grado")
    return -1
