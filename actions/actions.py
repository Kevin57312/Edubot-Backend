from typing import Any, Text, Dict, List
from actions.Flujos_WH.Modulo1 import Buscar_Tipo_Gestion_Docentes, enviar_todos_correos, transform_to_text
from actions.Flujos_WH.Modulo2 import assign_scores_in_sheet, validar_docente, validate_folder
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import UserUtteranceReverted, SlotSet
from fuzzywuzzy import process
from rasa_sdk.types import DomainDict
from rasa_sdk import FormValidationAction
import re
from rasa_sdk.events import Form


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

class ActionEnviarFormulario(Action):

    def name(self) -> Text:
        return "action_enviar_formulario"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        my_dict = dict()
        len_preguntas = [5,7,4]
        labels = ["pc", "cm", "re"]
        j = 0

        #Guardo en el diccionario las preguntas
        for len in len_preguntas:
            list_questions = list()
            label = labels[j]
            for i in range(len):
                tracker_item = tracker.get_slot(f"{label}_question_{i+1}")
                list_questions.append(tracker_item) 
            my_dict[label] = list_questions
            j +=1

        tracker_docente = tracker.get_slot("docente")
        tracker_gradoysec = tracker.get_slot("gradoysec")
        tracker_sesion = tracker.get_slot("sesion")

        my_dict["docente"] = tracker_docente
        my_dict["gradoysec"] = tracker_gradoysec
        my_dict["sesion"] = tracker_sesion
        assign_scores_in_sheet(my_dict, len_preguntas, labels)

        return []


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
    

