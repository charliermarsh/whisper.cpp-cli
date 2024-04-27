import shutil
import urllib.request
import zipfile
import os

from setuptools import setup, find_packages
import subprocess



WHISPER_CPP_VERSION = '1.5.5'

WHISPER_CPP_ZIP_URL = f"https://github.com/ggerganov/whisper.cpp/archive/refs/tags/v{WHISPER_CPP_VERSION}.zip"

WHISPER_DIR = f'whisper.cpp-{WHISPER_CPP_VERSION}'

WHISPER_BINARY = f'bin/whisper-cpp'

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
    shutil.rmtree('bin', ignore_errors=True)

    # Download the latest whisper-cpp release from GitHub.
    download_and_unzip(WHISPER_CPP_ZIP_URL, extract_to='.')

    # Run make to build the whisper-cpp library.
    subprocess.check_call(['make'], cwd=WHISPER_DIR)

    # Rename the built binary.
    os.makedirs('bin', exist_ok=True)

    # Copy the built binary to the `bin` directory.
    shutil.copy2(f'{WHISPER_DIR}/main', WHISPER_BINARY)


# Include the `whisper-cpp` binary in the package.
setup(
    name='whisper-cpp',
    version='0.0.1',
    packages=find_packages(),
    package_data={"whisper-cpp": [os.path.join("bin", "*")]},
    include_package_data=True,
    install_requires=[],
)
