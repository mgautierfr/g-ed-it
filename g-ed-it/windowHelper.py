#!/usr/bin/env python
#-*- coding:utf-8 -*-

#    Copyright 2009 Matthieu Gautier

#    This file is part of g-ed-it.
#
#    g-ed-it is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    any later version.
#
#    g-ed-it is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with g-ed-it.  If not, see <http://www.gnu.org/licenses/>.

import gedit

import gtk
import gtk.glade

import gobject

import os
import time

import docHelper

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

class WindowHelper:
	def __init__(self, plugin, window, gitAction):
		self.window = window
		self.plugin = plugin
		self.gitAction = gitAction
		
		self.docHelpers = {}
		self.create_all_docHelper()

		self.create_actionManager()
		# add menu
		self.ui_id = self.manager.add_ui_from_string(ui_string)
		self.set_call_back()

		
	def deactivate(self):        
		self.manager.remove_ui(self.ui_id)
		self.manager.remove_action_group(self.action_group)
		self.manager.ensure_update()
		self.manager = None
		
		self.window.disconnect(self.added_hid)
		self.window.disconnect(self.removed_hid)
	
		for docHelper in self.docHelpers:
			self.docHelpers[docHelper].deactivate()
		
		self.window = None
		self.plugin = None
		self.gitAction = None
		
	def update_ui(self):
		for docHelper in self.docHelpers:
			self.docHelpers[docHelper].update_ui()
		return
	
	def fast_update_ui(self):
		self.docHelpers[self.window.get_active_document()].update_ui()
		    
	def create_actionManager(self):
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
		
		self.commit_action.connect("activate", self.gitAction.commit, self.window)
		self.add_action.connect("activate", self.gitAction.add)
		
		self.action_group.add_action(self.git_menu_action)
		self.action_group.add_action(self.commit_action)
		self.action_group.add_action(self.add_action)

		# Add the action group.
		self.manager.insert_action_group(self.action_group, -1)
		self.manager.ensure_update()
		pass
		
		
	def create_all_docHelper(self):
		for view in self.window.get_views():
			tab = view
			while (tab.__class__ != gedit.Tab):
				tab = tab.get_parent()
			self.docHelpers[tab.get_document()] = docHelper.DocHelper(tab,self.window,self.gitAction)
		pass
	
	def set_call_back(self):
		self.added_hid = self.window.connect("tab-added",self.on_tab_added)
		self.removed_hid = self.window.connect("tab-removed",self.on_tab_removed)
		pass
	
	def on_tab_added(self,window,tab):
		self.docHelpers[tab.get_document()] = docHelper.DocHelper(tab,self.window,self.gitAction)
		pass
	
	def on_tab_removed(self,window,tab):
		self.docHelpers.pop(tab.get_document()).deactivate()
		pass
		
