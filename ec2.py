#!/usr/bin/env python3
import logging
import boto3


class EC2Actions(object):
    def __init__(self, clients):
        self.clients = clients

    def stop_instances(self, instance_ids):
        self.instance_ids = instance_ids
        print(self.instance_ids)
        try:
            self.response = self.clients.ec2r.instances.filter(InstanceIds=self.instance_ids).stop()
        except Exception as e:
            logging.exception(e)
            pass
        try:
            self.waiter = self.clients.ec2.get_waiter('instance_stopped')
            self.waiter.wait(InstanceIds=self.instance_ids, WaiterConfig={'Delay': 15})
        except Exception as e:
            logging.warn(e)

    def start_instances(self, instance_ids):
        self.instance_ids = instance_ids
        print(self.instance_ids)
        try:
            self.response = self.clients.ec2r.instances.filter(InstanceIds=self.instance_ids).start()
        except Exception as e:
            logging.exception(e)
        try:
            self.waiter = self.clients.ec2.get_waiter('instance_running')
            self.waiter.wait(InstanceIds=self.instance_ids, WaiterConfig={'Delay': 15})
        except Exception as e:
            logging.warn(e)

    def get_privateIps(self, instance_ids):
        privateIps=[]
        self.instance_ids=instance_ids
        try:
            self.response=self.clients.ec2.describe_instances(InstanceIds=self.instance_ids)
            for instances in self.response['Reservations']:
                for privateip in instances['Instances']:
                    privateIps.append(privateip['PrivateIpAddress'])
            return(privateIps)
        except Exception as e:
            logging.exception(e)