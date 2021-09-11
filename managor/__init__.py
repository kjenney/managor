import argparse
import json
import pulumi
import pulumi_aws as aws
from pulumi import automation as auto
import os
import sys

# Repeatable process for creating/update Pulumi stacks
# Assumes:
#    * pulumi automation module as auto
#    * pulumi-aws module as aws
#    * json module as json
#    * pulumi cli is installed

def args():
    parser = argparse.ArgumentParser(description='Manage a Pulumi automation stack.')
    parser.add_argument('-n', '--project-name', required=False, default='data')
    parser.add_argument('-a', '--aws-region', required=False, default='us-east-1')
    parser.add_argument('-b', '--backend-bucket', required=True)
    parser.add_argument('-s', '--stack-name', required=False, default='dev')
    parser.add_argument('-k', '--kms-alias-name', required=True)
    parser.add_argument('-d', '--destroy', help='destroy the stack',
                        action='store_true')
    return parser.parse_args()

def manage(args, pulumi_program):
    backend_bucket = args.backend_bucket
    project_name = args.project_name
    aws_region = args.aws_region
    kms_alias_name = args.kms_alias_name
    stack_name = f"{args.project_name}-{args.stack_name}"
    secrets_provider = f"awskms://alias/{kms_alias_name}"
    backend_url = f"s3://{backend_bucket}"
    environment = args.stack_name

    os.environ['PULUMI_CONFIG_PASSPHRASE'] = f'{project_name}{stack_name}'
    
    project_settings=auto.ProjectSettings(
        name=project_name,
        runtime="python",
        backend={"url": backend_url}
    )

    stack_settings=auto.StackSettings(
        secrets_provider=secrets_provider)

    stack = auto.create_or_select_stack(stack_name=stack_name,
                                        project_name=project_name,
                                        program=pulumi_program,
                                        opts=auto.LocalWorkspaceOptions(project_settings=project_settings,
                                                                        stack_settings={stack_name: stack_settings}))


    print("successfully initialized stack")

    # for inline programs, we must manage plugins ourselves
    print("installing plugins...")
    stack.workspace.install_plugin("aws", "v4.0.0")
    print("plugins installed")

    # set stack configuration from argparse arguments and secrets
    print("setting up config")
    stack.set_config("aws:region", auto.ConfigValue(value=aws_region))
    stack.set_config("environment", auto.ConfigValue(value=environment))
    print("config set")

    print("refreshing stack...")
    stack.refresh(on_output=print)
    print("refresh complete")

    if args.destroy:
        print("destroying stack...")
        stack.destroy(on_output=print)
        print("stack destroy complete")
        sys.exit()

    print("updating stack...")
    up_res = stack.up(on_output=print)
    print(f"update summary: \n{json.dumps(up_res.summary.resource_changes, indent=4)}")