#!/usr/bin/env python3

import os
import boto3

env = os.environ.get('ENVIRONMENT')
if env == 'dev':
    REGION = 'eu-central-1'
elif env == 'prod':
    REGION = 'us-east-1'
else:
    raise AttributeError("Can't find ENVIRONMENT")

# 52.29.216.16
ec2 = boto3.resource('ec2', region_name=REGION)
# list(ec2.instances.all())


def get_name(instance, field='Name', key_name='Key', value_name='Value'):
    for tag in instance.tags:
        if tag[key_name] == field:
            return tag[value_name]
    return


def get_pushpin(ec2, key='Name', status='running', instance_tag='pushpin'):
    for instance in ec2.instances.all():
        name = get_name(instance)
        if instance_tag in name:
            if instance.state[key] == status:
                print(name, instance.id)
                return instance
    return


pushpin = get_pushpin(ec2)
pushpin.id

# verify when the current is alive
pass
# d) verify association of IP :thinking:
pass
