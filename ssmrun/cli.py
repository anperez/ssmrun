# -*- coding: utf-8 -*-

import sys
import time
import datetime
import click
from cfntools import __version__
from ssm import Ssm


sys.tracebacklimit = 0

lpad = 13
lfill = '%13s'


@click.command()
@click.argument('ssm-docutment')
@click.argument('target')
@click.option('-s', '--show-stats', is_flag=True)
@click.option('-o', '--show-output', is_flag=True)
@click.option('-k', '--target-key', default='Name', help='Target tag key (default: Name)')
@click.option('-c', '--comment', default='', help='Command invocation comment')
@click.option('-i', '--interval', default=1.0, help='Check interval (default: 1.0s)')
@click.option('-p', '--profile', default=None, help='AWS profile')
@click.option('-r', '--region', default=None, help='AWS region')
def run(ssm_docutment, target, show_stats, show_output, target_key, comment, interval, profile, region):
    """Send SSM command to target"""
    ssm = Ssm(profile=profile, region=region)
    cmd = ssm.send_command_to_targets(
        document=ssm_docutment, key=target_key, value=target, comment=comment)
    print '==> ' + ssm.command_url(cmd['CommandId'])
    print 'Command ID: ' + cmd['CommandId']

    while True:
        time.sleep(interval)
        out = ssm.list_commands(CommandId=cmd['CommandId'])
        # Print final results when done
        if out[0]['Status'] not in ['Pending', 'InProgress']:
            if out[0]['TargetCount'] == out[0]['CompletedCount']:
                command_stats(cmd['CommandId'], out[0])
                if show_stats or show_output:
                    res = ssm.list_command_invocations(
                        cmd['CommandId'], Details=True)
                    if len(res) != 0:
                        print
                        print_command_output_per_instance(res, show_output)
                break
        # Print progress
        print lfill % ('[' + out[0]['Status'] + '] ') + \
            'Targets: ' + str(out[0]['TargetCount']) + \
            ' Completed: ' + str(out[0]['CompletedCount']) + \
            ' Errors: ' + str(out[0]['ErrorCount'])


@click.command()
@click.argument('command-id')
@click.option('-i', '--instanceId', default=None, help='Filter on instance id')
@click.option('-s', '--show-stats', is_flag=True)
@click.option('-o', '--show-output', is_flag=True)
@click.option('-p', '--profile', default=None, help='AWS profile')
@click.option('-r', '--region', default=None, help='AWS region')
def show(command_id, instanceid, show_stats, show_output, profile, region):
    """Get status/output of command invocation"""
    ssm = Ssm(profile=profile, region=region)
    out = ssm.list_commands(CommandId=command_id, InstanceId=instanceid)
    url = ssm.command_url(command_id)
    command_stats(command_id, out[0], url)

    if show_stats or show_output:
        res = ssm.list_command_invocations(
            command_id, instanceid, Details=True)
        if len(res) != 0:
            print
            print_command_output_per_instance(res, show_output)


@click.command()
@click.argument('ssm-docutment', default='')
@click.option('-l', '--long-list', is_flag=True, help='Detailed list')
@click.option('-p', '--profile', default=None, help='AWS profile')
@click.option('-r', '--region', default=None, help='AWS region')
def docs(ssm_docutment, long_list, profile, region):
    """List SSM Docutments"""
    ssm = Ssm(profile=profile, region=region)
    docs = ssm.list_documents()
    print 'total ' + str(len(docs))
    for d in docs:
        if long_list:
            print d['Name'], d['Owner'], d['PlatformTypes'], d['DocumentVersion'], d['DocumentType'], d['SchemaVersion']
        else:
            print d['Name']


@click.command()
@click.option('-u', '--invocation-url', is_flag=True, help='Command invocation url')
@click.option('-p', '--profile', default=None, help='AWS profile')
@click.option('-r', '--region', default=None, help='AWS region')
def ls(invocation_url, profile, region):
    """List SSM Command Invocations"""
    ssm = Ssm(profile=profile, region=region)
    invocations = ssm.list_commands()
    for i in invocations:
        if invocation_url:
            url = ssm.command_url(i['CommandId'])
            command_stats(i['CommandId'], i, url)

        command_stats(i['CommandId'], i)


def command_stats(commandId, invocation, invocation_url=None):
    if invocation_url:
        print '==> ' + invocation_url

    i = invocation
    print lfill % ('[' + i['Status'] + '] ') + \
        i['CommandId'] + ' ' + \
        i['DocumentName']
    print ' ' * lpad + str(i['RequestedDateTime'])
    print ' ' * lpad + 'Targets: ' + str(i['TargetCount']) + \
        ' Completed: ' + str(i['CompletedCount']) + \
        ' Errors: ' + str(i['ErrorCount'])


def print_command_output_per_instance(invocations, show_output=False):
    for i in invocations:
        print ' '.join(['***', i['Status'], i['InstanceId'], i['InstanceName']])
        if show_output:
            for cp in i['CommandPlugins']:
                print cp['Output']


@click.group()
@click.version_option(version=__version__)
def main(args=None):
    """Utilities for AWS EC2 SSM

       \b
       ssm --help
       ssm <command> --help
    """

main.add_command(docs)
main.add_command(ls)
main.add_command(show)
main.add_command(run)

if __name__ == "__main__":
    main()
