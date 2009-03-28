import gedit

import os
import os.path

import g_ed_it

class G_ed_it(gedit.Plugin):
	def __init__(self):
		gedit.Plugin.__init__(self)
		self.instances = {}
		
	def activate(self, window):
		self.instances[window] = g_ed_it.G_ed_itHelper(self, window)
		
	def deactivate(self, window):
		self.instances[window].deactivate()
		
	def update_ui(self, window):
		self.instances[window].update_ui()
