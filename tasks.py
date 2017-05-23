from invoke import task
import os, sys
import requests

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

@task
def base_integration_tests(ctx):
  api_definition = "m5sj78uaq4"  # Changes per fresh deployment of ApiDefinition
  api_gateway_google_url = "https://{0}.execute-api.us-west-2.amazonaws.com/prod/google".format(api_definition)
  api_gateway_amazon_url = "https://{0}.execute-api.us-west-2.amazonaws.com/prod/amazon".format(api_definition)

  # API Gateway /google vs https://www.google.com
  api_gateway_response = requests.get(api_gateway_google_url)
  google_response = requests.get("https://www.google.com")
  assert api_gateway_response.status_code == 200
  assert google_response.text != requests.get("https://www.google.com") # Every back to back request differs
  assert api_gateway_response.text[0:500] == google_response.text[0:500]

  # API Gateway /google/maps vs https://www.google.com/maps
  api_gateway_response = requests.get("{0}/maps".format(api_gateway_google_url))
  google_response = requests.get("https://www.google.com/maps")
  assert api_gateway_response.status_code == 200
  assert "Moved" in api_gateway_response.text
  assert google_response.status_code == 200
  assert "Moved" not in google_response.text

  # API Gateway /amazon vs https://www.amazon.com
  api_gateway_response = requests.get(api_gateway_amazon_url)
  amazon_response = requests.get("https://www.amazon.com")
  assert "All Departments" in api_gateway_response.text
  assert "Robot Check" in amazon_response.text

  print "***** BASE INTEGRATION TESTS SUCCESSFUL"