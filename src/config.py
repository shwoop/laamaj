"""
Laamaj Config Module.
Parse config file for configuration and override values with any
command line arguments.
"""

import sys
import argparse


_requirements = [
    'NICK','CONFIG','CHANNEL',
    'SERVER','IDENT','REALNAME'
    ]


def _parse_config(options):
    """ Parse the config file. """

    try:
        f = open(options['CONFIG'])
    except:
        print 'ERROR: Cannot open config {0}'.format(options['CONFIG'])
        sys.exit() 
    for line in f:
    
        if '#' in line:
            text, comment = line.split('#',1)
    
        if '=' in line:
            opt, val = line.split('=',1)
            opt = opt.strip()
            val = val.strip()
            if opt not in options.keys():
                options[opt] = val
    
    f.close()
    
    return options


def _parse_arguments(options):
    """ Parse runtime arguments. """

    aParse = argparse.ArgumentParser(
        description='Laamaj IRC Bot\nGrabber of links/pictures \
        and hopefully shower of them'
        )
    aParse.add_argument(
        '-t', '--test', action='store_true',
        help='Engage test mode (join EFNET #laamajtest'
        )
    aParse.add_argument(
        '-c', '--config',
        help='Specify config file (default .../laamaj/config.cfg'
        )
    args = aParse.parse_args()

    if args.test:
        toupdate = {
            'TESTMODE':True,'NICK':'laamajtest',
            'IDENT':'laamajtest','CHANNEL':'laamajtest'
            }
        for k, v in toupdate.iteritems():
            options[k] = v
    
    if args.config:
        options['CONFIG'] = args.config

    return options


def _option_exists(options, req):
    """ Check option has been set. """

    if req not in options.keys():
        print "ERROR: {0} has not been set.".format(req)
        sys.exit()
    return True


def _validate_options(options):
    """ Check all required options have been set in config. """

    for requirement in _requirements:
        _option_exists(options, requirement)
    return True


def get_parameters():
    """
    Return config dictionary accorging to config file overridden by
    command line arguments.
    
    TODO:
    Add list of config keys
    """
    
    options = {'TESTMODE':False, 'CONFIG':'../config.cfg'}
    options = _parse_arguments(options)
    options = _parse_config(options) 
    _validate_options(options)

    return options


if __name__ == '__main__':
    """ test. """
    print get_parameters()
