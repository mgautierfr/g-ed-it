#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os.path
import subprocess

import docBar

class DocHelper (object):
	def __init__(self, tab, window, gitAction):
		self.doc = tab.get_document()
		self.gitAction = gitAction
		self.tab = tab
		self.getDocState()
		
		self.docBar = docBar.DocBar(tab,self.gitAction, window, self)
		
		self.update_handler1 =  self.doc.connect("saved",self.doc_changed)
		self.update_handler2 =  self.doc.connect("loaded",self.doc_changed)
		pass
	
	def deactivate(self):
		self.doc.disconnect(self.update_handler1)
		self.doc.disconnect(self.update_handler2)
		
	def update_ui(self):
		self.getDocState()
		self.docBar.update_ui()
	
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
			subPro = subprocess.Popen(["git-ls-files",os.path.basename(uri)],stdout=subprocess.PIPE,cwd=cwd)
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


