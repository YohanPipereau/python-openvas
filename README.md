

This python code aims at interacting directly with openvassd, also named openvas-scanner using the OTP protocol.

# Features:

* Indicate the path to the unix socket used by openvassd : (by default: /var/run/openvassd.sock)
* Sort out the NVT by the OS/devices targeted called families (Ubuntu, Cisco, gentoo, ...)

#Required Packages and program

*openvas-manager (optional)
-/usr/bin/greenbone-certdata-sync
-/usr/bin/greenbone-scapdata-sync
-/usr/bin/openvas-certdata-sync
-/usr/bin/openvas-migrate-to-postgres
-/usr/bin/openvas-portnames-update
-/usr/bin/openvas-scapdata-sync
-/usr/bin/openvasmd

*openvas-scanner (required)
-/usr/bin/greenbone-nvt-sync
-/usr/bin/openvas-mkcert
-/usr/bin/openvas-mkcert-client
-/usr/bin/openvas-nvt-sync
-/usr/bin/openvassd

*openvas-libraries (???)
-/usr/bin/openvas-nasl
-/usr/bin/openvas-nasl-lint

*openvas-cli (optional)
-/usr/bin/check_omp
-/usr/bin/omp
-/usr/bin/omp-dialog

*greenbone-security-assistant (optional)
-/usr/bin/gsad


# Required configuration:

*Dependancies:
-openvas-scanner
-python
-python-progressbar

* openvas-handler only works with OTP scanners
* openvas-scanner version required is >= 5.1.0 which implements unix socket (otherwise change the code to talk to TCP socket)
* Add/Change the following line to your /etc/openvas/openvassd.conf: kb_location = /var/run/redis/redis.sock
* Add/Change the following lines to your /etc/redis.conf:
unixsocket /var/run/redis/redis.sock
unixsocketperm 700
port 0
timeout 0

# Use the OTP Shell

Open connection with the socket: nc -U /var/run/openvassd.sock

* to keep the connection to the socket opened you need to write
< OTP/2.0 >

* to print out the configuration including the preferences (part of it loaded from /etc/openvas/openvassd.conf):
CLIENT <|> NVT_INFO <|> CLIENT

* Display NVT (vulnerabilities) list:
< OTP/2.0 >
CLIENT <|> NVT_INFO <|> CLIENT
CLIENT <|> COMPLETE_LIST <|> CLIENT

* Run an attack (scan) on an IP:
< OTP/2.0 >
CLIENT <|> PREFERENCES <|>
plugin_set <|> 1.3.6.1.4.1.25623.1.0.810330
port_range <|> value_of_port
(lot of options here, please read conf/scan.conf)
<|> CLIENT
CLIENT <|> LONG_ATTACK 
length_of_ip (ex:12)
host_ip (ex:100.100.50.1) ou 188.184.88.1

* Stop a running task/scan
CLIENT <|> STOP_WHOLE_TEST <|> CLIENT

# Openvas slang
* Rules: Rules in Openvas specifies who it should scan
* Plugins: Plugins are NVT in fact
* NVT : network vulnerabilty test
* OTP : it is the protocol used to talk to the scanner
* OSP : it is a protocol aiming at substituting OTP but which has a daemon running apart from the scanner called ospd
* families : group of OS:devices targeted by a scan. NVTs belong to a family
* task: it is a scan

# Resources:
You might want to take a look at the former commands: http://www.openvas.org/compendium/otp-commands.html
or just read opevas-scanner source code: https://wald.intevation.org/scm/viewvc.php/trunk/openvas-scanner/src/?root=openvas

# Bug report

* openvas-scanner hangs after reboot and when you strace it seems the error comes after the connection with the redis.sock:
-Try to empty the redis database: redis-cli -s /var/run/redis/redis.sock flushall
-Check the database is indeed clear: redis-cli -s /var/run/redis/redis.sock dbsize
openvassd stores data in redis database 1 (SELECT 1), thus, oid can be retrieved by doing ("KEYS" "oid:*:name")
then SMEMBERS 'oid:<oid>:name' to get the path to the plugin in /var/lib/openvas/plugins

*python-openvas report socket.error Broken pipe.
Restart openvas-scanner.


* openvas-scanner fails to start:
-Check in /var/run/ if you have a openvassd.pid file, it is due to openvas-scanner launched without systemd
-kill openvas-scanner: pkill -9 openvassd
-remove the pid file: rm /var/run/openvassd.pid
-Relaunch the service: systemctl restart openvas-scanner
-Cross your fingers
