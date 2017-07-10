#This file aims at parsing the NVT_INFO output to get all the oid

class ParseOid:

    def __init__(self):
        message="""
        < OTP/2.0 >
        CLIENT <|> NVT_INFO <|> CLIENT
        CLIENT <|> COMPLETE_LIST <|> CLIENT
        """
        
    """
    if match_plugin[cmpt] == data and cmpt <= len(match_plugin):
        cmpt=cmpt+1
        msg.append(data)
        if msg == match_plugin:
            #Appelle la méthode parse_oid which parse oid and put in the proper families
    else:
        match_plugin = "SERVER <|> PLUGIN_LIST <|>"
        msg=""
        cmpt=0
    """
    #parser plugin:


    #SERVER <|> PLUGIN_LIST <|>
    #oid <|> Name of NVT <|> infos <|> Licence of vulnerability <|> Family <|> ID of revision <|> CVE id <|> BID (bugtrack id) <|> URL <|> Description \n
    # <|> SERVER

    #Parse the plugin and put the oid in lists
