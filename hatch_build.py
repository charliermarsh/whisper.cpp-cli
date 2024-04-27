import os
import shutil
import subprocess
import urllib.request
import zipfile
from typing import Any

from hatchling.builders.hooks.plugin.interface import BuildHookInterface

EXE = ".exe" if os.name == "nt" else ""

WHISPER_CPP_VERSION = "1.5.5"
WHISPER_CPP_ZIP_URL = (
    f"https://github.com/ggerganov/whisper.cpp/archive/refs/tags/v{WHISPER_CPP_VERSION}.zip"
)
WHISPER_DIR = f"whisper.cpp-{WHISPER_CPP_VERSION}"


class WhisperCppBuildHook(BuildHookInterface):
    PLUGIN_NAME = "whisper-cpp"

    def initialize(self, version: str, build_data: dict[str, Any]) -> None:
        if not os.path.exists(f"{WHISPER_DIR}/main{EXE}"):

            def download_and_unzip(url, extract_to="."):
                """
                Downloads a ZIP file from a URL and unzips it into the given directory.

                Args:
                url (str): The URL of the zip file to download.
                extract_to (str): The directory to extract the files into.
                """
                # Download the file from `url` and save it locally under `file_name`
                file_name = url.split("/")[-1]
                urllib.request.urlretrieve(url, file_name)

                # Unzip the file
                with zipfile.ZipFile(file_name, "r") as zip_ref:
                    zip_ref.extractall(extract_to)

                # Clean up the downloaded zip file
                os.remove(file_name)

            # Remove the existing whisper-cpp directory, if it exists
            shutil.rmtree(WHISPER_DIR, ignore_errors=True)

            # Download the latest whisper-cpp release from GitHub.
            download_and_unzip(WHISPER_CPP_ZIP_URL, extract_to=".")

            # Run make to build the whisper-cpp library.
            subprocess.check_call(["make"], cwd=WHISPER_DIR)

        build_data["shared_scripts"] = {f"{WHISPER_DIR}/main{EXE}": f"whisper-cpp{EXE}"}
        build_data["tag"] = self._infer_tag()

    def _infer_tag(self) -> str:
        """Infer the appropriate wheel tag.

        Based on Hatchling's own `get_best_matching_tag` as of v1.24.2, with the
        primary difference being that the plugin generates an ABI and version-agnostic
        wheel tag, modifying _only_ the platform tag to include the architecture.
        """
        import sys

        from packaging.tags import sys_tags

        tag = next(sys_tags())
        tag_platform = tag.platform

        # On macOS, set the version based on `MACOSX_DEPLOYMENT_TARGET`.
        if sys.platform == "darwin":
            macosx_deployment_target = os.environ.get("MACOSX_DEPLOYMENT_TARGET")
            if macosx_deployment_target:
                # Extract the architecture from, e.g., `macosx_14_0_arm64`.
                if tag_platform.endswith("_arm64"):
                    tag_arch = "arm64"
                elif tag_platform.endswith("_x86_64"):
                    tag_arch = "x86_64"
                else:
                    raise ValueError(f"Unknown macOS arch: {tag_platform}")

                # Reconstruct the platform tag with the architecture.
                tag_platform = f"macosx_{macosx_deployment_target.replace('.', '_')}_{tag_arch}"

        return f"py3-none-{tag_platform}"
