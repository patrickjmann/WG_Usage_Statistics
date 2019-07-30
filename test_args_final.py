# python script to test loading of parameters
#
from __future__ import print_function
import sys
import argparse
import datetime
from dateutil import parser
import itertools
#import dateutil
SCRIPTNAME = sys.argv[0]+": "
#-------------------------------------------------------------------------------
class Options:
    """Get the options from the command-line"""
    start_date_default = datetime.datetime(2019,1,1)
    end_date_default = datetime.datetime.now()

    def test_dates(self):
        if self.end_date <= self.start_date:
            print(CLASSNAME, "ERROR: end_date is before start_date")
            exit(1)

    def get_from_args(self):
        arg_parser = argparse.ArgumentParser( description="Test the python command-line argument parser. Uses datetime and argparser" )
        start_date_default_str = self.start_date_default.strftime("%Y-%m-%d")
        arg_parser.add_argument( 'start_date', help="start date (default="+start_date_default_str+")", nargs='?', default=start_date_default_str )

        end_date_default_str = self.end_date_default.strftime("%Y-%m-%d")
        arg_parser.add_argument( "end_date", help="end date (default="+end_date_default_str+")", nargs='?', default=end_date_default_str )
        args = arg_parser.parse_args( )
        self.start_date = parser.parse( args.start_date )
        self.end_date = parser.parse( args.end_date )

    def __init__(self):
        self.get_from_args()
        self.CLASSNAME = self.__class__.__name__
        print( "Class name        = \"", self.CLASSNAME, "\"", sep='' )
        print( "Class description = \"", self.__doc__, "\"", sep='' )

#===============================================================================
options = Options()
options.get_from_args()
print( "options.start_date_default = ", options.start_date_default )
print( "options.end_date_default   = ", options.end_date_default )
print( "options.start_date = ", options.start_date )
print( "options.end_date   = ", options.end_date )

# format date into the usage api format: year-month-date

usage_api_date = options.start_date.strftime( "%Y-%m-%d" )
print( SCRIPTNAME, "Start date formatted for usage api (Year-month-day)", usage_api_date )

options.test_dates()
