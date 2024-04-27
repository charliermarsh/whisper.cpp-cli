import os
import sys
import sysconfig


def find_whisper_bin() -> str:
    """Return the whisper binary path."""

    whisper_exe = "whisper-cpp" + sysconfig.get_config_var("EXE")

    path = os.path.join(sysconfig.get_path("scripts"), whisper_exe)
    if os.path.isfile(path):
        return path

    if sys.version_info >= (3, 10):
        user_scheme = sysconfig.get_preferred_scheme("user")
    elif os.name == "nt":
        user_scheme = "nt_user"
    elif sys.platform == "darwin" and sys._framework:
        user_scheme = "osx_framework_user"
    else:
        user_scheme = "posix_user"

    path = os.path.join(sysconfig.get_path("scripts", scheme=user_scheme), whisper_exe)
    if os.path.isfile(path):
        return path

    raise FileNotFoundError(path)


if __name__ == "__main__":
    whisper = os.fsdecode(find_whisper_bin())
    if sys.platform == "win32":
        import subprocess

        completed_process = subprocess.run([whisper, *sys.argv[1:]])
        sys.exit(completed_process.returncode)
    else:
        os.execvp(whisper, [whisper, *sys.argv[1:]])
