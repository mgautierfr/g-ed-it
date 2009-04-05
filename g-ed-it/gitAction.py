#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os.path
import gtk
import subprocess

import commitDialog

GLADE_FILE = os.path.join(os.path.dirname(__file__), "git_windows.glade")

class GitAction (object):
	def __init__(self,plugin):
		self.glade_xml = gtk.glade.XML(GLADE_FILE)
		self.commitDialog = commitDialog.CommitDialog(self.glade_xml,plugin)
		self.plugin = plugin
		pass
	
	def commit(self,launcher,window,fileUriMethod = None):
		if fileUriMethod :
			fileUri = fileUriMethod()
			allFile = False
		else:
			fileUri = window.get_active_document().get_uri_for_display()
			allFile = True
		self.commitDialog.run(window,fileUri,allFile)
		pass
	
	def add(self,launcher,fileUriMethod = None):
		if fileUriMethod : fileUri = fileUriMethod()
		subprocess.call(["git-add",os.path.basename(fileUri)],stdout=subprocess.PIPE,cwd=os.path.dirname(fileUri))
		self.plugin.fast_update_ui()
		pass
	
	def diff_head_index(self,launcher, fileUriMethod = None):
		if fileUriMethod : fileUri = fileUriMethod()
		subprocess.call(["git-diff","--cached",os.path.basename(fileUri)],stdout=subprocess.PIPE,cwd=os.path.dirname(fileUri))
		pass
	
	def diff_index_wt(self, launcher, fileUriMethod = None):
		if fileUriMethod : fileUri = fileUriMethod()
		subprocess.call(["git-diff",os.path.basename(fileUri)],stdout=subprocess.PIPE,cwd=os.path.dirname(fileUri))
		pass
