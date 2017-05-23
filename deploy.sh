#!/bin/bash -e
pip install invoke # task runner
pip install requests # http for humans

invoke aws_creds_are_set ~
invoke cloudformation_deploy
