import json
import os

import ui

from scraper import main


class AdventCalendarCollection (object):
    def __init__(self):
        self.view = ui.load_view('AdventCalendarCollection')
        self.view.background_color = "#fcfcfc"
        self.view.present('fullscreen')
        self.view.name = 'AdventCalendarCollection'
        
        

AdventCalendarCollection()
