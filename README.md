# aorc

__aorc__ is a personal cli tool in python3.

## Getting started running under python3.6

### step 1 Confirm the python version
Start by confirming the python version:
```
python3 --version
```
if this doe not repond
```
Python 3.6.15
```
then we need to think a little deeper; so stop.

### step 2 - Create a virtual environment
If we are ok with that setp then proceed. The `makefile` calls `python3` which we are now assuming is `python3.6`

Create a virtual environment with
```
    make mkenv
```

### step 3 Install requirements particularly github.com/robertblackwell/simple_curses

NOTE: this next comment is not true. It should install from the github repo 

Make sure that repo `github.com:robertblackwell/simple_curses` has been cloned into a sibling dirctory, and then
install that repo as a dependency with:

```
make install_requirements
```
###step 4 Activate the virtual environment
Activate the virtual environment with:

```
source env/bin/activate
```

### step 5 run the aorc app
Run the `aorc` application with:
```
python3 runner.py
```