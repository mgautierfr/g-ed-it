#!/usr/bin/env python
#-*- coding:utf-8 -*-

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

class MenuManager (object):

	def __init__(self, window):
		self.window = window
		self.ui_id = None
		self.insert_menu_item(window)
		
	def insert_menu_item(self, window):
		self.manager = self.window.get_ui_manager()
		self.ui_id = self.manager.add_ui_from_string(ui_string)
		
	def deactivate(self):        
		self.manager.remove_ui(self.ui_id)
		self.manager.ensure_update()
		
		self.window = None


