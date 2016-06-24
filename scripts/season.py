import pandas as pd
import numpy as np

def check_year(date):
	'''
	given a date of an NBA game, returns the season the game was played in

	@param date: date of basketball game
	@return: season that the game belongs to
	'''
    if date.month < 7:
        return date.year
    else:
        return (date.year + 1)