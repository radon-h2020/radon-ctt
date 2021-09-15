# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from openapi_server.models.base_model_ import Model
from openapi_server import util


class Workflow(Model):
    def __init__(self, workflow_data=None):  # noqa: E501

        self.openapi_types = {
            'workflow_data': str,
        }

        self.attribute_map = {
            'workflow_data': 'workflow_data',
        }

        self._workflow_data = workflow_data

    @classmethod
    def from_dict(cls, dikt) -> 'Workflow':
        return util.deserialize_model(dikt, cls)

    @property
    def workflow_data(self):
        return self._workflow_data

    @workflow_data.setter
    def workflow_data(self, workflow_data):
          self._workflow_data = workflow_data
