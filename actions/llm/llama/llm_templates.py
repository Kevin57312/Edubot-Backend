from langchain.prompts.prompt import PromptTemplate
from llm.Utilities.utils_prompt import _consult_docente, _consult_grado

TEMPLATE_DOCENTE = PromptTemplate(
    input_variables=["docentes", "contenido"],
    template=_consult_docente,
)

TEMPLATE_GRADO = PromptTemplate(
    input_variables=["contenido"],
    template=_consult_grado,
)