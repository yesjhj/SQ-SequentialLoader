import os, shutil
import folder_paths
from .SequentialImageLoader import LoadImagesSequentially


NODE_CLASS_MAPPINGS = {
    "Sequential Image Loader": LoadImagesSequentially,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Sequential Image Loader": "SQ-SequentialLoader",
}

WEB_DIRECTORY = "./js"
__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS', "WEB_DIRECTORY"]


# keep this for backward compatibility for a while..
module_js_directory = os.path.join(os.path.dirname(os.path.realpath(__file__)), "js")
application_root_directory = os.path.dirname(folder_paths.__file__)
application_web_extensions_directory = os.path.join(application_root_directory, "web", "extensions", "SQ-ImageLoader")

if os.path.exists(application_web_extensions_directory):
    shutil.rmtree(application_web_extensions_directory)
shutil.copytree(module_js_directory, application_web_extensions_directory, dirs_exist_ok=True)
