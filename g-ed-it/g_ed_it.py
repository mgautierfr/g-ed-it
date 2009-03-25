import gedit

import gtk
import gtk.glade

import gobject

import os
import time

import menuManager
import commitDialog

GLADE_FILE = os.path.join(os.path.dirname(__file__), "commit.glade")

class PluginHelper:
	def __init__(self, plugin, window):
		self.window = window
		self.plugin = plugin

		self.createActionManager()
		self.glade_xml = gtk.glade.XML(GLADE_FILE)

		self.menuManager = menuManager.MenuManager(self.window)
		
		self.commitDialog = commitDialog.CommitDialog(self.window,self.glade_xml)

		# I hardly even know how this works, but it gets our encoding.
		try: self.encoding = gedit.encoding_get_current()
		except: self.encoding = gedit.gedit_encoding_get_current()
		
	def deactivate(self):        
		self.menuManager.deactivate()
		self.manager.remove_action_group(self.action_group)
		
		self.window = None
		self.plugin = None
		
	def update_ui(self):
		return
		    
	def action_commit(self, window):
		self.commitDialog.show()
		pass

	def action_add(self, window):
		pass
		
	def createActionManager(self):
		self.manager = self.window.get_ui_manager()
		
		
		self.action_group = gtk.ActionGroup("GitPluginActions")
		
		self.git_menu_action = gtk.Action(name="GitMenu",
		                                   label="Git",
		                                   tooltip="Manage git",
		                                   stock_id=None)
		self.commit_action    = gtk.Action(name="Commit",
		                                   label="Commit",
		                                   tooltip="Commit current state",
		                                   stock_id=gtk.STOCK_GO_UP)
		self.add_action       = gtk.Action(name="Add",
		                                   label="Add to index",
		                                   tooltip="",
		                                   stock_id=gtk.STOCK_ADD)
		
		self.commit_action.connect("activate", self.action_commit)
		self.add_action.connect("activate", self.action_add)
		
		self.action_group.add_action(self.git_menu_action)
		self.action_group.add_action(self.commit_action)
		self.action_group.add_action(self.add_action)

		# Add the action group.
		self.manager.insert_action_group(self.action_group, -1)
		pass


