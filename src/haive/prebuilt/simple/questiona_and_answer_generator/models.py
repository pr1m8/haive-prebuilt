from typing import Tuple

from haive.core.common.types import ABCRootWrapper


class Question(ABCRootWrapper[str]):
    pass


class Answer(ABCRootWrapper[str]):
    pass


class QuestionAndAnswer(ABCRootWrapper[Tuple[Question, Answer]]):
    pass
