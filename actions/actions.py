from typing import Any, Text, Dict, List, Union
from actions.Flujos_WH.Modulo1 import Buscar_Tipo_Gestion_Docentes, enviar_todos_correos, transform_to_text
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import UserUtteranceReverted, SlotSet
from fuzzywuzzy import process

from rasa_sdk import FormValidationAction



class RevisarGestionEducativa(Action):

    def name(self) -> Text:
        return "action_revisar_gestion_educativa"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        tipo_gestion_entity = next(tracker.get_latest_entity_values('tipo_gestion'), None)
        course_entity = next(tracker.get_latest_entity_values('curso'), None)

        best_match_tipo_gestion = None
        best_match_course = None
        respuesta = ""

        array_gestion = ["sesiones de aprendizaje", "unidades de aprendizaje", "planificacion anual"]
        array_cursos = [
            "Matematica",
            "Comunicacion",
            "Educacion para el trabajo",
            "Arte y cultura",
            "Ciencias sociales",
            "Religion",
            "Desarrollo personal ciudadania y civica",
            "Ciencia y tecnologia",
            "Ingles"
        ]

        if tipo_gestion_entity:
            best_match_tipo_gestion, score = process.extractOne(tipo_gestion_entity, array_gestion)
            threshold = 75

            if score < threshold:
                respuesta = "No se especifico de manera clara el tipo de gestion, recuerda que son solo 3 los posibles"
                dispatcher.utter_message(respuesta)
                return []
            
        if course_entity:
            best_match_course, score = process.extractOne(tipo_gestion_entity, array_cursos)
            threshold = 75
            if score < threshold:
                best_match_course = None

        dict_cursos, dict_grados = Buscar_Tipo_Gestion_Docentes(tipo_gestion=best_match_tipo_gestion, curso= best_match_course)
        answer = transform_to_text(dict_cursos, dict_grados)

        dispatcher.utter_message(answer)
        return [
            SlotSet("my_total_cursos", dict_cursos),
            SlotSet("my_total_grados", dict_grados),
            SlotSet("name_gestion", best_match_tipo_gestion)
        ]


class ActionCostumFallback(Action):

    def name(self) -> Text:
        return "action_custom_fallback"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(response = 'utter_costum')

        return [UserUtteranceReverted()]

class ActionEnviarCorreos(Action):

    def name(self) -> Text:
        return "action_enviar_correos"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        dict_cursos = tracker.get_slot("my_total_cursos")
        dict_grados = tracker.get_slot("my_total_grados")
        tipo_gestion = tracker.get_slot("name_gestion")

        slots_to_reset = [
            "my_total_cursos",
            "my_total_grados",
            "tipo_gestion",
            "curso",
            "name_gestion",
        ]

        reset_events = [SlotSet(slot, None) for slot in slots_to_reset]

        enviar_todos_correos(dict_cursos, dict_grados, tipo_gestion)
        
        dispatcher.utter_message("Correos enviados! 😊")

        return reset_events
    

class ValidateFullForm(FormValidationAction):

    def name(self) -> str:
        return "validate_full_form"

    def validate_question_1(
        self,
        value: str,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[str, Any],
    ) -> Dict[str, Any]:
        
        print("valor 1",value)
        if value.lower() in ["strongly agree", "agree", "neutral", "disagree", "strongly disagree"]:
            return {"question_1": value}
        else:
            dispatcher.utter_message(text="Please select a valid response.")
            return {"question_1": None}

    def validate_question(
        self,
        value: str,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[str, Any],
    ) -> Dict[str, Any]:
        
        
        if value.lower() in ["strongly agree", "agree", "neutral", "disagree", "strongly disagree"]:
            return {"question_2": value}
        else:
            dispatcher.utter_message(text="Please select a valid response.")
            return {"question_2": None}