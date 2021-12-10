from enum import Enum

from consumer.analisis.cover import cover
from consumer.analisis.dice import dice


class AnalysisType(Enum):
    DICE = 1
    COVER = 2


AnalysisFunctions = {
    AnalysisType.DICE.name: dice,
    AnalysisType.COVER.name: cover
}
