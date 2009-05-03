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
import subprocess



class DocHelper (object):
	KEY = "G-ED-IT_DOCHELPER_KEY"
	def __init__(self, tab, window, gitAction):
		self.doc = tab.get_document()
		self.gitAction = gitAction
		self.tab = tab
		
		self.tab.set_data(self.KEY,self)
		
		self.getDocState()

		self.update_handler1 =  self.doc.connect("saved",self.doc_changed)
		self.update_handler2 =  self.doc.connect("loaded",self.doc_changed)
		pass
	
	def deactivate(self):
		self.doc.disconnect(self.update_handler1)
		self.doc.disconnect(self.update_handler2)
		self.tab.set_data(self.KEY,self)
		
	def update_ui(self):
		self.getDocState()
	
	def doc_changed(self,doc,arg1):
		self.getDocState()
		
	def getDocState(self):
		uri = self.doc.get_uri_for_display()
		cwd = os.path.dirname(uri)
		bname = os.path.basename(uri)
		
		self.inGitDir = False
		self.isCached = False
		self.HEAD2index = None
		self.index2WT = None
		
		if not self.doc.is_untitled():
			subPro = subprocess.Popen(["git-ls-files",os.path.basename(uri)],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,cwd=cwd)
			statusStr = subPro.communicate()[0]
			if subPro.returncode == 0 :
				self.inGitDir = True
				if statusStr != "":
					self.isCached = True
					statusStr = subprocess.Popen(["git-diff","--cached","--name-status",os.path.basename(uri)],stdout=subprocess.PIPE,cwd=cwd).communicate()[0]
					if statusStr != "":
						status = statusStr[:-1].split()[0]
						self.HEAD2index = status
					statusStr = subprocess.Popen(["git-diff","--name-status",os.path.basename(uri)],stdout=subprocess.PIPE,cwd=cwd).communicate()[0]
					if statusStr != "":
						status = statusStr[:-1].split()[0]
						self.index2WT = status
		pass


