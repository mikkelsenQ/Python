#!/usr/bin/env python
#!/usr/bin/python

# Updates the stock_data.txt file so conky shows up to date information. 
# Intended to run every few minutes during trading hours, through cron. 

import mqfinance

mqfinance.snetw()
