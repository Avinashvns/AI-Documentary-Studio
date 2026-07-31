from enum import Enum


class AgentType(str, Enum):
    MASTER = "master"
    RESEARCH = "research"
    SCRIPT = "script"
    SCENE_PLANNER = "scene_planner"
    IMAGE_PROMPT = "image_prompt"
    IMAGE_GENERATOR = "image_generator"
    ANIMATION = "animation"
    VOICE = "voice"
    MUSIC = "music"
    EXPORT = "export"


class VideoStyle(str, Enum):
    CINEMATIC = "cinematic"
    DOCUMENTARY = "documentary"


class Language(str, Enum):
    HINDI = "Hindi"
    ENGLISH = "English"