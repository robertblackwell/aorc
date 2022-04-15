NOC_SHEBANG="--python-shebang='/usr/bin/env python'"
MYNAME="Robert Blackwell"
MYEMAIL="rob@whiteacorn.com"
PROJECT_NAME="aorc"
LICENSE=MIT
# PREFIX=$(HOME)/.local
NEW_VERSION=
PYTHON=python3
# this is rag-tap collection of convenience options, without any systematic
# set for buildiing and distributing. Sorry



mkvenv:
	python3 -m virtualenv venv

install_requirements:
	python3 -m pip install -r requirements.txt

# install:
# 	$(PYTHON) setup.py install --prefix=$(PREFIX) 

clean:
	$(PYTHON) setup.py clean
	rm -rfv ./build
	rm *whl || true
	rm *.pex || true
	rm -rf env3.6/lib/python3.6/site-packages/simple_curses* || true


push:
	git status
	git add -A
	git commit -a

novenv:
	deactivate	

_license:
	licenser -n $(MYNAME) -e $(MYEMAIL) -l "MIT" -p "smpl"

# use tbump <new_version>
# THIS WILL CREATE A GIT TAG
# see tbump.toml
# thi sis just a remonder
# bump:
# 	tbump $(NEW_VERSION)

bumppatch:
	bumpversion --verbose patch

bumpminor:
	bumpversion --verbose minor

bumpmajor:
	bumpversion --verbose major

git_push_tags:
	git push --tags origin master

git_push: git_commit
	git push --tags origin master

git_commit:
	git add -A | true
	git commit -a | true

git_list_tags:
	git show-ref --tags -d

readme:
	pandoc --from=markdown --to=rst --output=README.rst README.md

.PHONY: dist
dist:
	rm -rfv smpl.egg*
	make readme
	make git_commit
	make bumpminor
	$(PYTHON) setup.py sdist

upload: 
	make dist
	$(PYTHON) setup.py upload