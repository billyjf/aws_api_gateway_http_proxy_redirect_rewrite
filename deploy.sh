#!/bin/bash -e
source common.sh

invoke aws_creds_are_set ~
invoke cloudformation_deploy
invoke base_integration_tests