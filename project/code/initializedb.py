import MySQLdb

def initializedb(conn, tbProfile, tbFriends):

    """
    Inputs  : Database Connection, Table_Profile_Name, Table_Friends_Name
    Does    : Creates Database, Tables, Sets UTF8 enabled.
    Returns : Nothing
    """

    c = conn.cursor()

    #Supress warning if table already exists
    c.execute ('SET sql_notes = 0')

    c.execute("create database if not exists fbdata")

    #Switch to fbdata database.
    c.execute("use fbdata")

    #check following to understand how to create AUTO_INCREMENT on a non_primary key coloumn
    #http://stackoverflow.com/questions/922308/is-it-possible-to-have-an-auto-increment-column-that-permits-duplicates


    c.execute('create table if not exists ' + tbProfile +  '(seqid BIGINT UNSIGNED NOT NULL AUTO_INCREMENT, pid BIGINT UNSIGNED primary key, name varchar(50) character set utf8 NOT NULL, usrname varchar(30), frnds integer, stamp timestamp, scraped integer, isdone integer,Level integer, Sex varchar(8) NOT NULL, KEY (seqid))')
    
    c.execute('CREATE TABLE if not exists  '+tbFriends+' (pid1 BIGINT, pid2 BIGINT, INDEX fpid1 (pid1), FOREIGN KEY (pid1) REFERENCES '+tbProfile+'(pid), INDEX fpid2 (pid2), FOREIGN KEY (pid2) REFERENCES '+tbProfile+'(pid))')

    #Allows you to view unicode Character
    c.execute("set names utf8")

    #Enable warnings Again
    c.execute ('SET sql_notes = 1')


    conn.commit()
    c.close()


