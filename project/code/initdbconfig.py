import MySQLdb

def initdbconfig():

    """
    Inputs  : Nothing
    Does    : Sets up the database
    Returns : Table_Profile_Name, Table_Friends_Name and Database Connection
    """

    #Configuration Values
    tbProfile = "User_profile"
    tbFriends = "User_friends"

    #Update User Password if its on different machine.
    conn = MySQLdb.connect(host='localhost', port=3306, user='root', passwd='password',charset='utf8')

    return (tbProfile, tbFriends, conn)
