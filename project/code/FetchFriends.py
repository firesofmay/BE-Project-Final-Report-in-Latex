import re, json

from Database import initdbconfig, updateProfile2db, storefriendsdb, setProfile2db, initializedb, checkdb
from LoginFB import LoginFB
from Decorators import openlink

def FetchFriends(friendscount, pid, browser, acct, conn, tbProfile, tbFriends, Level, orgcount, MainCount):

    """
    Inputs  : Friendscount incmremented by 10, profile ID, browser object, access token, Database Connection,
              Table_Profile_Name, Table_Friends_Name, Level, Original Friends Count, Total People Fetched Count
    Does    : Gets the new list of Friends of the Given pid. 
              friendscount is used in for loop to generate the count incremented by 10, as m.facebook domain
              shows friends list 10 per page. If the actual friend count is lets say 437 (orgcount), friendcount
              value will be 447, which in range(0,447,10) will generate value upto 440 hence we get all the 437 values
              as an example.
    Returns : 
    """
    
    #TODO - Note this Function is quite long, break it for simplicity.

    count = 0

    for val in range(0,friendscount,10):
    
        print "------------------------------------------------------------------------------------"

        #Keep retyring till you get it, using decorators here.
        url = 'http://m.facebook.com/friends/?id=%s&f=%s&refid=5&access_token=%s' % (pid, val, acct)
        (res) = openlink(browser, url)

        htmlfile = res.readlines()

        debugfile = open("debug.html", "w")

        #To debug the current Friends list HTML Being fetched.
        for line in htmlfile:
            debugfile.write(line)

        debugfile.close()


        for line in htmlfile:
            
            #Search for the Line which says Add Friend in the HTML Page just fetched.        
            m = re.search("Add Friend", line)
        
            if m:

                #Find all the Friends Name in this HTML page which is on the Add Friend Line.
                nameit = re.compile(u'name="[^>_=]+"><span>([^>_=]+)</span>')
                nameList = nameit.findall(line)

                #Reverse the nameList as we will pop out one by one values
                nameList.reverse()
                
                #Find all the either Profile IDS OR Usernames from the Regex below.
                matchit = re.compile(r'<div class="c"><a href=".profile.php\?id=([\d]+)|<div class="c"><a href=".([^?]+)')
                idList = matchit.findall(line)
                
                for (profileID,username) in idList:

                    print "------------------------------------------------------------------------------------"

                    #Store the 1st Name in name variable
                    name = nameList.pop()

                    
                    if profileID:
                        print "Value of profileID = " + profileID

                        #Using the profile id just found, get his name, gender, username.
                        # VIA FB API and Access Token.
                        frndpid = str(profileID)
                        (frndpid, name, gender, username) = getUserid(browser, frndpid, acct)

                        print "Name = " + name + "\t\t and "  + "Userid = " + str(frndpid)

                    else:
                        print "Value of username = " + username

                        #Using the username get the profile ID, name, gender, VIA FB API and Access Token.
                        (frndpid, name, gender, username) = getUserid(browser, username, acct)

                        print "Name = " + name + "\t\t and "  + "Userid = " + str(frndpid)
                    
                    #Increment the count of friends done for this users friends list.
                    count += 1

                    #Get the friends number of friends using Regex.
                    (actualcount) = getNumberOfFriends(browser, frndpid)
                
                    #TODO : Note For some profiles, FB API, returns False. Either leave it, or FIX it by
                    #       Swicthing to REGEX Completly. Example Username = vnittoor 
                    #If FB API Did not return a False (= 0) on the friends profile ID, store it, else skip it.
                    if frndpid != 0:
                        storefriendsdb(conn, str(pid), str(frndpid), tbFriends)        
                        setProfile2db(conn, frndpid, name, actualcount, tbProfile, Level, gender, username)

                    else:
                        print "PID = 0, Not inserting it in the database"

                    print "----------------------Count = %s--------------------------------------------------------------" % count
                    MainCount += 1
                    print "Total People Done = " + str(MainCount)


                    #Reissue FB Access Token Every 500 Requests.
                    if MainCount % 500 == 0:
                        (browser, acct) = LoginFB()
                        print ">" * 200
                        print "-----ReLogging In to Facebook and getting New Access Token-----"
                        print "<" * 200


                print "Count of Friends = " + str(count)
                   
    
    print "Actual Friends = " + str(orgcount) + " And Scrapped Friends = " + str(count)
    print "Done All Friends"
    
    #If Friends Fetched Equals Actual Count, set isdone = 1, else -1
    if orgcount == count:
        updateProfile2db(conn, str(pid), tbProfile, count, 1)
    else:
        updateProfile2db(conn, str(pid), tbProfile, count, -1)

    return (MainCount,browser, acct)

