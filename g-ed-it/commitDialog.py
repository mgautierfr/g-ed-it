#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os

import subprocess

class CommitDialog (object):

	def __init__(self,window,glade_xml):
		self.window = window
		self.glade_xml = glade_xml
		self.load_dialog()
		pass
		
	def load_dialog(self):
		self.commit_dialog = self.glade_xml.get_widget("commit_dialog")
		self.commit_dialog.hide()
		self.commit_dialog.set_transient_for(self.window)
		self.commit_dialog.connect("delete_event", self.commit_dialog.hide_on_delete)

		self.commit_button = self.glade_xml.get_widget("commit_button")
		self.commit_button.connect("clicked", self.on_commit_button_clicked)

		self.close_button = self.glade_xml.get_widget("cancel_button")
		self.close_button.connect("clicked", self.on_cancel_button_clicked)

		self.commit_text_box = self.glade_xml.get_widget("commit_text")
		self.commit_text_box.connect("insert-at-cursor", self.on_commit_text_changed)
		
	def on_cancel_button_clicked(self, close_button):
		self.commit_dialog.hide()
	
	def on_commit_button_clicked(self, close_button):
		commit_text_buffer = self.commit_text_box.get_buffer()
		os.system("git-commit -s -m'"+commit_text_buffer.get_text(commit_text_buffer.get_start_iter(),commit_text_buffer.get_end_iter())+"'")
		commit_text_buffer.set_text("")
		self.commit_dialog.hide()
		pass
		
	def on_commit_text_changed(self, commit_text_entry):
		pass
		
	def show(self,fileName=None):
		self.fileName = fileName
		if self.fileName:
			templateMsg = subprocess.Popen(["git-status","-s",os.path.basename(fileName)],stdout=subprocess.PIPE,cwd=os.path.dirname(fileName)).communicate()[0]
		else:
			cwd = os.path.dirname(self.window.get_active_document().get_uri_for_display())
			templateMsg = subprocess.Popen(["git-status","-s"],stdout=subprocess.PIPE,cwd=cwd).communicate()[0]
		self.commit_text_box.get_buffer().set_text(templateMsg)
		self.commit_dialog.show()


