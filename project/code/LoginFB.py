import re, urllib, urllib2, cookielib, getpass, time
from Decorators import openlink

def LoginFB():

    """
    Inputs  : Nothing.
    Does    : Logins to facebook given account.
    Returns : Browser Object, Access Token.
    """
    user = raw_input("Your Facebook Login ID: ")
    passw = getpass.getpass()

    # Initialize the needed modules
    CHandler = urllib2.HTTPCookieProcessor(cookielib.CookieJar())
    browser = urllib2.build_opener(CHandler)
    browser.addheaders = [('User-agent', 'Mozilla/5.0 (X11; Linux i686 on x86_64; rv:7.0.1) Gecko/20100101 Firefox/7.0.1')]
    urllib2.install_opener(browser)
 
    # Initialize the cookies and get the post_form_data
    print 'Initializing..'

    #uses decorator to keep trying ten times
    (res) = openlink(browser, 'http://m.facebook.com/index.php')
    
    mxt = re.search('name="post_form_id" value="(\w+)"', res.read())
    pfi = mxt.group(1)
    print 'Using PFI: %s' % pfi
    res.close()
 
    # Initialize the POST data
    data = urllib.urlencode({
        'lsd'               : '',
        'post_form_id'      : pfi,
        'charset_test'      : urllib.unquote_plus('%E2%82%AC%2C%C2%B4%2C%E2%82%AC%2C%C2%B4%2C%E6%B0%B4%2C%D0%94%2C%D0%84'),
        'email'             : user,
        'pass'              : passw,
        'login'             : 'Log+In'
    })
 
    # Login to Facebook
    print 'Logging in to account ' + user

    #Trying to connect to FB and retrying if failes
    connected = False
    errval = 0
    while not connected:
        try:
            errval +=1
            res = browser.open('https://www.facebook.com/login.php?m=m&refsrc=http%3A%2F%2Fm.facebook.com%2Findex.php&refid=8', data)
            connected = True

        except :
            time.sleep(5)
            print "Trying to Login Again to Facebook, count = " + str(errval)

            if errval == 10:
                break;

            pass


    #If Log out value is not shown, something went wrong, check your localization of your account,
    #maybe its in some other language.
    rcode = res.code
    if not re.search('Logout', res.read()):
        print 'Login Failed'
 
        # For Debugging (when failed login)
        fh = open('debug.html', 'w')
        fh.write(res.read())
        fh.close
 
        # Exit the execution :(
        exit(2)
    res.close()
 
    # Get Access Token
    #Keep retyring till you get it, using decorators here.
    (res) = openlink(browser,'http://developers.facebook.com/docs/reference/api')

    #Extract the access token value
    conft = res.read()
    mat = re.search('access_token=(.*?)"', conft)
    acct = mat.group(1)
    print 'Using access token: %s' % acct

    return (browser, acct)

