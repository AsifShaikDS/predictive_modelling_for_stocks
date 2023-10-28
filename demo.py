# # imports datetime for picking beginning and end dates for the analysis
# import datetime

# # to hide warning messages
# import warnings
# warnings.filterwarnings('ignore')

# # sets the sample period as 5 years back from 09/12/2019
# end = datetime.datetime(2019, 9, 12)
# start = end - datetime.timedelta(days = 7*365)

# print(start)

from get_all_tickers import get_tickers as gt

list_of_tickers = gt.get_tickers()
gt.save_tickers()


# print(list_of_tickers)