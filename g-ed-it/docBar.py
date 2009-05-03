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
import subprocess

import os
import os.path

class DocBar (object):
	code2status = dict({None:'Unchanged',
	                    'A':'Added',
	                    'C':'Copied',
	                    'D':'Deleted',
	                    'M':'Modified',
	                    'R':'Renamed',
	                    'T':'Type changed',
	                    'U':'Unmerged',
	                    'X':'Unknown',
	                    'B':'pairing Broken'
	                   })
	def __init__(self, tab, gitAction, window, docHelper):
		self.tab = tab
		self.gitAction = gitAction
		self.docHelper = docHelper
		
		self.docBar = gtk.HBox() 
		
		self.lbl_status = gtk.Label("État du fichier")
		
		self.commit_text = gtk.Entry()
		
		self.btn_add = gtk.Button("add")
		self.btn_add.connect("clicked", self.gitAction.add, self.tab.get_document().get_uri_for_display)
		
		self.btn_commit = gtk.Button("commit")
		self.btn_commit.connect("clicked", self.gitAction.commit, window, self.tab.get_document().get_uri_for_display,self.get_and_clear_commitText)
		
		self.btn_diff_head_index = gtk.Button("diff HEAD/INDEX")
		self.btn_diff_head_index.connect("clicked", self.gitAction.diff_head_index, self.tab.get_document().get_uri_for_display)
		
		self.btn_diff_index_wt = gtk.Button("diff INDEX/WT")
		self.btn_diff_index_wt.connect("clicked", self.gitAction.diff_index_wt, self.tab.get_document().get_uri_for_display)
		
		self.docBar.pack_start(self.btn_diff_head_index, False, False)
		self.docBar.pack_start(self.btn_diff_index_wt, False, False)
		self.docBar.pack_start(self.lbl_status, True, True)
		self.docBar.pack_start(self.commit_text, True, True)
		self.docBar.pack_start(self.btn_commit, False, False)
		self.docBar.pack_start(self.btn_add, False, False)
		
		self.tab.pack_start(self.docBar, False, False)
		
		self.tab.show_all()
		
		self.update_ui()
		
	def get_and_clear_commitText(self):
		text = self.commit_text.get_text()
		self.commit_text.set_text("")
		return text
		
	def deactivate(self):
		self.tab.remove(self.docBar)
		
		self.docBar = None
		self.tab = None
		
	def update_ui(self):
		if not self.docHelper.inGitDir :
			self.docBar.hide()
			return 
		self.docBar.show()
		self.btn_add.set_sensitive(self.docHelper.index2WT!=None or not self.docHelper.isCached)
		self.btn_commit.set_sensitive(self.docHelper.HEAD2index!=None)
		self.commit_text.set_sensitive(self.docHelper.HEAD2index!=None)
		self.btn_diff_head_index.set_sensitive(self.docHelper.HEAD2index!=None)
		self.btn_diff_index_wt.set_sensitive(self.docHelper.index2WT!=None)
		text = "HEAD <-"
		text = text + DocBar.code2status[self.docHelper.HEAD2index]
		text = text + "-> INDEX <-"
		if self.docHelper.isCached :
			text = text + DocBar.code2status[self.docHelper.index2WT]
		else:
			text = text + DocBar.code2status['A']
		text = text + "-> WT"
		self.lbl_status.set_label(text)
