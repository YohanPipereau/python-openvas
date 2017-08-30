# Install

Before going any further please make sure your openvassd version is more than 5.1.0
openvassd --version

Start by cloning the git repository
```sh
git clone <this git repository>
```

Change directory to python-openvas where setu.py file lies
```sh
cd python-openvas
```

Launch installation
```sh
python setup.py install
```

# Uninstall

If you want to uninstall, the best would be to remove the following directories/files:
/opt/python-openvas
/etc/python-openvas
/usr/bin/openvas-blacklist
/usr/bin/python-openvas
/usr/bin/magicredis
/usr/lib/pythonX.Y/site-packages/python_openvas-<version of package>-pyX.Y.egg
