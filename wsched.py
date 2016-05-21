#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# wsched.py -- a little script to extract my hours from the brutally hard-to-read
# schedule spreadsheet at work.

import xlrd
import argparse
import datetime
from prettytable import PrettyTable

def get_schedule(filename, week):
    """Opens the workbook provied on the commandline, and extracts all relevant
    data. Returns the dates of the week and the hours I work for that week."""
    
    workbook = xlrd.open_workbook(filename)

    if week == 1: sheet = workbook.sheet_by_name("Week 1")
    elif week == 2: sheet = workbook.sheet_by_name("Week 2")
    elif week == 3: sheet = workbook.sheet_by_name("Week 3")
    elif week == 4: sheet = workbook.sheet_by_name("Week 4")
    
    # get my name + hours from spreadsheet
    schedule = []
    for col in range(1, 21):
        # my name is at row 20 on the spreadsheet.
        schedule.append(sheet.cell_value(20, col))

    # get xlrd dates from spreadsheet
    tmpdates = []
    for col in range(2, 21):
        tmpdates.append(sheet.cell_value(10, col))

    # convert xlrd dates to normal dates
    dates = []
    tmpdates = filter(None, tmpdates)
    for date in tmpdates:
        ttuple = xlrd.xldate_as_tuple(date, 0)
        dates.append(str(datetime.datetime(*ttuple)))

    return dates, schedule


def tableprint_schedule():
    """Displays the data from get_schedule() as a pretty table. Returns nothing.
    """
    
    realdays = ['Sunday', 'Monday', 'Tuesday', 'Wednesday',
                'Thursday', 'Friday', 'Saturday']
    dates, schedule = get_schedule(args.filename, args.week)
    newdates = []
    
    # cut out the month and day from datetime output
    for a in dates:
        newdates.append(a[5:10])

    # format the scheduled hours list. the original list has each start time,
    # end time, and spacer as its own list entry.
    #
    # this takes every third item starting with 0, and every third item
    # starting with 1, and makes a tuple out of them. this lets me skip over
    # the spacer that separates each pair of start/end times.
    newschedule = zip(schedule[0::3], schedule[1::3])

    # prepare the table
    t = PrettyTable(['Day', 'Date', 'Schedule'])

    # iterates over all three lists simultaneously 
    for x, y, z in zip(realdays, newdates, newschedule):
        if z[0] == '':
            z = '0'
        t.add_row([x, y, ' - '.join(map(str, z))])
    
    print t


parser = argparse.ArgumentParser(description='Extract and process hours from schedule.xls')
parser.add_argument('filename', type=str, help='Path to schedule.xls')
parser.add_argument('week', type=int, help='Week number to extract')
args = parser.parse_args()

tableprint_schedule()
