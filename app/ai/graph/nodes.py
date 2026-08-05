from app.agents.image_prompt import ImagePromptAgent
from app.agents.research import ResearchAgent
from app.agents.scene_planner import ScenePlannerAgent
from app.agents.script import ScriptAgent

from app.ai.state.documentary_state import DocumentaryState
from app.schemas.request import DocumentaryRequest

from app.image_generation.services import (
    ImageGenerationService,
    ImageOutputManager,
)

from app.agents.animation_agent import AnimationAgent
from app.animation.services.animation_service import AnimationService


class DocumentaryNodes:
    def __init__(
        self,
        research_agent: ResearchAgent,
        script_agent: ScriptAgent,
        scene_planner_agent: ScenePlannerAgent,
        image_prompt_agent: ImagePromptAgent,
        animation_agent: AnimationAgent,
        animation_service: AnimationService,
        image_generation_service: ImageGenerationService | None = None,
        image_output_manager: ImageOutputManager | None = None,
    ):
        self.research_agent = research_agent
        self.script_agent = script_agent
        self.scene_planner_agent = scene_planner_agent
        self.image_prompt_agent = image_prompt_agent

        self.animation_agent = animation_agent
        self.animation_service = animation_service

        self.image_generation_service = (
            image_generation_service
            or ImageGenerationService()
        )

        self.image_output_manager = (
            image_output_manager
            or ImageOutputManager()
        )

    def research_node(
        self,
        state: DocumentaryState,
    ) -> dict:
        request = DocumentaryRequest(
            topic=state["topic"],
            language=state["language"],
            duration=state["duration"],
            style=state["style"],
        )

        research = self.research_agent.run(request)

        return {
            "research": research,
        }

    def script_node(
        self,
        state: DocumentaryState,
    ) -> dict:
        research = state["research"]

        if research is None:
            raise ValueError(
                "Research result is required before script generation."
            )

        script = self.script_agent.run(
            research=research,
            language=state["language"],
        )

        return {
            "script": script,
        }

    def scene_planner_node(
        self,
        state: DocumentaryState,
    ) -> dict:
        script = state["script"]

        if script is None:
            raise ValueError(
                "Script result is required before scene planning."
            )

        scenes = self.scene_planner_agent.run(
            script=script,
            duration=state["duration"],
        )

        return {
            "scenes": scenes,
        }

    def image_prompt_node(
        self,
        state: DocumentaryState,
    ) -> dict:
        scenes = state["scenes"]

        image_prompts = self.image_prompt_agent.run(
            scenes=scenes,
            style=state["style"],
        )

        return {
            "image_prompts": image_prompts,
        }


    def image_generation_node(
        self,
        state: DocumentaryState,
    ) -> dict:
        image_prompts = state.get(
            "image_prompts",
            [],
        )

        if not image_prompts:
            return {
                "images": [],
            }

        generated_images = (
            self.image_generation_service.generate_images(
                image_prompts=image_prompts,
            )
        )

        organized_images = (
            self.image_output_manager.save_images(
                images=generated_images,
                topic=state["topic"],
            )
        )

        return {
            "images": [
                image.path
                for image in organized_images
            ]
        }


    def animation_planning_node(
        self,
        state: DocumentaryState,
    ) -> dict:
        scenes = state.get(
            "scenes",
            [],
        )

        if not scenes:
            return {
                "animation_instructions": [],
            }

        instructions = self.animation_agent.run(
            scenes=scenes,
        )

        return {
            "animation_instructions": instructions,
        }


    def animation_generation_node(
        self,
        state: DocumentaryState,
    ) -> dict:
        images = state.get(
            "images",
            [],
        )

        instructions = state.get(
            "animation_instructions",
            [],
        )

        if not images or not instructions:
            return {
                "animations": [],
            }

        if len(images) != len(instructions):
            raise ValueError(
                "Images and animation instructions "
                "must have the same length."
            )

        animations = []

        for image_path, instruction in zip(
            images,
            instructions,
            strict=True,
        ):
            video = self.animation_service.generate_animation(
                image_path=image_path,
                prompt=instruction.prompt,
                negative_prompt=instruction.negative_prompt,
                camera_motion=instruction.camera_motion,
            )

            animations.append(
                video.path
            )

        return {
            "animations": animations,
        }