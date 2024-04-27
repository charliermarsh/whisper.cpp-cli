from pathlib import Path
from typing import Any

from hatchling.builders.hooks.plugin.interface import BuildHookInterface

import shutil
import urllib.request
import zipfile
import os

import subprocess

WHISPER_CPP_VERSION = '1.5.5'
WHISPER_CPP_ZIP_URL = f"https://github.com/ggerganov/whisper.cpp/archive/refs/tags/v{WHISPER_CPP_VERSION}.zip"
WHISPER_DIR = f'whisper.cpp-{WHISPER_CPP_VERSION}'
WHISPER_BINARY = f"{WHISPER_DIR}/main"


class WhisperCppBuildHook(BuildHookInterface):
    PLUGIN_NAME = "whisper-cpp"

    def initialize(self, version: str, build_data: dict[str, Any]) -> None:
        if not os.path.exists(WHISPER_BINARY):
            def download_and_unzip(url, extract_to='.'):
                """
                Downloads a ZIP file from a URL and unzips it into the given directory.

                Args:
                url (str): The URL of the zip file to download.
                extract_to (str): The directory to extract the files into.
                """
                # Download the file from `url` and save it locally under `file_name`
                file_name = url.split('/')[-1]
                urllib.request.urlretrieve(url, file_name)

                # Unzip the file
                with zipfile.ZipFile(file_name, 'r') as zip_ref:
                    zip_ref.extractall(extract_to)

                # Clean up the downloaded zip file
                os.remove(file_name)

            # Remove the existing whisper-cpp directory, if it exists
            shutil.rmtree(WHISPER_DIR, ignore_errors=True)

            # Download the latest whisper-cpp release from GitHub.
            download_and_unzip(WHISPER_CPP_ZIP_URL, extract_to='.')

            # Run make to build the whisper-cpp library.
            subprocess.check_call(['make'], cwd=WHISPER_DIR)

        build_data['shared_scripts'] = {
            WHISPER_BINARY: "whisper-cpp"
        }
