import gedit

import gtk
import gtk.glade

import gobject

import os
import time

import menuManager

GLADE_FILE = os.path.join(os.path.dirname(__file__), "commit.glade")

class PluginHelper:
	def __init__(self, plugin, window):
		self.window = window
		self.plugin = plugin

		self.createActionManager()

		self.menuManager = menuManager.MenuManager(window)
		self.load_dialogs()


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
		self._search_dialog.show()
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
		
	 ###
	# Called when the "Close" button is clicked.
	def on_cancel_button_clicked(self, close_button):
		self._search_dialog.hide()
	
	def on_commit_button_clicked(self, close_button):
		pass
		
	###
    # Called when the text to be replaced is changed.
	def on_commit_text_changed(self, commit_text_entry):
		pass
		
	###
	# Load commit dialog.
	#   - Load dialog from its Glade file
	#   - Connect widget signals
	#   - Put needed widgets in object variables. 
	def load_dialogs(self):
		self.glade_xml = gtk.glade.XML(GLADE_FILE)
		
		self._search_dialog = self.glade_xml.get_widget("commit_dialog")
		self._search_dialog.hide()
		self._search_dialog.set_transient_for(self.window)
		self._search_dialog.connect("delete_event", self._search_dialog.hide_on_delete)

		self._find_button = self.glade_xml.get_widget("commit_button")
		self._find_button.connect("clicked", self.on_commit_button_clicked)

		close_button = self.glade_xml.get_widget("cancel_button")
		close_button.connect("clicked", self.on_cancel_button_clicked)

		self._search_text_box = self.glade_xml.get_widget("commit_text")
		self._search_text_box.connect("changed", self.on_commit_text_changed)


