##
##  Playing about with puthon to get arguments
##

import sys, argparse

__requirements = ['NICK','CONFIG','CHANNEL','SERVER','IDENT','REALNAME']


def __parseConfig(options):
    """
    __parseConfig
    -> dict -> dict
    Parse a config file.
    """
    try:
        f = open(options['CONFIG'])
    except:
        print 'CANNOT OPEN CONFIG FILE'
        __usage()
        assert False, 'Config does not exist'
    
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


def __parseArguments(options):
    """
    __parseArguments
    -> dict -> dict
    Parse runtime arguments
    """
    desc="""
    Laamaj IRC Bot
        Grabber of links and pictures
        Hopefully eventually a shower of them"""
    aParse = argparse.ArgumentParser(description='Laamaj IRC Bot\nGrabber of links/pictures and hopefully shower of them')
    aParse.add_argument('-t','--test',action='store_true',help='Engage test mode')
    aParse.add_argument('-c','--config',help='Specify config file (default .../laamaj/config.cfg')
    args = aParse.parse_args()

    print args
    
    if args.test:
        toupdate = {'TESTMODE':True,'NICK':'laamajtest','IDENT':'laamajtest','CHANNEL':'laamajtest'}
        for k, v in toupdate.iteritems():
            options[k] = v
    
    if args.config:
        options['CONFIG'] = args.config

    return options


def __optionExists(options, req):
    """
    __optionExists
    -> dict -> str -> bool
    Check if value exists.
    Print error and return
    """
    if req not in options.keys():
        warning = "ERROR: {0} has not been set.".format(req)
        print warning
        assert False, warning
    return True


def __validateOptions(options):
    """
    __validateOptions
    -> dict -> bool
    Check all required options have been set in config.
    """
    for requirement in __requirements:
        __optionExists(options, requirement)
    return True


def getParameters():
    """
    getPerameters
    -> dict
    Return config accorging to config file overridden by command line arguments
    """
    options = {'TESTMODE':False, 'CONFIG':'../config.cfg'}
    options = __parseArguments(options)
    options = __parseConfig(options) 
    __validateOptions(options)

    return options


if __name__ == '__main__':
    """
    Quick testing 
    """
    print getParameters()
