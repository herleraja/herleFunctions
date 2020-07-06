import inspect
import logging
import datetime as dt
import math
import numpy as np
import json
from abc import ABC

from sqlalchemy.sql.sqltypes import TIMESTAMP, VARCHAR
import numpy as np
import pandas as pd

from iotfunctions.base import BaseTransformer
from iotfunctions.ui import (UISingle, UIMultiItem, UIFunctionOutSingle, UISingleItem, UIFunctionOutMulti, UIMulti,
                             UIExpression, UIText, UIParameters)

logger = logging.getLogger(__name__)

# Specify the URL to your package here.
# This URL must be accessible via pip install

PACKAGE_URL = 'git+https://github.com/herleraja/herleFunctions.git'


class PopulatePropertyFromDimensionAPI(BaseTransformer):
    """
    Get the dimension of other entity type and populate a property based on the conditional property.
    """

    def __init__(self, entity_type_name, comparision_property, insertion_property, output_item=None):
        super().__init__()

        self.entity_type_name = entity_type_name
        self.comparision_property = comparision_property
        self.insertion_property = insertion_property
        if output_item is None:
            self.output_item = 'output_item'
        else:
            self.output_item = output_item

    def execute(self, df):

        entity_type = self.get_entity_type()
        db = entity_type.db
        credentials = db.credentials
        url = 'https://%s/api/master/v1/%s/entityType/%s/dimensional' % (
            credentials['as']['host'], entity_type.tenant_id, self.entity_type_name)
        headers = {'Content-Type': "application/json", 'X-api-key': credentials['as']['api_key'],
                   'X-api-token': credentials['as']['api_token'], 'Cache-Control': "no-cache", }

        response = db.http.request('GET', url, headers=headers)
        response_data = json.loads(response.data)

        # Dirty trick
        df[self.comparision_property] = np.random.choice(a=['1', '2', ''], size=len(df.index))

        df[self.output_item] = None

        for dimension in response_data:
            logging_output = 'comparision_property_value = %s , insertion_property_value = %s ' % (
                dimension[self.comparision_property], dimension[self.insertion_property])
            logger.info(logging_output)

            if len(dimension[self.comparision_property]) > 0:
                logger.info(df[df[self.comparision_property] == dimension[self.comparision_property]])
                df[self.output_item] = np.where(df[self.comparision_property] == dimension[self.comparision_property],
                                                df[self.insertion_property], df[self.output_item])

        return df

    @classmethod
    def build_ui(cls):
        # define arguments that behave as function inputs
        inputs = []
        inputs.append(UISingle(name='entity_type_name', description="Name of the entity type"))
        inputs.append(UISingleItem(name='comparision_property',
                                   description='Name of a property in dimension api on which comparison is done'))
        inputs.append(UISingle(name='insertion_property',
                               description='Name of a property in dimension api which will be inserted into output on successful comparison is done'))
        # define arguments that behave as function outputs
        outputs = []
        outputs.append(UIFunctionOutSingle(name='output_item', description='function output'))

        return (inputs, outputs)
