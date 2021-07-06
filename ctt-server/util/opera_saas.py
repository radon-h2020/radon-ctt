import base64
import json
import os
import subprocess
import sys
import requests

from requests.cookies import RequestsCookieJar

if sys.version_info < (3, 10):
    from util.cookiejar import MozillaCookieJar
else:
    from http.cookiejar import MozillaCookieJar

auth_script_path: str = './opera-saas-auth.sh'
api_url_default: str = 'https://xopera-radon.xlab.si/api'
auth_base_url_default: str = 'https://openid-radon.xlab.si'
default_headers: dict = {'Accept': 'application/json', 'User-Agent': 'RADON CTT Server',
                         'Cache-Control': 'no-cache', 'Content-Type': 'application/json'}


class OperaSaas:
    def __init__(self, username: str, password: str,
                 api_url: str = api_url_default,
                 auth_base_url: str = auth_base_url_default):
        self.__api_url: str = api_url
        self.__auth_base_url: str = auth_base_url
        self.__username: str = username
        self.__password: str = password
        self.__cookie_jar: RequestsCookieJar = RequestsCookieJar()
        self.__requests_session = requests.Session()
        if self.__authenticate():
            self.__auth_status = self.__check_status()
        else:
            raise Exception("Authentication with Opera SaaS failed.")

    def __authenticate(self) -> bool:
        proc_result = subprocess.run([auth_script_path,
                                      self.__username,
                                      self.__password,
                                      self.__api_url,
                                      self.__auth_base_url],
                                     capture_output=True)
        if proc_result.returncode == 0:
            cookie_jar_path = proc_result.stdout.decode('UTF-8').strip()
            cj = MozillaCookieJar("/tmp/cookiejar_ctt_int.txt")
            cj.load(cookie_jar_path, ignore_discard=True, ignore_expires=True)
            for cookie in cj:
                self.__cookie_jar.set_cookie(cookie)
            self.__requests_session.cookies = self.__cookie_jar
            return True
        return False

    def de_authenticate(self) -> None:
        self.__requests_session.cookies.clear()
        self.__requests_session.close()

    def __check_status(self):
        response = self.__requests_session.get(url=f'{self.__api_url}/auth/status',
                                               headers=default_headers,
                                               allow_redirects=True)
        if response.status_code == 200:
            return response.json()
        else:
            return None

    @property
    def is_logged_in(self) -> bool:
        return self.__auth_status['isLoggedIn']

    def project_create(self, workspace_id: int, csar_file: str, name: str):
        if os.path.isfile(csar_file):
            with open(csar_file, 'rb') as csar_binary:
                csar_binary_content = csar_binary.read()
                csar_base64 = base64.b64encode(csar_binary_content)
                csar_base64_utf8 = csar_base64.decode('utf-8')
                param = {'csar': f'{csar_base64_utf8}', 'name': f'{name}'}

            response = self.__requests_session.post(url=f'{self.__api_url}/workspace/{workspace_id}/project',
                                                    headers=default_headers,
                                                    data=json.dumps(param))
            if response.status_code == 200:
                return response.json()
        return None

    def project_status(self, workspace_id: int, project_id: int):
        response = self.__requests_session.get(url=f'{self.__api_url}/workspace/{workspace_id}'
                                                   f'/project/{project_id}/creationStatus',
                                               headers=default_headers)
        if response.status_code == 200:
            return response.json()
        return None

    def workspaces_get(self):
        response = self.__requests_session.get(url=f'{self.__api_url}/workspace',
                                               headers=default_headers)
        if response.status_code == 200:
            return response.json()
        return None

    def workspace_get(self, workspace_id: int):
        response = self.__requests_session.get(url=f'{self.__api_url}/workspace/{workspace_id}',
                                               headers=default_headers)
        if response.status_code == 200:
            return response.json()
        return None

    def projects_get(self, workspace_id: int):
        response = self.__requests_session.get(url=f'{self.__api_url}/workspace/{workspace_id}/project',
                                               headers=default_headers)
        if response.status_code == 200:
            return response.json()
        return None

    def project_get(self, workspace_id: int, project_id):
        response = self.__requests_session.get(url=f'{self.__api_url}/workspace/{workspace_id}/project/{project_id}',
                                               headers=default_headers)
        if response.status_code == 200:
            return response.json()
        return None

    def project_delete(self, workspace_id: int, project_id):
        response = self.__requests_session.delete(url=f'{self.__api_url}/workspace/{workspace_id}/project/{project_id}',
                                                  headers=default_headers)
        if response.status_code == 200:
            return True
        return None

    def validate_post(self, workspace_id: int, project_id: int):
        param = {}
        response = self.__requests_session.post(url=f'{self.__api_url}/workspace/{workspace_id}'
                                                    f'/project/{project_id}/validate',
                                                data=json.dumps(param),
                                                headers=default_headers)
        if response.status_code == 200:
            return response.json()
        return False

    def deploy_post(self, workspace_id: int, project_id: int, inputs_file=None):
        param = {}
        if inputs_file and os.path.isfile(inputs_file):
            with open(inputs_file, 'r') as inputs:
                param = json.loads(inputs)
        payload = json.dumps(param)
        response = self.__requests_session.post(url=f'{self.__api_url}/workspace/{workspace_id}'
                                                    f'/project/{project_id}/deploy',
                                                data=payload,
                                                headers=default_headers)
        if response.status_code == 200:
            return response.json()
        return None

    def deploy_status_get(self):
        return None

    def undeploy_post(self, workspace_id: int, project_id: int):
        response = self.__requests_session.post(url=f'{self.__api_url}/workspace/{workspace_id}'
                                                    f'/project/{project_id}/undeploy',
                                                headers=default_headers)
        if response.status_code == 200:
            return response.json()
        return False
