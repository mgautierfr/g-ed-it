import gedit

import gtk
import gtk.glade

import gobject

import os
import time

ui_string = """<ui>
  <menubar name="MenuBar">
    <placeholder name="ExtraMenu_1">
      <menu action="GitMenu">
        <menuitem action="Commit"/>
        <menuitem action="Add"/>
      </menu>
    </placeholder>
  </menubar>
</ui>
"""

GLADE_FILE = os.path.join(os.path.dirname(__file__), "commit.glade")

class PluginHelper:
	def __init__(self, plugin, window):
		self.window = window
		self.plugin = plugin
		
		self.ui_id = None

		# Add a "toggle split view" item to the View menu
		self.insert_menu_item(window)
		self.load_dialogs()


		# I hardly even know how this works, but it gets our encoding.
		try: self.encoding = gedit.encoding_get_current()
		except: self.encoding = gedit.gedit_encoding_get_current()
		
	def deactivate(self):        
		self.remove_menu_item()
		
		self.window = None
		self.plugin = None
		
	def update_ui(self):
		return
		    
	def commit_action(self, window):
		self._search_dialog.show()
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
		

	def add_action(self, window):
		pass

	def insert_menu_item(self, window):
		manager = self.window.get_ui_manager()
		
		self.action_group = gtk.ActionGroup("GitPluginActions")
		
		self.git_menu_action_ = gtk.Action(name="GitMenu", label="Git",          tooltip="Manage git", stock_id=None)
		self.commit_action_   = gtk.Action(name="Commit",  label="Commit",       tooltip="Commit current state", stock_id=gtk.STOCK_GO_UP)
		self.add_action_      = gtk.Action(name="Add",     label="Add to index", tooltip="", stock_id=gtk.STOCK_ADD)
		self.commit_action_.connect("activate", self.commit_action)
		self.add_action_.connect("activate", self.add_action)
		
		self.action_group.add_action(self.git_menu_action_)
		self.action_group.add_action(self.commit_action_)
		self.action_group.add_action(self.add_action_)

		# Add the action group.
		manager.insert_action_group(self.action_group, -1)

		self.ui_id = manager.add_ui_from_string(ui_string)
		
	def remove_menu_item(self):
		manager.remove_ui(self.ui_id)
		manager.remove_action_group(self.action_group)
		manager.ensure_update()
		
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


