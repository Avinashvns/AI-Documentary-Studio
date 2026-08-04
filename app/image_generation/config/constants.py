from enum import StrEnum


class ImageProviderType(StrEnum):
    LOCAL = "local"
    CLOUD = "cloud"


class ImageFormat(StrEnum):
    PNG = "png"
    JPEG = "jpeg"
    WEBP = "webp"