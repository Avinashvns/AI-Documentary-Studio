from unittest.mock import MagicMock

from app.ai.graph.documentary_graph import create_documentary_graph
from app.animation.models import GeneratedVideo
from app.image_generation.models import GeneratedImage
from app.schemas.animation import AnimationInstruction
from app.schemas.image_prompt import ImagePrompt
from app.schemas.research import ResearchResult
from app.schemas.scene import Scene
from app.schemas.script import ScriptResult, ScriptSection


def test_documentary_graph():
    research_result = ResearchResult(
        topic="Mughal Empire",
        summary="History of the Mughal Empire.",
        timeline=[],
        characters=[],
        sources=[],
    )

    script_result = ScriptResult(
        title="The Mughal Empire",
        hook="An empire that changed history.",
        introduction="The story begins in the sixteenth century.",
        sections=[
            ScriptSection(
                title="The Beginning",
                narration="Babur entered northern India.",
            )
        ],
        ending="The empire left a lasting legacy.",
        cta="Subscribe for more documentaries.",
    )

    scenes = [
        Scene(
            number=1,
            title="The Beginning",
            narration="Babur entered northern India.",
            duration=30,
        )
    ]

    image_prompts = [
        ImagePrompt(
            scene_number=1,
            prompt=(
                "Babur entering northern India, historical "
                "Mughal setting, cinematic lighting, "
                "photorealistic documentary style"
            ),
            negative_prompt=(
                "modern clothing, cars, text, watermark"
            ),
        )
    ]

    generated_images = [
        GeneratedImage(
            path="ComfyUI_00001_.png",
            width=768,
            height=432,
            format="png",
            provider="local",
        )
    ]

    organized_images = [
        GeneratedImage(
            path=(
                "outputs/documentaries/"
                "mughal-empire/images/scene_001.png"
            ),
            width=768,
            height=432,
            format="png",
            provider="local",
        )
    ]

    animation_instructions = [
        AnimationInstruction(
            scene_number=1,
            prompt=(
                "cinematic historical documentary, "
                "subtle natural movement"
            ),
            negative_prompt=(
                "flickering, jitter, watermark"
            ),
            camera_motion="Zoom In",
        )
    ]

    generated_video = GeneratedVideo(
        path=(
            "outputs/documentaries/"
            "mughal-empire/animations/"
            "scene_001.mp4"
        ),
        width=512,
        height=512,
        fps=16,
        frame_count=33,
        provider="comfyui",
    )

    research_agent = MagicMock()
    research_agent.run.return_value = research_result

    script_agent = MagicMock()
    script_agent.run.return_value = script_result

    scene_planner_agent = MagicMock()
    scene_planner_agent.run.return_value = scenes

    image_prompt_agent = MagicMock()
    image_prompt_agent.run.return_value = image_prompts

    image_generation_service = MagicMock()
    image_generation_service.generate_images.return_value = (
        generated_images
    )

    image_output_manager = MagicMock()
    image_output_manager.save_images.return_value = (
        organized_images
    )

    animation_agent = MagicMock()
    animation_agent.run.return_value = (
        animation_instructions
    )

    animation_service = MagicMock()
    animation_service.generate_animation.return_value = (
        generated_video
    )

    graph = create_documentary_graph(
        research_agent=research_agent,
        script_agent=script_agent,
        scene_planner_agent=scene_planner_agent,
        image_prompt_agent=image_prompt_agent,
        animation_agent=animation_agent,
        animation_service=animation_service,
        image_generation_service=image_generation_service,
        image_output_manager=image_output_manager,
    )

    initial_state = {
        "topic": "Mughal Empire",
        "language": "Hindi",
        "duration": 10,
        "style": "historical documentary",
        "research": None,
        "script": None,
        "scenes": [],
        "image_prompts": [],
        "images": [],
        "animation_instructions": [],
        "animations": [],
        "narration": "",
        "audio_path": "",
        "music_path": "",
        "subtitles_path": "",
        "output_video": "",
    }

    result = graph.invoke(initial_state)

    assert result["topic"] == "Mughal Empire"
    assert result["research"] == research_result
    assert result["script"] == script_result
    assert result["scenes"] == scenes
    assert result["image_prompts"] == image_prompts

    assert result["images"] == [
        (
            "outputs/documentaries/"
            "mughal-empire/images/scene_001.png"
        )
    ]

    assert (
        result["animation_instructions"]
        == animation_instructions
    )

    assert result["animations"] == [
        (
            "outputs/documentaries/"
            "mughal-empire/animations/"
            "scene_001.mp4"
        )
    ]

    research_agent.run.assert_called_once()

    script_agent.run.assert_called_once_with(
        research=research_result,
        language="Hindi",
    )

    scene_planner_agent.run.assert_called_once_with(
        script=script_result,
        duration=10,
    )

    image_prompt_agent.run.assert_called_once_with(
        scenes=scenes,
        style="historical documentary",
    )

    image_generation_service.generate_images.assert_called_once_with(
        image_prompts=image_prompts,
    )

    image_output_manager.save_images.assert_called_once_with(
        images=generated_images,
        topic="Mughal Empire",
    )

    animation_agent.run.assert_called_once_with(
        scenes=scenes,
    )

    animation_service.generate_animation.assert_called_once_with(
        image_path=(
            "outputs/documentaries/"
            "mughal-empire/images/"
            "scene_001.png"
        ),
        prompt=animation_instructions[0].prompt,
        negative_prompt=(
            animation_instructions[0].negative_prompt
        ),
        camera_motion=(
            animation_instructions[0].camera_motion
        ),
    )


