from app.schemas.documentary import Documentary
from app.schemas.request import DocumentaryRequest
from app.schemas.render import RenderConfig


def test_documentary_schema():
    documentary = Documentary(
        request=DocumentaryRequest(topic="Mughal Empire"),
        render=RenderConfig(),
    )

    assert documentary.request.topic == "Mughal Empire"
    assert documentary.render.resolution == "2K"
    assert documentary.scenes == []
    assert documentary.image_prompts == []