from langgraph.graph import END, START, StateGraph

from app.agents.animation_agent import AnimationAgent
from app.agents.image_prompt import ImagePromptAgent
from app.agents.research import ResearchAgent
from app.agents.scene_planner import ScenePlannerAgent
from app.agents.script import ScriptAgent

from app.ai.graph.nodes import DocumentaryNodes
from app.ai.state.documentary_state import DocumentaryState
from app.image_generation.services import ImageGenerationService

from app.image_generation.services import (
    ImageOutputManager,
)

from app.animation.services.animation_service import (
    AnimationService,
)

from app.voice.narration import NarrationService


def create_documentary_graph(
    research_agent: ResearchAgent | None = None,
    script_agent: ScriptAgent | None = None,
    scene_planner_agent: ScenePlannerAgent | None = None,
    image_prompt_agent: ImagePromptAgent | None = None,
    animation_agent: AnimationAgent | None = None,
    animation_service: AnimationService | None = None,
    narration_service: NarrationService | None = None,
    image_generation_service: ImageGenerationService | None = None,
    image_output_manager: ImageOutputManager | None = None,
):
    research_agent = research_agent or ResearchAgent()
    script_agent = script_agent or ScriptAgent()
    scene_planner_agent = (
        scene_planner_agent or ScenePlannerAgent()
    )
    image_prompt_agent = (
        image_prompt_agent or ImagePromptAgent()
    )

    if animation_agent is None:
            raise ValueError(
                "animation_agent is required."
            )
    
    if animation_service is None:
            raise ValueError(
                "animation_service is required."
            )

    nodes = DocumentaryNodes(
        research_agent=research_agent,
        script_agent=script_agent,
        scene_planner_agent=scene_planner_agent,
        image_prompt_agent=image_prompt_agent,
        animation_agent=animation_agent,
        animation_service=animation_service,
        narration_service=narration_service,
        image_generation_service=image_generation_service,
        image_output_manager=image_output_manager,
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

    workflow.add_node(
        "animation_planning",
        nodes.animation_planning_node,
    )

    workflow.add_node(
        "animation_generation",
        nodes.animation_generation_node,
    )

    workflow.add_node(
        "narration_generation",
        nodes.narration_generation_node,
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
        "animation_planning",
    )

    workflow.add_edge(
        "animation_planning",
        "animation_generation",
    )

    workflow.add_edge(
        "animation_generation",
        "narration_generation",
    )

    workflow.add_edge(
        "narration_generation",
        END,
    )

    return workflow.compile()