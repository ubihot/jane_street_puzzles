#!/usr/bin/env sh 
# ^^ is the above even correct??? the shebang


# create the virtual env with python3.11
# python3.11 doesn't seem to work for importing the model, let's try python3.9
# OK, this was fun, it works in python3.9, thanks https://github.com/ultralytics/ultralytics/issues/8509#issuecomment-1968545813
python3.9 -m venv .venv
source .venv/bin/activate
# to deactivate just run `deactivate`
