# managor

Reusable code to build a Pulumi stack with an S3 backend

## Requirements

* Python 3
* argparse
* pulumi
* pulumi-aws

## Testing building

Basic testing with Docker:

```shell
docker build -t managor .
docker run -it --rm --env-file <(aws-vault exec me -- env | grep ^AWS_) managor python test.py -b {{your_s3_bucket}} -k {{your_kms_key}} 
```




