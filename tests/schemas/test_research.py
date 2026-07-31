from app.schemas.research import (
    ResearchResult,
    TimelineEvent,
)


def test_research_schema():

    research = ResearchResult(

        topic="Mughal Empire",

        summary="History",

        timeline=[
            TimelineEvent(
                year="1526",
                title="Battle of Panipat",
                description="Babur defeated Ibrahim Lodi."
            )
        ],

        characters=[],

        sources=[]
    )

    assert research.topic == "Mughal Empire"

    assert research.timeline[0].year == "1526"