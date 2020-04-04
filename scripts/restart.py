#!/usr/bin/env python3

import os
import time
import boto3

# TERMINATE = True
TERMINATE = False
PROFILE_NAME = "proof"
ENV = os.environ.get("ENVIRONMENT")
if ENV == "dev":
    REGION = "eu-central-1"
elif ENV == "prod":
    REGION = "us-east-1"
else:
    raise AttributeError("Can't find ENVIRONMENT")
EXISTING_EIP = os.environ.get("ELASTIC_IP", None)


def get_name(instance, field="Name", key_name="Key", value_name="Value"):
    for tag in instance.tags:
        if tag[key_name] == field:
            return tag[value_name]
    return


def get_pushpin(ec2, key="Name", status="running", instance_tag="pushpin"):
    for instance in ec2.instances.all():
        name = get_name(instance)
        if instance_tag in name:
            if instance.state[key] == status:
                print(
                    f"Pushpin: {name} ({instance.id} == {instance.public_ip_address})"
                )
                return instance
    return


def find_eips(aws_client, key="Addresses"):
    data = aws_client.describe_addresses()
    for eip in data[key]:
        pip = eip["PublicIp"]
        aip = eip["AllocationId"]

        yieldable = False
        if "InstanceId" not in eip:
            if EXISTING_EIP:
                yieldable = pip == EXISTING_EIP
            else:
                yieldable = True

        if yieldable:
            yield aip, eip


if __name__ == "__main__":
    aws_session = boto3.session.Session(profile_name=PROFILE_NAME, region_name=REGION)

    ############
    # get current instance
    aws_resource = aws_session.resource("ec2")
    pushpin = get_pushpin(aws_resource)
    if pushpin:
        if TERMINATE:
            print(f"Terminating: {pushpin.id}")
            pushpin.terminate()
        else:
            pass
    else:
        raise ValueError("No pushpin found")

    ############
    # verify when the current is alive
    if TERMINATE:
        while True:
            print("Waiting...")
            time.sleep(5)

            pushpin = get_pushpin(aws_resource)
            if pushpin:
                print(f"Found: {pushpin.id}")
                break

    ############
    # verify elastic ip and attach if necessary

    # TODO: check network interfaces and/or nat gateways for those free IP
    # ?region=eu-central-1#NIC:sort=networkInterfaceId
    # ?region=eu-central-1#NatGateways:sort=natGatewayId

    aws_client = aws_session.client("ec2")

    # for element in find_eips(aws_client):
    #     print("FREE?", element)
    try:
        aid, eip = next(find_eips(aws_client))
    except Exception as e:
        print(e.__class__.__name__, e)
        print("No IP to associate")
    else:
        print(f"Allocating: {eip}")
        aws_client.associate_address(AllocationId=aid, InstanceId=pushpin.id)
