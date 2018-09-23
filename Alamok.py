#!/usr/bin/python3

import gps_logger
import sys
import getopt
import json
import time


def main(argv):
    database_file = ''
    config_file = ''
    try:
        opts, args = getopt.getopt(argv,"hc:o:",["cfile=","ofile="])
    except getopt.GetoptError:
        print ('Alamok.py -c <config_file> -o <database_file>')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print ('Alamok.py -c <config_file> -o <database_file>')
            sys.exit()
        elif opt in ("-c", "--cfile"):
            config_file = arg
        elif opt in ("-o", "--ofile"):
            database_file = arg
    print('Configuration file is ', config_file)
    print('Output file is ', database_file)

    try:
        with open(config_file, 'r') as infile:
            config = json.load(infile)
    except:
        print ('Error in configuration file')
        sys.exit(2)
    gps_log= gps_logger.GpsLogger(config=config,db_filename=database_file)
    gps_log.start()

    try:
        while (True):
            time.sleep(0.1)
    except(KeyboardInterrupt, SystemExit,Exception ) as error:
        gps_log.stop()
        print(error)
        print("bye")


if __name__ == "__main__":
    main(sys.argv[1:])
