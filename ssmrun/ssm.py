import boto3

ssm_max_results = 50


class Ssm(object):

    def __init__(self, profile, region):
        self.session = boto3.session.Session(
            profile_name=profile, region_name=region)
        self.region = region
        self.client = self.session.client('ssm')
        self.InstanceIds = []

    def list_documents(self):
        """ Returng a list of SSM Docutments """
        response = self.client.list_documents(MaxResults=ssm_max_results)
        docs = response['DocumentIdentifiers']
        while True:
            if 'NextToken' not in response:
                break
            response = self.client.list_documents(
                NextToken=response['NextToken'], MaxResults=ssm_max_results)
            docs += response['DocumentIdentifiers']
        return docs

    def send_command_to_targets(self, document, key, value, comment):
        """ Send command to key/value taget """
        response = self.client.send_command(
            Targets=[
                {
                    'Key': 'tag:' + key,
                    'Values': [value]
                },
            ],
            DocumentName=document,
            Comment=comment
        )
        return response['Command']

    def list_commands_by_command_id(self, CommandId):
        response = self.client.list_commands(
            CommandId=CommandId,
            MaxResults=ssm_max_results
        )
        commands = response['Commands']
        while True:
            if 'NextToken' not in response:
                break
            response = self.client.list_commands(
                NextToken=response['NextToken'],
                CommandId=CommandId,
                MaxResults=ssm_max_results
            )
        commands += response['Commands']
        return commands

    def list_command_invocations(self, CommandId, Details=False):
        response = self.client.list_command_invocations(
            CommandId=CommandId,
            MaxResults=ssm_max_results,
            Details=Details
        )
        invocations = response['CommandInvocations']
        while True:
            if 'NextToken' not in response:
                break
            response = self.client.list_command_invocations(
                NextToken=response['NextToken'],
                CommandId=CommandId,
                MaxResults=ssm_max_results,
                Details=Details
            )
            invocations += response['CommandInvocations']
        return invocations

    def command_url(self, CommandId):
        if self.region is None:
            self.region = 'us-east-1'
        return 'https://console.aws.amazon.com/ec2/v2/home?region=' + \
            self.region + '#Commands:CommandId=' + \
            str(CommandId) + ';sort=CommandId'
