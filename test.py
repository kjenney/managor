import managor
import pulumi

## Testing managor module inside a Docker container

def pulumi_program():
    config = pulumi.Config()
    pulumi.export('test', 'test')

args = managor.args()
stack = managor.manage(args, pulumi_program)
