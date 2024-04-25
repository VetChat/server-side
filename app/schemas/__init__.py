from .animal_schema import *
from .urgent_case_schema import *
from .urgency_schema import *
from .ticket_schema import *
from .symptom_schema import *
from .question_set_schema import *
from .question_schema import *
from .answer_schema import *
from .answer_record_schema import *
from .summary_schema import *
from .ticket_question_schema import *
from .breed_schema import *
from .ticket_answer_record_schema import *

__all__ = ["AnimalRead", "AnimalCreate", "AnimalResponse", "UrgentCaseWithUrgency", "UrgentCaseRead",
           "UrgencyRead", "UrgentCaseResponse", "UrgentCaseCreate", "UrgentCaseUpdate", "UrgentCaseBulkResponse",
           "UrgencyResponse", "UrgencyMostRequest", "TicketCreate", "TicketAnswer", "TicketId", "SymptomWithQuestions",
           "SymptomRead", "QuestionSetRequest", "QuestionResponse", "AnswerRead", "AnswerRecordCreate",
           "AnswerRecordResponse", "TicketSummaryResponse", "TicketQuestionRead", "TicketAnswerRead",
           "SymptomCreateBody", "SymptomResponse", "AnimalUpdate", "SymptomUpdate", "TicketInfo", "SymptomSummary",
           "AnswerSummary", "QuestionWithListAnswer", "UrgentCaseUpdateFailed", "UrgentCaseId", "QuestionSetCreateBody",
           "QuestionSetResponse", "TicketLabel", "TicketEachSummaryResponse", "TicketDataResponse",
           "QuestionWithListAnswerCreate", "AnswerResponse", "AnswerCreateFailed", "TicketAnswerRecordUpdate",
           "AnswerUpdate", "AnswerUpdateFailed", "QuestionId", "AnswerCreateUpdate", "TicketAnswerRecordUpdateResponse",
           "QuestionWithListAnswerUpdate", "QuestionWithListAnswerDeleteResponse",
           "QuestionWithListAnswerResponse", "QuestionCreateFailedResponse", "QuestionUpdateFailedResponse",
           "QuestionSetRead", "BreedRead", "BreedCreate", "BreedUpdate", "BreedCreateUpdateResponse",
           "QuestionWithListAnswerCreateUpdate", "QuestionDeleteResponse",
           "AnswerCreateUpdateDeleteBulkResponse", "AnswerDelete", "AnswerCreateUpdateDelete", "AnswerDeleteResponse",
           "AnswerCreateUpdateDeleteSuccessResponse", "AnswerCreateUpdateDeleteFailedResponse",
           "QuestionCreateUpdateDeleteSuccessResponse", "QuestionCreateUpdateDelete",
           "QuestionCreateUpdateDeleteFailedResponse", "QuestionCreateUpdateDeleteBulkResponse"]
