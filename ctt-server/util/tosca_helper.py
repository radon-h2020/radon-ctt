import glob
import os
import shutil
import tempfile
import yaml
import zipfile

from flask import current_app


class Csar:
    """

    """

    def __init__(self, csar_file, extract_dir=None, keep=False):
        """
        Constructor that already extracts the CSAR file to later operate on its content.
        :param csar_file:
        The CSAR file to operate on.
        :param extract_dir:
        Directory the CSAR file is supposed to be extracted to.
        If no directory is given, a temporary directory will be created and used.
        :param keep:
        Whether the extracted directory should be deleted when the class instance is destroyed.
        Default is False.
        """
        self.__csar_file = csar_file
        self.__tosca_entry_point = None
        self.__extracted = False
        self.__extract_dir = extract_dir
        self.__keep = keep

        if not os.path.isfile(csar_file):
            raise FileNotFoundError(f'CSAR file {csar_file} could not be found.')

        self.__extract()

    def __del__(self):
        self.__cleanup()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__cleanup()

    def __cleanup(self):
        if not self.__keep and self.__extract_dir:
            shutil.rmtree(self.__extract_dir, ignore_errors=True)

    @property
    def tosca_entry_point(self, tosca_meta_file='TOSCA-Metadata/TOSCA.meta'):
        if not self.__tosca_entry_point:
            tosca_meta_file_path = os.path.join(self.__extract_dir, tosca_meta_file)
            if os.path.isfile(tosca_meta_file_path):
                with open(tosca_meta_file_path, 'r') as tosca_meta:
                    for line in tosca_meta:
                        if line.startswith('Entry-Definitions: '):
                            self.__tosca_entry_point = line.strip().split(' ')[1]
            if not self.__tosca_entry_point:
                raise Exception('Entry definition could not be found.')
        return self.__tosca_entry_point

    @property
    def extract_dir(self):
        return self.__extract_dir

    def file_as_dict(self, tosca_file):
        tosca_file_path = os.path.join(self.__extract_dir, tosca_file)
        if os.path.isfile(tosca_file_path):
            with open(tosca_file_path, 'r') as tosca_yaml:
                tosca_dict = yaml.full_load(tosca_yaml)
                return tosca_dict

    def file_ns_name(self, tosca_file):
        tosca_file_metadata = self.file_as_dict(tosca_file)['metadata']
        return f"{tosca_file_metadata['targetNamespace']}.{tosca_file_metadata['name']}"

    def full_file_path(self, file_path):
        full_file_path = os.path.join(self.__extract_dir, file_path)
        if os.path.isfile(full_file_path):
            return full_file_path
        else:
            raise FileNotFoundError(f'The file \'{file_path}\' does not exist in this CSAR.')

    def __extract(self):
        if not self.__extracted:
            if not self.__extract_dir:
                self.__extract_dir = tempfile.mkdtemp()

            if not os.path.isdir(self.__extract_dir):
                os.makedirs(self.__extract_dir)

            zipfile.ZipFile(self.__csar_file).extractall(self.__extract_dir)
            self.__extracted = True
        else:
            current_app.logger.info(f"File has already been extracted to '{self.__extract_dir}'. Skipping extraction.")

    def drop_policies(self):
        Csar.drop_policies_in_dir(self.__extract_dir)

    @staticmethod
    def drop_policies_in_dir(directory):
        definitions_folder = os.path.join(directory, "_definitions")
        if os.path.isdir(directory) and os.path.isdir(definitions_folder):
            file_list = glob.glob(definitions_folder + os.sep + "*.tosca")
            if len(file_list) > 0:
                for file in file_list:
                    tosca_yaml = Csar.tosca_to_dict(file)
                    if 'policy_types' in tosca_yaml:
                        del tosca_yaml['policy_types']
                    if 'topology_template' in tosca_yaml and 'policies' in tosca_yaml['topology_template']:
                        del tosca_yaml['topology_template']['policies']

                    with open(file, 'w') as tosca_file_out:
                        yaml.dump(tosca_yaml, tosca_file_out)
                current_app.logger.info(f"Processed {len(file_list)} TOSCA files with 'drop_policies'.")
            else:
                # traceback.print_stack(..)
                current_app.logger.info("No tosca-files in", definitions_folder)

    @staticmethod
    def tosca_to_dict(tosca_file):
        if os.path.isfile(tosca_file):
            with open(tosca_file, 'r') as tosca_yaml:
                tosca_dict = yaml.full_load(tosca_yaml)
                return tosca_dict
