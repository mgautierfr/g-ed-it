import gedit
import gtk

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

class PluginHelper:
    def __init__(self, plugin, window):
        self.window = window
        self.plugin = plugin
        
        self.ui_id = None

        # Add a "toggle split view" item to the View menu
        self.insert_menu_item(window)

        # We're going to keep track of each tab's split view
        # and, if used, ALT view -- the view of a separate
        # document -- with a couple of dictionaries.  We'll
        # index each dictionary via the tab objects.
        self.split_views = {}
        self.alt_views = {}

        # This keeps track of whether the user is viewing an ALT document.
        self.same_document = {}

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
        pass
    
    def add_action(self, window):
        pass

    def insert_menu_item(self, window):
        manager = self.window.get_ui_manager()
        
        self.action_group = gtk.ActionGroup("GitPluginActions")
        
        # Create an action for the "Run in python" menu option
        # and set it to call the "run_document_in_python" function.
        self.git_menu_action_ = gtk.Action(name="GitMenu", label="Git", tooltip="Manage git", stock_id=None)
        self.commit_action_ = gtk.Action(name="Commit", label="Commit", tooltip="Commit current state", stock_id=gtk.STOCK_GO_UP)
        self.add_action_ = gtk.Action(name="Add", label="Add to index", tooltip="", stock_id=gtk.STOCK_ADD)
        self.commit_action_.connect("activate", self.commit_action)
        self.add_action_.connect("activate", self.add_action)
        
        # Add the action with Ctrl + F5 as its keyboard shortcut.
        self.action_group.add_action(self.git_menu_action_)
        self.action_group.add_action(self.commit_action_)
        self.action_group.add_action(self.add_action_)

        # Add the action group.
        manager.insert_action_group(self.action_group, -1)

        # Add the item to the "Views" menu.
        self.ui_id = manager.add_ui_from_string(ui_string)
        
    def remove_menu_item(self):
        panel = self.window.get_side_panel()
        
        panel.remove_item(self.results_view)

class G_ed_it(gedit.Plugin):
    def __init__(self):
        gedit.Plugin.__init__(self)
        self.instances = {}
        
    def activate(self, window):
        self.instances[window] = PluginHelper(self, window)
        
    def deactivate(self, window):
        self.instances[window].deactivate()
        
    def update_ui(self, window):
        self.instances[window].update_ui()
