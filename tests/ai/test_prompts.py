from langchain_core.prompts import ChatPromptTemplate

from app.ai.prompts.research import ResearchPrompt
from app.ai.prompts.script import ScriptPrompt


def test_research_prompt():

    prompt = ResearchPrompt.build()

    assert isinstance(prompt, ChatPromptTemplate)


def test_script_prompt():

    prompt = ScriptPrompt.build()

    assert isinstance(prompt, ChatPromptTemplate)