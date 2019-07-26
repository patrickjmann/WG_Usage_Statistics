# python script to test loading of parameters
#
from __future__ import print_function
import sys
import argparse
import datetime
from dateutil import parser
#import dateutil

SCRIPTNAME=sys.argv[0]
##print( "number of arguments:", len(sys.argv) )
##print( "List of arguments: ", str(sys.argv) )
##print( "---------------------------------------------------")
##print()

def give_help():
    print(SCRIPTNAME, "give some help\nAnother line")
    print("  another line")

year = 2019
month = 1
day = 1
start_date_default = datetime.datetime(year, month, day)
start_date_default_str = start_date_default.strftime("%y-%m-%d")

arg_parser = argparse.ArgumentParser( description="Test the python command-line argument parser. Uses datetime and argparser" )
##parser.add_argument( 'integers', metavar='N', type=int, nargs='+', help="start date" )
arg_parser.add_argument( '--verbosity', type=int, choices=[0,1,2],
                         help='verbosity level' )
arg_parser.add_argument( 'start_date', help="start date (default="+start_date_default_str+")", nargs='?', default=start_date_default_str )

end_date_default = datetime.datetime.now()
end_date_default_str = end_date_default.strftime("%Y-%m-%d")
arg_parser.add_argument( "end_date", help="end date (default="+end_date_default_str+")", nargs='?', default=end_date_default_str )
args = arg_parser.parse_args( )

print( SCRIPTNAME, "Current Date/Time ", datetime.datetime.now() )
print( SCRIPTNAME, "The verbosity is ", args.verbosity )

print( SCRIPTNAME, "The raw start date is ", args.start_date )
start_date = parser.parse( args.start_date )
print( SCRIPTNAME, "The parsed start date is ", start_date )

# format date into the usage api format: year-month-date

usage_api_date = start_date.strftime( "%Y-%m-%d" )
print( SCRIPTNAME, "Start date formatted for usage api (Year-month-day)", usage_api_date )

print( SCRIPTNAME, "The raw end date is ", args.end_date )
end_date = parser.parse( args.end_date )
print ( SCRIPTNAME, "The parsed end date is", end_date )

if end_date <= start_date:
    print(SCRIPTNAME, "ERROR: end_date is before start_date")
    exit(1)

print( "running the give_help function")
give_help()
