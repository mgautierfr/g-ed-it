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

import os
import time
import subprocess

class CommitDialog (object):

	def __init__(self,glade_xml,plugin):
		self.glade_xml = glade_xml
		self.load_dialog()
		self.plugin = plugin
		pass
		
	def load_dialog(self):
		self.commit_dialog = self.glade_xml.get_widget("commit_dialog")
		self.commit_dialog.hide()
		self.commit_dialog.connect("delete_event", self.on_cancel_button_clicked)

		self.commit_button = self.glade_xml.get_widget("commit_button")
		self.commit_button.connect("clicked", self.on_commit_button_clicked)

		self.close_button = self.glade_xml.get_widget("cancel_button")
		self.close_button.connect("clicked", self.on_cancel_button_clicked)

		self.commit_text_box = self.glade_xml.get_widget("commit_text")
		self.commit_text_box.connect("insert-at-cursor", self.on_commit_text_changed)
		
	def run(self,window,fileURI, allFile):
		self.commit_dialog.set_transient_for(window)
		self.current_window = window
		self.cwd = os.path.dirname(fileURI)
		if allFile:
			self.fileName = None
		else:
			self.fileName = os.path.basename(fileURI)
		self.commit_text_box.get_buffer().set_text("")
		self.commit_dialog.show()

	def on_cancel_button_clicked(self, close_button):
		self.commit_dialog.hide()
		self.current_window = None
	
	def on_commit_button_clicked(self, close_button):
		commit_text_buffer = self.commit_text_box.get_buffer()
		commit_text = commit_text_buffer.get_text(commit_text_buffer.get_start_iter(),commit_text_buffer.get_end_iter())
		if self.fileName :
			subprocess.call('git-commit -m "'+commit_text+'" '+self.fileName,stdout=subprocess.PIPE,cwd=self.cwd, shell=True)
		else:
			subprocess.call('git-commit -m "'+commit_text+'"',stdout=subprocess.PIPE,cwd=self.cwd, shell=True)
		commit_text_buffer.set_text("")
		self.commit_dialog.hide()
		self.current_window.emit("active-tab-state-changed")
		self.current_window = None
		pass
		
	def on_commit_text_changed(self, commit_text_entry):
		pass

