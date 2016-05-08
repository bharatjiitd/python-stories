'''
Created on 07-May-2016

@author: bharat
'''

import sys, getopt

from bj.xsd2dbschemagen.core import gen_db_schema


def main(xsd_schema_filename, db_type):
    gen_db_schema(xsd_schema_filename, {"GroupHeader48"})

if __name__ == "__main__":
    inputfile = ''
    dbtype = ''
    
    try:
        opts, args = getopt.getopt(sys.argv[1:], "i:d:")
    except getopt.GetoptError:
        print('main.py -i <inputfile> -d <db_type>')
        sys.exit()
    
    for opt, arg in opts:
        if opt in ("-i"):
            inputfile = arg
        elif opt in ("-d"):
            dbtype = arg
                
    print("Generating schema for", inputfile, dbtype)            
    main(inputfile, dbtype)