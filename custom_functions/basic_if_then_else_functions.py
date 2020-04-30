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
    if_conditional_expression: df['temp'] > 50
    then_true_value : Offline
    else_false_value : Online
    """

    def __init__(self, input_items, if_conditional_expression, then_true_value, else_false_value, output_item=None):
        super().__init__()

        self.input_items = input_items
        self.if_conditional_expression = self.parse_expression(if_conditional_expression)
        self.then_true_value = then_true_value
        self.else_false_value = else_false_value
        if output_item is None:
            self.output_item = 'output_item'
        else:
            self.output_item = output_item

    def execute(self, df):
        df[self.output_item] = np.where(eval(self.if_conditional_expression), self.then_true_value, self.else_false_value)
        return df

    @classmethod
    def build_ui(cls):
        # define arguments that behave as function inputs
        inputs = []
        inputs.append(UIMultiItem('input_items', description="data items that are used in conditional_expression"))
        inputs.append(UIExpression(name='if_conditional_expression',
                                   description="expression that returns a specified value, eg. if df['temp']>50 then Offline else Online"))
        inputs.append(UISingle(name='then_true_value', description="value when true, eg. Offline"))
        inputs.append(UISingle(name='else_false_value', description='value when false, eg. Online '))
        # define arguments that behave as function outputs
        outputs = []
        outputs.append(UIFunctionOutSingle(name='output_item', description='function output'))

        return (inputs, outputs)
