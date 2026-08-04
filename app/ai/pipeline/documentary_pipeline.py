from typing import Any

from app.ai.graph.documentary_graph import create_documentary_graph
from app.ai.pipeline.exceptions import DocumentaryPipelineError
from app.schemas.documentary import Documentary
from app.schemas.render import RenderConfig
from app.schemas.request import DocumentaryRequest


class DocumentaryPipeline:
    """
    High-level interface for running the AI documentary workflow.
    """

    def __init__(
        self,
        graph: Any | None = None,
    ):
        self.graph = graph or create_documentary_graph()

    def run(
        self,
        request: DocumentaryRequest,
        render: RenderConfig | None = None,
    ) -> Documentary:
        try:
            render_config = render or RenderConfig()

            initial_state = {
                "topic": request.topic,
                "language": request.language,
                "duration": request.duration,
                "style": request.style,
                "research": None,
                "script": None,
                "scenes": [],
                "image_prompts": [],
                "images": [],
                "narration": "",
                "audio_path": "",
                "music_path": "",
                "subtitles_path": "",
                "output_video": "",
            }

            result = self.graph.invoke(initial_state)

            return Documentary(
                request=request,
                research=result["research"],
                script=result["script"],
                scenes=result["scenes"],
                image_prompts=result["image_prompts"],
                render=render_config,
            )

        except Exception as exc:
            raise DocumentaryPipelineError(
                f"Documentary pipeline failed: {exc}"
            ) from exc