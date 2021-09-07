# exp-oleron


## Dependencies

- roblib : https://github.com/nathanfourniol/roblib.git


## Clone the repo

```shell
# Clone the repo HTTPS
git clone https://github.com/nathanfourniol/exp_oleron.git
# Clone the repo SSH
git clone git@github.com:nathanfourniol/exp_oleron.git

# Init submodule
git submodule init
git submodule update

# Do both clone, init submodule
git clone --recurse-submodules git@github.com:nathanfourniol/exp_oleron.git
```


## How to install roblib package

```shell
cd exemples_rob

# Create a python3 venv (store in venv folder)
python3 -m venv venv
# Activate the venv
. venv/bin/activate

# Install roblib
pip install -e roblib # install roblib and dependancies : numpy, scipy, matplotlib
# pip install with -e allow to edit the roblib file (in roblib folder) without having to reinstall the library to take the changes into account

# Check the install
pip freeze #list package installed
# Or
python
# >>> import roblib
# >>> roblib.angle
# <function angle at 0xXXXXXXXXXX>

# Uninstall
pip uninstall roblib
```


## How to use roblib package in .py files

```python
# Import roblib
from roblib import *
# or
import roblib
```
