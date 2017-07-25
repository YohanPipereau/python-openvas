

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



"""
{
  "result": "VULNERABLE",
  "notes": "The target uses weak ciphers [ NULL-SHA, AECDH-NULL-SHA]",
  "target": {
    "host": "ip de l'hôte",
  },
  "plugin": {
    "name": "weak_ciphers",
    "version": "1.1",
    "description": "Detects if SSL server accepts weak ciphers.",
  }
} 
"""
"""
SERVER <|> ALARM <|> 188.185.74.71 <|> 22/tcp <|> Installed version: 6.6.1
Fixed version:     6.9

 <|> 1.3.6.1.4.1.25623.1.0.806049 <|> SERVER
"""


"""
^[SERVER <|> LOG <|> 188.185.74.71 <|> 80/tcp <|> Here is the Nikto report:
- ***** RFIURL is not defined in nikto.conf--no RFI tests will run *****
- Nikto v2.1.6
---------------------------------------------------------------------------
+ Target IP:          188.185.74.71
+ Target Hostname:    188.185.74.71
+ Target Port:        80
+ Virtual Host:       openvas5.cern.ch
+ Start Time:         2017-07-21 12:53:56 (GMT0)
---------------------------------------------------------------------------
+ Server: No banner retrieved
+ The X-XSS-Protection header is not defined. This header can hint to the user agent to protect against some forms of XSS
+ The X-Content-Type-Options header is not set. This could allow the user agent to render the content of the site in a different fashion to the MIME type
+ Root page / redirects to: https://openvas5.cern.ch:9392/login/login.html
+ No CGI Directories found (use '-C all' to force check all possible dirs)
+ ERROR: Error limit (20) reached for host, giving up. Last error: er
ror reading HTTP response
+ Scan terminated:  20 error(s) and 2 item(s) reported on remote host
+ End Time:           2017-07-21 12:55:38 (GMT0) (102 seconds)
---------------------------------------------------------------------------
+ 1 host(s) tested

 <|> 1.3.6.1.4.1.25623.1.0.14260 <|> SERVER
"""
