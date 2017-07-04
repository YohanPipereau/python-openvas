

This python code aims at interacting directly with openvassd, also named openvas-scanner using the OTP protocol.

# Features:

* Indicate the path to the unix socket used by openvassd : (by default: /var/run/openvassd.sock)
* Sort out the NVT by the OS/devices targeted called families (Ubuntu, Cisco, gentoo, ...)

# Required configuration:

You must have installed openvassd and use the OTP scanners. You can check that by running:
openvasmd --get-scanners to get the UUID of the scanners
Then you can verify which type of scanner it is (OSP or OTP) by running:
openvasmd --verify-scanner=<UUID scanner>

openvasmd is not required with this code

# Use the OTP Shell

* to keep the connection to the socket opened you need to write
< OTP/2.0 >

* to print out the configuration including the preferences (part of it loaded from /etc/openvas/openvassd.conf):
CLIENT <|> NVT_INFO

* Display NVT (vulnerabilities) list:
< OTP/2.0 >
CLIENT <|> NVT_INFO
COMPLETE_LIST

* Run an attack (scan) on an IP:
< OTP/2.0 >
< OTP/2.0 >
CLIENT <|> PREFERENCES <|>
port_range <|> value_of_port
<|> CLIENT
CLIENT <|> LONG_ATTACK
length_of_ip (ex:12)
host_ip (ex:100.100.50.1)

# Openvas slang
* Rules: Rules in Openvas specifies who it should scan
* Plugins: Plugins are NVT in fact
* NVT : network vulnerabilty test
* OTP : it is the protocol used to talk to the scanner
* OSP : it is a protocol aiming at substituting OTP but which has a daemon running apart from the scanner called ospd
* families : group of OS:devices targeted by a scan. NVTs belong to a family

# Resources:
You might want to take a look at the former commands: http://www.openvas.org/compendium/otp-commands.html
or just read opevas-scanner source code: https://wald.intevation.org/scm/viewvc.php/trunk/openvas-scanner/src/?root=openvas