class ValidatePlanCurricularForm(FormValidationAction):

    def name(self) -> str:
        return "validate_plan_curricular_form"

    def validate_pc_question_1(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[str, Any]:
        match = re.search(r'\b[1-4]\b', slot_value)
        if not match:
            dispatcher.utter_message(text="Debe ser un valor entre 1 y 4")
            return {"pc_question_1": None}
        
        return {"pc_question_1": match.group()}
    
    def validate_pc_question_2(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[str, Any]:
        match = re.search(r'\b[1-4]\b', slot_value)
        if not match:
            dispatcher.utter_message(text="Debe ser un valor entre 1 y 4")
            return {"pc_question_2": None}
        
        return {"pc_question_2": match.group()}
    
    def validate_pc_question_3(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[str, Any]:
        match = re.search(r'\b[1-4]\b', slot_value)
        if not match:
            dispatcher.utter_message(text="Debe ser un valor entre 1 y 4")
            return {"pc_question_3": None}
        
        return {"pc_question_3": match.group()}
    
    def validate_pc_question_4(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[str, Any]:
        match = re.search(r'\b[1-4]\b', slot_value)
        if not match:
            dispatcher.utter_message(text="Debe ser un valor entre 1 y 4")
            return {"pc_question_4": None}
        
        return {"pc_question_4": match.group()}
    
    def validate_pc_question_5(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[str, Any]:
        match = re.search(r'\b[1-4]\b', slot_value)
        if not match:
            dispatcher.utter_message(text="Debe ser un valor entre 1 y 4")
            return {"pc_question_5": None}
        
        return {"pc_question_5": match.group()}
    
    def submit(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        # Puedes realizar acciones finales aquí después de validar todos los slots
        return [Form("validate_conduccion_mediacion_form")]


class ValidateConduccionMediacionForm(FormValidationAction):

    def name(self) -> str:
        return "validate_conduccion_mediacion_form"
    
    def validate_cm_question_1(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[str, Any]:
        match = re.search(r'\b[1-4]\b', slot_value)
        if not match:
            dispatcher.utter_message(text="Debe ser un valor entre 1 y 4")
            return {"cm_question_1": None}
        
        return {"cm_question_1": match.group()}
    

    def validate_cm_question_2(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[str, Any]:
        match = re.search(r'\b[1-4]\b', slot_value)
        if not match:
            dispatcher.utter_message(text="Debe ser un valor entre 1 y 4")
            return {"cm_question_2": None}
        
        return {"cm_question_2": match.group()}
    
    def validate_cm_question_3(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[str, Any]:
        match = re.search(r'\b[1-4]\b', slot_value)
        if not match:
            dispatcher.utter_message(text="Debe ser un valor entre 1 y 4")
            return {"cm_question_3": None}
        
        return {"cm_question_3": match.group()}
    
    def validate_cm_question_4(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[str, Any]:
        match = re.search(r'\b[1-4]\b', slot_value)
        if not match:
            dispatcher.utter_message(text="Debe ser un valor entre 1 y 4")
            return {"cm_question_4": None}
        
        return {"cm_question_4": match.group()}
    
    def validate_cm_question_5(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[str, Any]:
        match = re.search(r'\b[1-4]\b', slot_value)
        if not match:
            dispatcher.utter_message(text="Debe ser un valor entre 1 y 4")
            return {"cm_question_5": None}
        
        return {"cm_question_5": match.group()}
    
    def validate_cm_question_6(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[str, Any]:
        match = re.search(r'\b[1-4]\b', slot_value)
        if not match:
            dispatcher.utter_message(text="Debe ser un valor entre 1 y 4")
            return {"cm_question_6": None}
        
        return {"cm_question_6": match.group()}
    
    def validate_cm_question_7(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[str, Any]:
        match = re.search(r'\b[1-4]\b', slot_value)
        if not match:
            dispatcher.utter_message(text="Debe ser un valor entre 1 y 4")
            return {"cm_question_7": None}
        
        return {"cm_question_7": match.group()}
    
    def submit(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        # Puedes realizar acciones finales aquí después de validar todos los slots
        return [Form("validate_retroalimentacion_evaluacion_form")]


class ValidateRetroalimentacionEvaluacionForm(FormValidationAction):

    def name(self) -> str:
        return "validate_retroalimentacion_evaluacion_form"
    
    def validate_re_question_1(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[str, Any]:
        match = re.search(r'\b[1-4]\b', slot_value)
        if not match:
            dispatcher.utter_message(text="Debe ser un valor entre 1 y 4")
            return {"re_question_1": None}
        
        return {"re_question_1": match.group()}
    
    def validate_re_question_2(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[str, Any]:
        match = re.search(r'\b[1-4]\b', slot_value)
        if not match:
            dispatcher.utter_message(text="Debe ser un valor entre 1 y 4")
            return {"re_question_2": None}
        
        return {"re_question_2": match.group()}
    
    def validate_re_question_3(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[str, Any]:
        match = re.search(r'\b[1-4]\b', slot_value)
        if not match:
            dispatcher.utter_message(text="Debe ser un valor entre 1 y 4")
            return {"re_question_3": None}
        
        return {"re_question_3": match.group()}
    
    def validate_re_question_4(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[str, Any]:
        match = re.search(r'\b[1-4]\b', slot_value)
        if not match:
            dispatcher.utter_message(text="Debe ser un valor entre 1 y 4")
            return {"re_question_4": None}
        
        return {"re_question_4": match.group()}
    

class ValidateDatosForm(FormValidationAction):

    def name(self) -> str:
        return "validate_datos_form"
    
    def validate_docente(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[str, Any]:
        
        docente_filtrado = validar_docente(slot_value)
        if (docente_filtrado == "-1"):
            dispatcher.utter_message(text="No se encontro el docente, por favor mencione uno valido")
            return {"docente": None}

        validate_folder(docente_filtrado)
        return {"docente": docente_filtrado}
    
    def validate_sesion(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[str, Any]:
        
        if not slot_value:
            dispatcher.utter_message(text="Ingrese el nombre de la sesion, por favor")
            return {"sesion": None}

        return {"sesion": slot_value}
    
    def validate_gradoysec(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[str, Any]:
        
        pattern = r'[1-4][A-D]'
        matches = re.findall(pattern, slot_value)

        if(not matches):
            dispatcher.utter_message(text="Debe ingresar un grado y seccion en el formato solicitado")
            return {"gradoysec": None}

        if(len(matches) > 1):
            dispatcher.utter_message(text="Se identificaron varios secciones y grados, por favor solo ingrese uno con el formato")
            return {"gradoysec": None}
        print("nuevo lugar")
        return {"gradoysec": matches[0]}

class ValidateFullForm(FormValidationAction):

    def name(self) -> str:
        return "validate_full_form"

    def validate_question_1(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[str, Any]:
        
        if not (slot_value in ["1","2","3","4","5"]):
            dispatcher.utter_message(text="Debe ser un valor entre 1 y 4")
            return {"question_1": No    ne}
    
        return {"question_1": slot_value}
    

    def validate_question_2(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[str, Any]:
        
        if not (slot_value in ["1","2","3","4","5"]):
            dispatcher.utter_message(text="Debe ser un valor entre 1 y 4")
            return {"question_2": None}
    
        return {"question_2": slot_value}
    

    def validate_question_3(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[str, Any]:
        
        if not (slot_value in ["1","2","3","4","5"]):
            dispatcher.utter_message(text="Debe ser un valor entre 1 y 4")
            return {"question_3": None}
    
        return {"question_3": slot_value}
    

    def validate_question_4(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[str, Any]:
        
        if not (slot_value in ["1","2","3","4","5"]):
            dispatcher.utter_message(text="Debe ser un valor entre 1 y 4")
            return {"question_4": None}
    
        return {"question_4": slot_value}
    

    def validate_question_5(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[str, Any]:
        
        if not (slot_value in ["1","2","3","4","5"]):
            dispatcher.utter_message(text="Debe ser un valor entre 1 y 4")
            return {"question_5": None}
    
        return {"question_5": slot_value}