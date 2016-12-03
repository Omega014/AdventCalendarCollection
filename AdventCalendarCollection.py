import json
import os
from datetime import datetime

import ui

import scraper


class AdventCalendarCollection (object):
    def __init__(self):
        self.view = ui.load_view('AdventCalendarCollection')
        self.view.background_color = "#ffedd9"
        self.view.present('fullscreen')
        self.view.name = 'AdventCalendarCollection'
        self.reload_data(None)
        
    def refresh(self, sender):
        scraper.main()
        self.reload_data(None)

    def reload_data(self, sender):
        
        today = str(datetime.now().day)
        self.view['textview'+today].background_color = '#ffd9d9'
        
        filepath = os.path.join(os.path.realpath('./'), 'registrations.json')
        with open(filepath, 'r') as f:
            registrations = json.load(f)

        for data in registrations:
            day = data['date'].split('-')[-1]
            if day[0] == '0':
                day = day[1]
            title = data['title']
            self.view['textview'+day].text = title


AdventCalendarCollection()
