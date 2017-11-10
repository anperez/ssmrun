ssmrun
======

.. image:: https://img.shields.io/pypi/v/ssmrun.svg
    :target: https://pypi.python.org/pypi/ssmrun
    :alt: Latest PyPI version

.. image:: https://travis-ci.org/Fullscreen/ssmrun.png
   :target: https://travis-ci.org/Fullscreen/ssmrun
   :alt: Latest Travis CI build status


* GitHub: https://github.com/Fullscreen/ssmrun
* PyPI: https://pypi.python.org/pypi/ssmrun

Utilities for AWS EC2 SSM

* run commands
* list and show invocations


Installation
------------

Install via pip

    $ pip install ssmrun


Usage
-----

Quickly run system commands on Linux nodes:

.. code:: bash

  # Target nodes by name
  $ ssm cmd <target> <system_command> -o

  # Target nodes in an auto scaling group
  $ ssm cmd <target> <system_command> -A -o

  # Target nodes created with a CloudFormation stack (including CFN ASGs)
  $ ssm cmd <target> <system_command> -S -o


Run SSM Command:

.. code:: bash

  # Run on targets filtered by EC2 tag "Name"
  $ ssm run <docutment-name> <ec2-instances-name>

  # Run with SSM parameters
  $ ssm run <docutment-name> <ec2-instances-name> -P p1="v1" -P p2="v2"

  # Run and get status for each targeted instance
  $ ssm run <docutment-name> <ec2-instances-name> -s

  # Run and get command output for each targeted instance
  $ ssm run <docutment-name> <ec2-instances-name> -o

  # Run against instances in an auto scaling group
  $ ssm run <docutment-name> <asg-name> -k aws:autoscaling:groupName

  # Run against instances created via CloudFormation stack
  $ ssm run <docutment-name> <cfn-stack-name> -k aws:cloudformation:stack-name


List and Show SSM Command Invocations:

.. code:: bash

  # Show invocation
  $ ssm show <command-id>

  # Show invocation and targets status
  $ ssm show <command-id> -s

  # Show invocation and targets status and command output
  $ ssm show <command-id> -o

  # List command invocations
  $ ssm ls -n NUM

  # List command invocations and targets status
  $ ssm ls -s


List and Show SSM Documents:

.. code:: bash

  # List documents
  $ ssm docs

  # List documents with details
  $ ssm docs -l

  # Get document content
  $ ssm get <doc-name>


Authors
-------

`ssmrun` was written by `Fullscreen Devops <devops@fullscreen.com>`_.
