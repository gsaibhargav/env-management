#!/usr/bin/env python3
import boto3


class Clients(object):
    def __init__(self, **kwargs):
        if ("aws_region" in kwargs and kwargs['aws_region'] is not None):
            self.region = kwargs['aws_region']
        if ('aws_access_key_id' in kwargs and 'aws_secret_access_key' in kwargs and kwargs[
            'aws_access_key_id'] is not None and kwargs['aws_secret_access_key'] is not None):
            self.aws_access_key_id = kwargs['aws_access_key_id']
            self.aws_secret_access_key = kwargs['aws_secret_access_key']
            self.session = boto3.session.Session(
                aws_access_key_id=self.aws_access_key_id,
                aws_secret_access_key=self.aws_secret_access_key
            )
        elif ('aws_profile' in kwargs and kwargs['aws_profile'] is not None):
            self.profile_name = kwargs['aws_profile']
            session = boto3.Session(profile_name=self.profile_name, region_name=self.region)
        else:
            session = boto3.session.Session()

        self.cloudformation = session.client('cloudformation', region_name=self.region)
        self.autoscaling = session.client('autoscaling', region_name=self.region)
        self.ec2 = session.client('ec2', region_name=self.region)
        self.ec2r = session.resource('ec2', region_name=self.region)
        self.ecs = session.client('ecs', region_name=self.region)
        self.elb = session.client('elb', region_name=self.region)
