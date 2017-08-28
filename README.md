This package include three tools and a library:
* python-openvas which is a python wrapper to interact with openvassd, using the OTP protocol.
* openvas-blacklist is a python script which help the user with blacklisting of OID.
* magicredis is a bash script useful to solve the problem of hanging scans.

# Installation:

Read INSTALL.md file.

# Features:

* Scan a target according to families (General, CISCO, Malware, Buffer overflow ...)
* Send Email with report
* Write report to a file
* Send report in json output for Apache Flume
* Blacklist OIDs not to get them in report
* python-openvas only works with OTP scanners

# Required Packages :

* openvas-scanner >=5.1.0 (required)
* openvas-libraries (required)
* python-progressbar (required)
* greenbone-security-assistant (optional)
* openvas-manager (optional)

# Informations:

* openvas-scanner version required is >= 5.1.0 which implements unix socket (otherwise change the code to talk to TCP socket)

##### Make sure your redis server is configured properly :
* Add/Change the following line to your /etc/openvas/openvassd.conf: kb_location = /var/run/redis/redis.sock
* Add/Change the following lines to your /etc/redis.conf:
unixsocket /var/run/redis/redis.sock
unixsocketperm 700
port 0
timeout 0

##### Use the OTP Shell

Open connection with the socket: nc -U /var/run/openvassd.sock

* to keep the connection to the socket opened you need to write : 
> < OTP/2.0 >

* to print out the configuration including the preferences (part of it loaded from /etc/openvas/openvassd.conf): 
> CLIENT <|> NVT_INFO <|> CLIENT

* Display NVT (vulnerabilities) list:
> < OTP/2.0 >
> CLIENT <|> NVT_INFO <|> CLIENT
> CLIENT <|> COMPLETE_LIST <|> CLIENT

* Run an attack (scan) on an IP:
> < OTP/2.0 >
> CLIENT <|> PREFERENCES <|>
> plugin_set <|> 1.3.6.1.4.1.25623.1.0.810330
> port_range <|> value_of_port
> (lot of options here, please read conf/scan.conf)
> <|> CLIENT
> CLIENT <|> LONG_ATTACK 
> length_of_ip (ex:12)
> host_ip (ex:100.100.50.1) ou 188.184.88.1

* Stop a running task/scan
> CLIENT <|> STOP_WHOLE_TEST <|> CLIENT

##### Openvas slang
* Rules: Rules in Openvas specifies who it should scan
* Plugins: Plugins are NVT in fact
* NVT : network vulnerabilty test
* OTP : it is the protocol used to talk to the scanner
* OSP : it is a protocol aiming at substituting OTP but which has a daemon running apart from the scanner called ospd
* families : group of OS:devices targeted by a scan. NVTs belong to a family
* task: it is a scan

##### Resources:
You might want to take a look at the former commands: http://www.openvas.org/compendium/otp-commands.html
Or read opevas-scanner source code: https://wald.intevation.org/scm/viewvc.php/trunk/openvas-scanner/src/?root=openvas

# Bug report

#### openvas-scanner hangs
openvas-scanner hangs after reboot and when you strace it seems the error comes after the connection with the redis.sock:

> Try to empty the redis database: redis-cli -s /var/run/redis/redis.sock flushall
> Check the database is indeed clear: redis-cli -s /var/run/redis/redis.sock dbsize

*Details for the bug: 'A new database get added everytime we run a scan and is supposed to get deleted at some point but sometimes it is not. 
Multiple KBs can be served in parallel, for multiple hosts scanned by one or several tasks. This is done using redis databases, which are independent namepaces. The DBs 0 & 1, are reserved.
It contains a single variable, called 'OpenVAS.__GlobalDBIndex'. This variable is a bitmap of the different namespaces. 
When opening a new DB, the scanner will look for the first bit that is not set, starting from 1 to the maximum number of available DBs.
If none is found, the scanner will enter a wait and retry loop. 
Otherwise, it will (atomically, along with the check) set the bit to 1 and switch to the selected namespace.'
In redis.conf file, you can change the number of databases run redis-cli -s /var/run/redis/redis.sock INFOKEYSPACE in order to get the number of databases currently used in redis-server.*

[openVAS Mailing List for this Bug report](http://lists.wald.intevation.org/pipermail/openvas-discuss/2017-August/011380.html)

#### openvas-scanner fails to start:

> Check in /var/run/ if you have a openvassd.pid file, it is due to openvas-scanner launched without systemd
> kill openvas-scanner: pkill -9 openvassd
> remove the pid file: rm /var/run/openvassd.pid
> relaunch the service: systemctl restart openvas-scanner
