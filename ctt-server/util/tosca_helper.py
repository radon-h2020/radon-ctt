import os
import shutil
import tempfile
import yaml
import zipfile


def tosca_to_dict(tosca_file):
    if os.path.isfile(tosca_file):
        with open(tosca_file, 'r') as tosca_yaml:
            tosca_dict = yaml.full_load(tosca_yaml)
            return tosca_dict


class Csar:

    def __init__(self, csar_file):
        self.__csar_file = csar_file
        self.__tosca_entry_point = None

        if os.path.isfile(csar_file):
            self.__temp_dir = tempfile.mkdtemp()
            zipfile.ZipFile(csar_file).extractall(self.__temp_dir)
        else:
            raise FileNotFoundError(f'CSAR file {csar_file} could not be found.')

    def __del__(self):
        shutil.__cleanup()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__cleanup()

    def __cleanup(self):
        shutil.rmtree(self.__temp_dir, ignore_errors=True)

    @property
    def tosca_entry_point(self, tosca_meta_file='TOSCA-Metadata/TOSCA.meta'):
        if not self.__tosca_entry_point:
            tosca_meta_file_path = os.path.join(self.__temp_dir, tosca_meta_file)
            if os.path.isfile(tosca_meta_file_path):
                with open(tosca_meta_file_path, 'r') as tosca_meta:
                    for line in tosca_meta:
                        if line.startswith('Entry-Definitions: '):
                            self.__tosca_entry_point = line.strip().split(' ')[1]
            if not self.__tosca_entry_point:
                raise Exception('Entry definition could not be found.')
        return self.__tosca_entry_point

    def file_as_dict(self, tosca_file):
        tosca_file_path = os.path.join(self.__temp_dir, tosca_file)
        if os.path.isfile(tosca_file_path):
            with open(tosca_file_path, 'r') as tosca_yaml:
                tosca_dict = yaml.full_load(tosca_yaml)
                return tosca_dict

    def file_ns_name(self, tosca_file):
        tosca_file_metadata = self.file_as_dict(tosca_file)['metadata']
        return f"{tosca_file_metadata['targetNamespace']}.{tosca_file_metadata['name']}"

    def full_file_path(self, file_path):
        full_file_path = os.path.join(self.__temp_dir, file_path)
        if os.path.isfile(full_file_path):
            return full_file_path
        else:
            raise FileNotFoundError(f'The file \'{file_path}\' does not exist in this CSAR.')
