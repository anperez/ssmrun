# -*- coding: utf-8 -*-

import sys
import time
import click
from cfntools import __version__
from ssm import Ssm


sys.tracebacklimit = 0


@click.command()
@click.version_option(version=__version__)
@click.argument('ssm-docutment')
@click.argument('target')
@click.option('-o', '--show-output', is_flag=True)
@click.option('-k', '--target-key', default='Name', help='Target tag key (default: Name)')
@click.option('-c', '--comment', default='', help='Command invocation comment')
@click.option('-i', '--interval', default=1.0, help='Check interval (default: 1.0s)')
@click.option('-p', '--profile', default=None, help='AWS profile')
@click.option('-r', '--region', default=None, help='AWS region')
def main(ssm_docutment, target, show_output, target_key, comment, interval, profile, region):
    """Utilities for AWS EC2 SSM

       \b
       ssmrun --help
    """
    ssm = Ssm(profile=profile, region=region)
    cmd = ssm.send_command_to_targets(
        document=ssm_docutment, key=target_key, value=target, comment=comment)
    print '==> ' + ssm.command_url(cmd['CommandId'])

    while True:
        time.sleep(interval)
        out = ssm.list_commands_by_command_id(cmd['CommandId'])
        print '%13s' % ('[' + out[0]['Status'] + '] ') + \
            'Targets: ' + str(out[0]['TargetCount']) + \
            ' Completed: ' + str(out[0]['CompletedCount']) + \
            ' Errors: ' + str(out[0]['ErrorCount'])
        if out[0]['Status'] not in ['Pending', 'InProgress']:
            if out[0]['TargetCount'] == out[0]['CompletedCount']:
                if show_output:
                    res = ssm.list_command_invocations(
                        cmd['CommandId'], Details=True)
                    if len(res) != 0:
                        print '\n'
                        print_command_output_per_instance(res)
                break


def print_command_output_per_instance(invocations):
    for i in invocations:
        print ' '.join(['***', i['Status'], i['InstanceId'], i['InstanceName']])
        for cp in i['CommandPlugins']:
            print cp['Output']


if __name__ == "__main__":
    main()
