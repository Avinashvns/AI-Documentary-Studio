from langgraph.graph import END, START, StateGraph

from app.agents.image_prompt import ImagePromptAgent
from app.agents.research import ResearchAgent
from app.agents.scene_planner import ScenePlannerAgent
from app.agents.script import ScriptAgent

from app.ai.graph.nodes import DocumentaryNodes
from app.ai.state.documentary_state import DocumentaryState
from app.image_generation.services import ImageGenerationService


def create_documentary_graph(
    research_agent: ResearchAgent | None = None,
    script_agent: ScriptAgent | None = None,
    scene_planner_agent: ScenePlannerAgent | None = None,
    image_prompt_agent: ImagePromptAgent | None = None,
    image_generation_service: ImageGenerationService | None = None,
):
    research_agent = research_agent or ResearchAgent()
    script_agent = script_agent or ScriptAgent()
    scene_planner_agent = (
        scene_planner_agent or ScenePlannerAgent()
    )
    image_prompt_agent = (
        image_prompt_agent or ImagePromptAgent()
    )

    nodes = DocumentaryNodes(
        research_agent=research_agent,
        script_agent=script_agent,
        scene_planner_agent=scene_planner_agent,
        image_prompt_agent=image_prompt_agent,
        image_generation_service=image_generation_service,
    )

    workflow = StateGraph(DocumentaryState)

    workflow.add_node(
        "research",
        nodes.research_node,
    )

    workflow.add_node(
        "script",
        nodes.script_node,
    )

    workflow.add_node(
        "scene_planner",
        nodes.scene_planner_node,
    )

    workflow.add_node(
        "image_prompt",
        nodes.image_prompt_node,
    )

    workflow.add_node(
        "image_generation",
        nodes.image_generation_node,
    )

    workflow.add_edge(
        START,
        "research",
    )

    workflow.add_edge(
        "research",
        "script",
    )

    workflow.add_edge(
        "script",
        "scene_planner",
    )

    workflow.add_edge(
        "scene_planner",
        "image_prompt",
    )

    workflow.add_edge(
        "image_prompt",
        "image_generation",
    )

    workflow.add_edge(
        "image_generation",
        END,
    )

    return workflow.compile()