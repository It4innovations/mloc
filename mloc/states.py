from enum import Enum


class General(Enum):
    def __str__(self):
        return str(self.value)

    RUNNING = 'running'
    ERROR = 'error'
    FINISHED = 'finished'


class NetworkState(Enum):
    COMPILING = 'compiling'
    COMPILED = 'compiled'


class FitState(Enum):
    FITTING = 'fitting'
    FITTED = 'fitted'


class EvaluationState(Enum):
    EVALUATING = 'evaluating'
    EVALUATED = 'evaluated'


class PredictionState(Enum):
    PREDICTING = 'evaluating'
    PREDICTED = 'evaluated'
