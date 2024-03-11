from .animal_crud import AnimalCRUD
from .urgent_case_crud import UrgentCaseCRUD
from .urgency_crud import UrgencyCRUD
from .ticket_crud import TicketCRUD
from .question_set_crud import QuestionSetCRUD
from .question_crud import QuestionCRUD
from .answer_record_crud import AnswerRecordCRUD
from .answer_crud import AnswerCRUD
from .ticket_question_crud import TicketQuestionCRUD

__all__ = ["AnimalCRUD", "UrgentCaseCRUD", "UrgencyCRUD", "TicketCRUD", "QuestionSetCRUD", "QuestionCRUD",
           "AnswerRecordCRUD", "AnswerCRUD", "TicketQuestionCRUD"]
