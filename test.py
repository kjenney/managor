import managor
import pulumi

## Testing managor module inside a Docker container

def pulumi_program():
    config = pulumi.Config()
    environment = config.require('environment')
    aws_region = config.require('aws_region')
    config_data = managor.get_config(environment)
    subnet1_cidr = config_data['vpc']['subnet1']['cidr']
    pulumi.export('subnet1_cidr', subnet1_cidr)
    pulumi.export('aws_region', aws_region)

args = managor.args()
stack = managor.manage(args, pulumi_program)
