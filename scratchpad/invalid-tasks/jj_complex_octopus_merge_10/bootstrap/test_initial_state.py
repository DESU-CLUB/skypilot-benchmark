import os
import shutil
import subprocess
import pytest

def test_jj_binary_available():
    assert shutil.which("jj") is not None, "jj binary not found in PATH."

def test_home_directory_exists():
    assert os.path.isdir("/home/user"), "/home/user directory does not exist."
