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
		subprocess.call("git-add "+os.path.basename(fileUri),stdout=subprocess.PIPE,cwd=os.path.dirname(fileUri), shell=True)
		self.plugin.fast_update_ui()
		pass
	
	def diff_head_index(self,launcher, fileUriMethod = None):
		if fileUriMethod : fileUri = fileUriMethod()
		subprocess.call("git-diff --cached "+os.path.basename(fileUri),stdout=subprocess.PIPE,cwd=os.path.dirname(fileUri), shell=True)
		pass
	
	def diff_index_wt(self, launcher, fileUriMethod = None):
		if fileUriMethod : fileUri = fileUriMethod()
		subprocess.call("git-diff "+os.path.basename(fileUri),stdout=subprocess.PIPE,cwd=os.path.dirname(fileUri), shell=True)
		pass
