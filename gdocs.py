#!/usr/bin/env python
"""
Rapsberry Pi Projects For Dummies: temperate logger to google docs spreadsheet
Adapted from Guy Carpenter (http://guy.carpenter.id.au/gaugette/) https://github.com/guyc/py-gaugette
For the Raspberry Pi
"""

import gaugette.oauth
import datetime
import gdata.service
import sys
  
def LogRowInGDocSpreadsheet(CLIENT_ID, CLIENT_SECRET, SPREADSHEET_KEY, HEADINGS, TEMPERATURE, UOM):                  
        oauth = gaugette.oauth.OAuth(CLIENT_ID, CLIENT_SECRET)
        if not oauth.has_token():
                user_code = oauth.get_user_code()
                print "Go to %s and enter the code %s" % (oauth.verification_url, user_code)
                oauth.get_new_token()
         
        gd_client = oauth.spreadsheet_service()
        spreadsheet_id = SPREADSHEET_KEY
        
        try:
                worksheets_feed = gd_client.GetWorksheetsFeed(spreadsheet_id)
        except gdata.service.RequestError as error:
            if (error[0]['status'] == 401):
                    oauth.refresh_token()
                    gd_client = oauth.spreadsheet_service()
                    worksheets_feed = gd_client.GetWorksheetsFeed(spreadsheet_id)
            else:
                    raise
        
        worksheet_id = worksheets_feed.entry[0].id.text.rsplit('/',1)[1]
         
        now = datetime.datetime.now().isoformat(' ')
        row = {
            #google docs spreadsheet columns must be in lowercase
            HEADINGS[0].lower(): str(TEMPERATURE),
            HEADINGS[1].lower(): now,
            HEADINGS[2].lower(): UOM
            }

        try:
                gd_client.InsertRow(row, spreadsheet_id, worksheet_id)
        except gdata.service.RequestError as error:
                if (error[0]['status'] == 400):
                    oauth.refresh_token()
                    gd_client = oauth.spreadsheet_service()
                    gd_client.InsertRow(row, spreadsheet_id, worksheet_id)
                else:
                    raise
          
