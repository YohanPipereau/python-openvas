

print("""
1) Display Scanner configuration infos
2) List NVT vulnerabilities with their id, families, etc...
3) Run a scan
4) Get shell access to the scanner (speak OTP please, more info in man.md...)
""")


try:
    choice=int(input("Enter your option: "))
    if choice == 1:
        #Run the Display scanner information object
        print("not yet")
    if choice == 2:
        #Run the List NVT vulerabilities object
        print("not yet")
    if choice == 3:
        #variables Required: hosts_ip, ports
        #Run a scan
        print("not yet")
    if choice == 4:
        #
        print("not yet")

except (NameError, SyntaxError):
    print "You should not run the program while drunk, please enter an integer"
