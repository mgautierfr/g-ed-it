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

import docHelper

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
	def __init__(self, gitAction, window):
		self.gitAction = gitAction
		self.window = window
		
		self.currentTab = None
		self.create_docBar()
		
		self.swap_to_currentTab(window.get_active_tab())
			
		self.window.connect("active-tab-changed",self.active_tab_changed)
		self.window.connect("active-tab-state-changed",self.active_tab_state_changed)
		
	def create_docBar(self):
		self.docBar = gtk.HBox() 
		self.lbl_status = gtk.Label("État du fichier")
		
		self.commit_text = gtk.Entry()
		
		self.btn_add = gtk.Button("add")
		self.btn_add.connect("clicked", self.gitAction.add)
		
		self.btn_commit = gtk.Button("commit")
		self.btn_commit.connect("clicked", self.gitAction.commit, self.window,self.get_and_clear_commitText)
		
		self.btn_diff_head_index = gtk.Button("diff HEAD/INDEX")
		self.btn_diff_head_index.connect("clicked", self.gitAction.diff_head_index)
		
		self.btn_diff_index_wt = gtk.Button("diff INDEX/WT")
		self.btn_diff_index_wt.connect("clicked", self.gitAction.diff_index_wt)
		
		self.docBar.pack_start(self.btn_diff_head_index, False, False)
		self.docBar.pack_start(self.btn_diff_index_wt, False, False)
		self.docBar.pack_start(self.lbl_status, True, True)
		self.docBar.pack_start(self.commit_text, True, True)
		self.docBar.pack_start(self.btn_commit, False, False)
		self.docBar.pack_start(self.btn_add, False, False)
		
	def active_tab_changed(self,window,tab):
		print "tab_change"
		self.swap_to_currentTab(tab)
	
	def active_tab_state_changed(self,window):
		print "tab_state_changed"
		self.update_docBar_ui()
		
	def swap_to_currentTab(self, tab):
		if self.currentTab:
			self.currentTab.remove(self.docBar)
		self.currentTab = tab
		if self.currentTab:
			self.currentTab.pack_start(self.docBar, False, False)
			self.currentTab.show_all()
		self.update_docBar_ui()
		
	def get_and_clear_commitText(self):
		text = self.commit_text.get_text()
		self.commit_text.set_text("")
		return text
		
	def deactivate(self):
		if self.currentTab:
			self.currentTab.remove(self.docBar)
		
		self.docBar = None
		self.currentTab = None
		
	def update_docBar_ui(self):
		if not self.currentTab:
			return
		_docHelper = self.currentTab.get_data(docHelper.DocHelper.KEY)
		if not _docHelper or not _docHelper.inGitDir :
			self.docBar.hide()
			return 
		
		self.docBar.show()
		self.btn_add.set_sensitive(_docHelper.index2WT!=None or not _docHelper.isCached)
		self.btn_commit.set_sensitive(_docHelper.HEAD2index!=None)
		self.commit_text.set_sensitive(_docHelper.HEAD2index!=None)
		self.btn_diff_head_index.set_sensitive(_docHelper.HEAD2index!=None)
		self.btn_diff_index_wt.set_sensitive(_docHelper.index2WT!=None)
		text = "HEAD <-"
		text = text + DocBar.code2status[_docHelper.HEAD2index]
		text = text + "-> INDEX <-"
		if _docHelper.isCached :
			text = text + DocBar.code2status[_docHelper.index2WT]
		else:
			text = text + DocBar.code2status['A']
		text = text + "-> WT"
		self.lbl_status.set_label(text)
