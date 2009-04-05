import gedit

import os
import os.path

import windowHelper
import gitAction

class G_ed_it(gedit.Plugin):
	def __init__(self):
		gedit.Plugin.__init__(self)
		self.windowHelpers = {}
		self.gitAction = gitAction.GitAction(self)
		
	def activate(self, window):
		self.windowHelpers[window] = windowHelper.WindowHelper(self, window, self.gitAction)
		
	def deactivate(self, window):
		self.windowHelpers[window].deactivate()
		
	def update_ui(self, window):
		self.windowHelpers[window].update_ui()
	
	def fast_update_ui(self):
		for windowHelper in self.windowHelpers :
			self.windowHelpers[windowHelper].fast_update_ui()
		
