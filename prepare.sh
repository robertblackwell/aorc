# This script prepares the directory to run the aorc app in a virtual environment using pyhton3.6
python36=

# fiind python3.6
if command -v python3.6 &> /dev/null
then
    # python3.6 can be called directly
    echo "python3.6" does exist as a specific command
    python36=python3.6
else
    python3_version=`python3 --version`
    echo $python3_version
    if [ "$python3_version" == "Python 3.6.15" ]
    then
        # python3 IS python3.6
        python36=python3
        echo "Its ok python3 is python3.6 == ${python36}"
    else
        # python3.6 not found
        echo "No python3.6 found"
        exit -1
    fi
fi
rm -rf env3.6 || true
${python36} -m virtualenv env3.6
source env3.6/bin/activate
make upgrade_simple_curses
make freeze
${python36} runner.py
