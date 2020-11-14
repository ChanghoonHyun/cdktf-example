#!/usr/bin/env python
from constructs import Construct
from cdktf import App, TerraformStack
from imports.aws import AwsProvider
from imports.terraform_aws_modules.vpc.aws import Vpc


class AwsStack(TerraformStack):
    def __init__(self, scope: Construct, ns: str):
        super().__init__(scope, ns)

        AwsProvider(self, 'Aws', region='ap-northeast-2')

        Vpc(self, 'CustomVpc',
            name='custom-vpc',
            cidr='10.10.0.0/16',
            azs=["ap-northeast-1a", "ap-northeast-1c"],
            public_subnets=["10.10.1.0/24", "10.10.2.0/24"]
        )


app = App()
stack = AwsStack(app, "aws")
app.synth()
