import pytest

from app.music.music_manager import MusicManager


def test_prepare_background_music(
    tmp_path,
):
    source = tmp_path / "cinematic.mp3"

    source.write_bytes(
        b"fake audio data"
    )

    output_root = tmp_path / "outputs"

    manager = MusicManager(
        output_root=output_root,
    )

    result = manager.prepare(
        source_path=source,
        topic="Mughal Empire",
    )

    expected = (
        output_root
        / "mughal-empire"
        / "music"
        / "background.mp3"
    )

    assert result == str(expected)
    assert expected.is_file()

    assert (
        expected.read_bytes()
        == b"fake audio data"
    )


def test_missing_music_file(
    tmp_path,
):
    manager = MusicManager(
        output_root=tmp_path,
    )

    with pytest.raises(
        FileNotFoundError,
        match="Music file does not exist",
    ):
        manager.prepare(
            source_path=(
                tmp_path / "missing.mp3"
            ),
            topic="Mughal Empire",
        )


def test_unsupported_music_format(
    tmp_path,
):
    source = tmp_path / "music.txt"
    source.write_text("invalid")

    manager = MusicManager(
        output_root=tmp_path,
    )

    with pytest.raises(
        ValueError,
        match="Unsupported music format",
    ):
        manager.prepare(
            source_path=source,
            topic="Mughal Empire",
        )