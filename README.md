# smpl

__smpl__ is a personal cli tool in python3 for installing c/c++ dependencies for c/c++ projects.

## Installation

The package is still in its early days and is not yet pip3 installable.

In the unlikely event that the reader is interested in trying it, the project can installed by cloning the repo and doing a local pip3 install. 

```bash
git clone git@github.com:robertblackwell/smpl.git
pip3 install --user ./smpl
```
## Sample project

Note there is a sample project called __project_pig__ within the repo that has a config file already setup to install some predefined c/c++ dependencies for this sample project. The package can be demonstrated on the sample project __without__ the local install described in under the previous heading.

## Prerequisites

Current development work is undertaken on Ubuntu 18.04 with g++ 9.0, python 3.6 and so thats where, currently (April 2020), the package is known to work.

Some of the packages in the sample project (project_pig, see below) require cmake 3.16 to build.

A python3 installation with pip3 and yaml is required. 

## Usage

Its a cli tool, so usage (after installing) is easy. To get more details run smpl help.

```bash
smpl --help
```
It should be run from the project root directory of a c/c++ project and expects to find a config file in that directory names `smpl.yaml`.

As mentioned above the repo contains a sample c/c++ project called `project_pig` where one can run an install of predefined dependencies by running the command

```bash
cd smpl
cd project_pig
python3 ../runner.py --clean-before 
```
This does __NOT__ depend on the local pip3 install described above.

But, be warned, this installs boost_1.72 and openssl_1.1.1f plus some other stuff and will perform a __large number__ of g++/clang++ compiles. 

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)