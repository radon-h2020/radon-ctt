import os

BasePath: str = '.radonCTT'
CheDirectoryPrefix: str = '/projects'
DefaultDirectoryPrefix: str = '/tmp'
RepoDir: str = 'radon-ctt'
DBFile: str = 'radon-ctt.db'
SUTFile: str = 'sut_tosca.yaml'
TIFile: str = 'ti_tosca.yaml'
DropPolicies: bool = True
AutoUndeploy: bool = False


def is_che_env() -> bool:
    ctt_che_env = os.getenv('CTT_CHE_ENV')
    if ctt_che_env and ctt_che_env == "True":
        return True
    else:
        return False


def is_test_mode() -> bool:
    """
    Checks whether CTT was set to test mode by setting the environment variable 'CTT_TEST_MODE' to True.
    This prevents all actions with the outside (e.g., deployment, execution) and returns dummy data.
    :return: True if test mode is activated, otherwise False.
    """
    ctt_test_mode = os.getenv('CTT_TEST_MODE')
    if ctt_test_mode and ctt_test_mode == 'True':
        return True
    else:
        return False


def custom_dir_prefix() -> str:
    custom_dir = os.getenv('CTT_BASE_DIR')
    if custom_dir and custom_dir.strip():
        return custom_dir
    else:
        return None


def get_dir_prefix() -> str:
    if custom_dir_prefix():
        return custom_dir_prefix()
    elif is_che_env():
        return CheDirectoryPrefix
    else:
        return DefaultDirectoryPrefix


def get_path():
    return os.path.join(get_dir_prefix(), BasePath)
