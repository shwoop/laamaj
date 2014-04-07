#!/usr/bin/python
# vim: set fileencoding=utf-8 :
'''
Laamaj Config Module.
Parse config file for configuration and override values with any
command line arguments.
'''

import sys
import argparse


_requirements = [
    u'NICK',u'CONFIG',u'CHANNEL',
    u'SERVER',u'IDENT',u'REALNAME'
    ]


def _parse_config(options):
    ''' Parse the config file. '''

    try:
        f = open(options[u'CONFIG'])
    except:
        print u'ERROR: Cannot open config {0}'.format(options[u'CONFIG'])
        sys.exit() 
    for line in f:
    
        if u'#' in line:
            text, comment = line.split(u'#',1)
    
        if u'=' in line:
            opt, val = line.split(u'=',1)
            opt = opt.strip()
            val = val.strip()
            if opt not in options.keys():
                options[opt] = val
    
    f.close()
    
    return options


def _parse_arguments(options):
    ''' Parse runtime arguments. '''

    aParse = argparse.ArgumentParser(
        description=u'Laamaj IRC Bot\nGrabber of links/pictures \
        and hopefully shower of them'
        )
    aParse.add_argument(
        u'-t', u'--test', action=u'store_true',
        help=u'Engage test mode (join EFNET #laamajtest'
        )
    aParse.add_argument(
        u'-c', u'--config',
        help=u'Specify config file (default .../laamaj/config.cfg'
        )
    args = aParse.parse_args()

    if args.test:
        toupdate = {
            u'TESTMODE':True,u'NICK':u'laamajtest',
            u'IDENT':u'laamajtest',u'CHANNEL':u'laamajtest'
            }
        for k, v in toupdate.iteritems():
            options[k] = v
    
    if args.config:
        options[u'CONFIG'] = args.config

    return options


def _option_exists(options, req):
    ''' Check option has been set. '''

    if req not in options.keys():
        print u'ERROR: {0} has not been set.'.format(req)
        sys.exit()
    return True


def _validate_options(options):
    ''' Check all required options have been set in config. '''

    for requirement in _requirements:
        _option_exists(options, requirement)
    return True


def get_parameters():
    '''
    Return config dictionary accorging to config file overridden by
    command line arguments.
    
    TODO:
    Add list of config keys
    '''
    
    options = {u'TESTMODE':False, u'CONFIG':u'config.cfg'}
    options = _parse_arguments(options)
    options = _parse_config(options) 
    _validate_options(options)

    return options


if __name__ == u'__main__':
    ''' test. '''
    print get_parameters()
