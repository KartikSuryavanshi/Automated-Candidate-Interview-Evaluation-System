from pydantic import BaseModel


class InterviewStartPayload(BaseModel):
    action: str
    topic: str


class InterviewAnswerPayload(BaseModel):
    action: str
    answer: str


class InterviewStopPayload(BaseModel):
    action: str
