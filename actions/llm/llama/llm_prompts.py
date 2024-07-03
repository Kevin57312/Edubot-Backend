from actions.llm.llama.llm_templates import TEMPLATE_DOCENTE, TEMPLATE_GRADO

class questions_prompts:
    def __init__(self,question=None):
        self.question = question

    def EXTRACT_TEACHER_NAME(self, contenido, docentes):

        final_prompt = TEMPLATE_DOCENTE.format(
            docentes= docentes,
            contenido = contenido, 
        )
        return final_prompt
    
    def EXTRACT_GRADO(self, contenido):

        final_prompt = TEMPLATE_GRADO.format(
            contenido = contenido
        )
        return final_prompt