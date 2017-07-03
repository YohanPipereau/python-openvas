

This python code aims at interacting directly with openvassd, also named openvas-scanner using the OTP protocol.

## Required configuration:

You must have installed openvassd and use the OTP scanners. You can check that by running:
openvasmd --get-scanners to get the UUID of the scanners
Then you can verify which type of scanner it is (OSP or OTP) by running:
openvasmd --verify-scanner=<UUID scanner>

## Installation :

* Clone the repository
* run python install setup.py


## Features:

* Indicate the path to the unix socket used by openvassd : (by default: /var/run/openvassd.sock)
* Sort out the NVT by the OS/devices targeted (Ubuntu, Cisco, gentoo, ...)

## TODO:

* Connect to unix socket in python
* Create a class to print out the server configuration of the scanner : CLIENT <|> NVT_INFO in the socket
* Handle the concurrent accesses to the socket
