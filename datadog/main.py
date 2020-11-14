#!/usr/bin/env python
from constructs import Construct
from cdktf import App, TerraformStack
from imports.datadog import DatadogProvider, Monitor, User, ServiceLevelObjective
import json


def read_config(file='config.json'):
    with open(file, 'r') as ff:
        return json.load(ff)


def read_resource_variables(file):
    with open(f"variables/{file}", 'r') as ff:
        return json.load(ff)


def init_resource(stack, variable, resource_type):
    monitors = read_resource_variables(variable)
    for mm in monitors:
        resource_type(stack, id=mm['name'], **mm)


class DatadogStack(TerraformStack):
    def __init__(self, scope: Construct, ns: str):
        super().__init__(scope, ns)

        config = read_config()

        DatadogProvider(
            self,
            'datadog',
            api_key=config['datadog']['api_key'],
            app_key=config['datadog']['app_key'],
        )
        init_resource(self, 'aws_monitors.json', Monitor)
        init_resource(self, 'apm_monitors.json', Monitor)
        init_resource(self, 'datadog_user.json', User)


app = App()
stack = DatadogStack(app, 'datadog')
stack.add_override('terraform.backend', {
    's3': {
        'bucket': '...',
        'key': 'datadog/cdktf/terraform.state',
        'profile': '...',
        'region': 'ap-northeast-2',
    }
})

app.synth()