def test_documentary_graph_execution_order():
    execution_order = []

    research_result = ResearchResult(
        topic="Mughal Empire",
        summary="History",
        timeline=[],
        characters=[],
        sources=[],
    )

    script_result = ScriptResult(
        title="The Mughal Empire",
        hook="Hook",
        introduction="Introduction",
        sections=[],
        ending="Ending",
        cta="CTA",
    )

    scenes = [
        Scene(
            number=1,
            title="Beginning",
            narration="Narration",
            duration=30,
        )
    ]

    image_prompts = [
        ImagePrompt(
            scene_number=1,
            prompt="Historical cinematic documentary image",
            negative_prompt="text, watermark",
        )
    ]

    generated_images = [
        GeneratedImage(
            path="ComfyUI_00001_.png",
            width=768,
            height=432,
            format="png",
            provider="local",
        )
    ]

    organized_images = [
        GeneratedImage(
            path=(
                "outputs/documentaries/"
                "mughal-empire/images/scene_001.png"
            ),
            width=768,
            height=432,
            format="png",
            provider="local",
        )
    ]

    animation_instructions = [
        AnimationInstruction(
            scene_number=1,
            prompt="slow cinematic zoom",
            negative_prompt="flickering",
            camera_motion="Zoom In",
        )
    ]

    generated_video = GeneratedVideo(
        path="scene_001.mp4",
        width=512,
        height=512,
        fps=16,
        frame_count=33,
        provider="comfyui",
    )

    research_agent = MagicMock()
    script_agent = MagicMock()
    scene_planner_agent = MagicMock()
    image_prompt_agent = MagicMock()
    image_generation_service = MagicMock()
    image_output_manager = MagicMock()
    animation_agent = MagicMock()
    animation_service = MagicMock()

    def research_run(*args, **kwargs):
        execution_order.append("research")
        return research_result

    def script_run(*args, **kwargs):
        execution_order.append("script")
        return script_result

    def scene_run(*args, **kwargs):
        execution_order.append("scene_planner")
        return scenes

    def image_prompt_run(*args, **kwargs):
        execution_order.append("image_prompt")
        return image_prompts

    def image_generation_run(*args, **kwargs):
        execution_order.append(
            "image_generation"
        )
        return generated_images

    def animation_planning_run(*args, **kwargs):
        execution_order.append(
            "animation_planning"
        )
        return animation_instructions

    def animation_generation_run(*args, **kwargs):
        execution_order.append(
            "animation_generation"
        )
        return generated_video

    research_agent.run.side_effect = research_run
    script_agent.run.side_effect = script_run
    scene_planner_agent.run.side_effect = scene_run
    image_prompt_agent.run.side_effect = image_prompt_run

    image_generation_service.generate_images.side_effect = (
        image_generation_run
    )

    image_output_manager.save_images.return_value = (
        organized_images
    )

    animation_agent.run.side_effect = (
        animation_planning_run
    )

    animation_service.generate_animation.side_effect = (
        animation_generation_run
    )

    graph = create_documentary_graph(
        research_agent=research_agent,
        script_agent=script_agent,
        scene_planner_agent=scene_planner_agent,
        image_prompt_agent=image_prompt_agent,
        animation_agent=animation_agent,
        animation_service=animation_service,
        image_generation_service=image_generation_service,
        image_output_manager=image_output_manager,
    )

    initial_state = {
        "topic": "Mughal Empire",
        "language": "Hindi",
        "duration": 10,
        "style": "historical documentary",
        "research": None,
        "script": None,
        "scenes": [],
        "image_prompts": [],
        "images": [],
        "animation_instructions": [],
        "animations": [],
        "narration": "",
        "audio_path": "",
        "music_path": "",
        "subtitles_path": "",
        "output_video": "",
    }

    result = graph.invoke(initial_state)

    assert execution_order == [
        "research",
        "script",
        "scene_planner",
        "image_prompt",
        "image_generation",
        "animation_planning",
        "animation_generation",
    ]

    assert result["images"] == [
        (
            "outputs/documentaries/"
            "mughal-empire/images/scene_001.png"
        )
    ]

    assert (
        result["animation_instructions"]
        == animation_instructions
    )

    assert result["animations"] == [
        "scene_001.mp4"
    ]

    image_output_manager.save_images.assert_called_once_with(
        images=generated_images,
        topic="Mughal Empire",
    )

    animation_agent.run.assert_called_once_with(
        scenes=scenes,
    )

    animation_service.generate_animation.assert_called_once_with(
        image_path=(
            "outputs/documentaries/"
            "mughal-empire/images/scene_001.png"
        ),
        prompt=animation_instructions[0].prompt,
        negative_prompt=(
            animation_instructions[0].negative_prompt
        ),
        camera_motion=(
            animation_instructions[0].camera_motion
        ),
    )