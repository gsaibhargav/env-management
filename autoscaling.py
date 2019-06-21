#!/usr/bin/env python3
import logging


class ASGActions(object):
    def __init__(self, clients):
        self.clients = clients
        self.paginator = self.clients.autoscaling.get_paginator('describe_auto_scaling_groups')

    def filter_asg_byname(self, names):
        self.names = names
        self.asglist = []
        self.page_iterator = self.paginator.paginate()
        for page in self.page_iterator:
            for group in page['AutoScalingGroups'][:]:
                for name in self.names[:]:
                    if (name.strip() in group['AutoScalingGroupName']):
                        self.asglist.append(group['AutoScalingGroupName'])
                    else:
                        continue
        return self.asglist

    def instances_by_asg(self, autoscalinggroups, state):
        self.idlist = []
        self.autoscalinggroups = autoscalinggroups
        for self.asg in self.autoscalinggroups[:]:
            self.page_iterator = self.paginator.paginate(AutoScalingGroupNames=[self.asg])
            for page in self.page_iterator:
                for group in page['AutoScalingGroups']:
                    for instance in group['Instances']:
                        if instance['LifecycleState'] == state:
                            self.idlist.append(instance['InstanceId'])
        return self.idlist

    def set_desired_capacity(self, asgname, capacity):
        response = self.clients.autoscaling.set_desired_capacity(
            AutoScalingGroupName=asgname,
            DesiredCapacity=capacity
        )
        logging.info(response)

    def suspend_termination_process(self, autoscalinggroups):
        self.autoscalinggroups = autoscalinggroups
        for self.asgname in self.autoscalinggroups:
            self.response = self.clients.autoscaling.suspend_processes(
                AutoScalingGroupName=self.asgname,
                ScalingProcesses=['Terminate']
            )
            logging.info('Suspended termination process for %s', self.asgname)

    def suspend_healthcheck_process(self, autoscalinggroups):
        self.autoscalinggroups = autoscalinggroups
        for self.asgname in self.autoscalinggroups:
            self.response = self.clients.autoscaling.suspend_processes(
                AutoScalingGroupName=self.asgname,
                ScalingProcesses=['HealthCheck']
            )
            logging.info('Suspended healthcheck process for %s', self.asgname)

    def resume_termination_process(self, autoscalinggroups):
        self.autoscalinggroups = autoscalinggroups
        for self.asgname in self.autoscalinggroups:
            self.response = self.clients.autoscaling.resume_processes(
                AutoScalingGroupName=self.asgname,
                ScalingProcesses=['Terminate']
            )
            logging.info('Resumed termination process for %s',self.asgname)

    def resume_healthcheck_process(self, autoscalinggroups):
        self.autoscalinggroups = autoscalinggroups
        for self.asgname in self.autoscalinggroups:
            self.response = self.clients.autoscaling.resume_processes(
                AutoScalingGroupName=self.asgname,
                ScalingProcesses=['HealthCheck']
            )
            logging.info('Resumed healthcheck process for %s',self.asgname)
