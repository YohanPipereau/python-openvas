# Install with already working openvas architecture

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

# Install a reduced architecture from scratch

Install the following packages *openvas-scanner* , *openvas-libraries* with your favorite package manager.

In most cases, redis-server will not be added as depency of openvas-libraries nor openvas-scanner. Only if you install openvas entirely it will install it (no need for that).

Now install *redis* and edit /etc/redis.conf
* Comment 
port 6379

* Uncomment & Add:
unixsocket /var/run/redis/redis.sock
unixsocketperm 700
port 0
timeout 0

Now edit /etc/openvas/openvassd.conf

Add the following line:
kb_location = /var/lib/redis/redis.sock

'''sh
/usr/sbin/openvas-nvt-sync
systemctl start openvas-scanner
'''

# Uninstall

If you want to uninstall, the best would be to remove the following directories/files:
/opt/python-openvas
/usr/bin/openvas-blacklist
/usr/bin/python-openvas
/usr/bin/magicredis
/usr/lib/pythonX.Y/site-packages/python_openvas-<version of package>-pyX.Y.egg
