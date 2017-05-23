from invoke import task
import os, sys

@task
def aws_creds_are_set(ctx,
                      home):
  creds_file = "{0}/.aws/credentials".format(home)

  if not os.path.isfile(creds_file):
    print "Aws creds not set, setting them now."

    ctx.run("mkdir -p {0}/.aws".format(home))

    with open(creds_file, 'w') as creds:
      creds.write("""[default]
region=us-west-2
aws_access_key_id={0}
aws_secret_access_key={1}
""".format(os.environ['aws_access_key_id'],
           os.environ['aws_secret_access_key']))

@task
def cloudformation_deploy(ctx):
  ctx.run("aws cloudformation deploy --template cloudformation/api-gateway.yaml --stack-name api-gateway-rewrite-redirect-poc")

@task
def travis_creds(ctx):
  ctx.run("aws cloudformation deploy --template cloudformation/travis.yaml --stack-name api-gateway-rewrite-redirect-poc-travis-creds --capabilities CAPABILITY_NAMED_IAM")