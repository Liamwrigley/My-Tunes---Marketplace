import datetime

def datetimeformat(value, format='%I:%M - %a %d %b %Y'):
  #returns datetime object formatted into a string of hour:minute - day/month/year
    return value.strftime(format)

def excerpt(value):
  #creates an excerpt from description
  if len(value) > 115:
    return value[0:115]+'...'
  else:
    return value
    