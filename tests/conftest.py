import sys
import os
import pytest
import shutil

# Add the parent directory to the module search path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# This function is used to remove all temp files once pytest is finished.
# It may be worth commenting out if debugging failures.
@pytest.fixture(scope='session', autouse=True)
def cleanup_temp_directories(request, tmp_path_factory):
    # Get the temporary directory path
    temp_dir = tmp_path_factory.getbasetemp().parent

    yield

    # Perform cleanup after all tests have finished
    shutil.rmtree(temp_dir)