

print("
1) Display Scanner configuration infos
2) List NVT vulnerabilities with their id, families, etc...
3) Run a scan
4) Get shell access to the scanner (speak OTP please...)
")

choice=input("Enter your option")
try:
    if choice == 1:
        #Run the Display scanner information object
    if choice == 2:
        #Run the List NVT vulerabilities object
    if choice == 3:


except ValueError:
    print "Please enter an integer"
