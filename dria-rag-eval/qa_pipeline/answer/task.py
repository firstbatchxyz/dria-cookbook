from typing import List, Sequence, Type

from dria import SingletonTemplate
from dria.models import TaskResult
from pydantic import BaseModel, Field

from dria_workflows import *
from dria.factory.utilities import get_tags, parse_json, get_abs_path

class AnswerOutput(BaseModel):
    persona: str = Field(...,description="Persona")
    question: str = Field(...,description="Question")
    context: str = Field(...,description="Context")
    answer: str = Field(...,description="Question")

class AnswerGeneration(SingletonTemplate):
    persona: str = Field(...,description="Persona")
    question: str = Field(...,description="Question")
    context: str = Field(...,description="Context")
    
    OutputSchema=AnswerOutput

    def workflow(self):    
        builder = WorkflowBuilder(question=self.question,context=self.context)
        builder.set_max_tokens(800)
        builder.set_max_time(65)
        builder.set_max_steps(3)

        builder.generative_step(
            path=get_abs_path("prompt.md"),
            operator=Operator.GENERATION,
            outputs=[Write.new("output")],
        )

        flow = [Edge(source="0", target="_end")]

        builder.flow(flow)
        builder.set_return_value("output")
        return builder.build()
    
    def callback(self, result: List[TaskResult]) -> List[AnswerOutput]:
        results = []
        for r in result:
            results.append(
                    AnswerOutput(
                        answer=r.result.strip(),
                        persona=self.persona,
                        context=self.context,
                        question=self.question
                    )
                )
        return results 
