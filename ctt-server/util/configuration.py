import os

BasePath = '.radonCTT'
CheDirectoryPrefix = '/projects'
DefaultDirectoryPrefix = '/tmp'
RepoDir = 'radon-ctt'
DBFile = 'radon-ctt.db'
SUTFile = 'sut_tosca.yaml'
TIFile = 'ti_tosca.yaml'
DropPolicies = True
FaasScenario = False


def is_che_env():
    ctt_che_env = os.getenv('CTT_CHE_ENV')
    if ctt_che_env and ctt_che_env == "True":
        return True
    else:
        return False


def custom_dir_prefix():
    custom_dir = os.getenv('CTT_BASE_DIR')
    if custom_dir and custom_dir.strip():
        return custom_dir
    else:
        return None


def get_dir_prefix():
    if custom_dir_prefix():
        return custom_dir_prefix()
    elif is_che_env():
        return CheDirectoryPrefix
    else:
        return DefaultDirectoryPrefix


def get_path():
    return os.path.join(get_dir_prefix(), BasePath)
