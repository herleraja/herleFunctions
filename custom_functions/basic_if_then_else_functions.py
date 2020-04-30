import inspect
import logging
import datetime as dt
import math
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

PACKAGE_URL = 'git+https://github.com/herleraja/herleFunctions.git@'


class BasicIfThenElse(BaseTransformer):
    """
    Set the value of the output_item based on a conditional expression.
    When the conditional expression returns a True value, return the true_value.

    Example:
    conditional_expression: df['temp'] > 50
    true value: Offline
    false value: Online
    """

    def __init__(self, input_items, conditional_expression, true_value, false_value, output_item=None):
        super().__init__()

        self.input_items = input_items
        self.conditional_expression = self.parse_expression(conditional_expression)
        self.true_value = true_value
        self.false_value = false_value
        if output_item is None:
            self.output_item = 'output_item'
        else:
            self.output_item = output_item

    def execute(self, df):
        df[self.output_item] = np.where(eval(self.conditional_expression), self.true_value, self.false_value)
        return df

    @classmethod
    def build_ui(cls):
        # define arguments that behave as function inputs
        inputs = []
        inputs.append(UIMultiItem('input_items', description="data items that are used in conditional_expression"))
        inputs.append(UIExpression(name='conditional_expression',
                                   description="expression that returns a specified value, eg. if df['temp']>50 then Offline else Online"))
        inputs.append(UISingle(name='true_value', description="value when true, eg. Offline"))
        inputs.append(UISingle(name='false_value', description='value when false, eg. Online '))
        # define arguments that behave as function outputs
        outputs = []
        outputs.append(UIFunctionOutSingle(name='output_item', description='function output'))

        return (inputs, outputs)
