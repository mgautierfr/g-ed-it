#!/usr/bin/env python
#-*- coding:utf-8 -*-

import gedit
import gtk

import subprocess

import os
import os.path

class DocBar (object):

	def __init__(self, tab, commitDialog):
		self.tab = tab
		self.child = self.tab.get_children()[0]
		self.tab.remove(self.child)
		self.vbox = gtk.VBox()
		
		self.commitDialog = commitDialog
		
		self.doc = self.tab.get_document()
		self.update_handler1 =  self.doc.connect("saved",self.doc_changed)
		self.update_handler2 =  self.doc.connect("loaded",self.doc_changed)
		
		hbox = gtk.HBox() 
		
		self.lbl_status = gtk.Label("État du fichier")
		
		self.btn_add = gtk.Button("add")
		self.btn_add.connect("clicked", self.add_file)
		
		self.btn_commit = gtk.Button("commit")
		self.btn_commit.connect("clicked", self.commit_file)
		
		hbox.pack_start(self.lbl_status, True, False)
		hbox.pack_start(self.btn_add, False, False)
		hbox.pack_start(self.btn_commit, False, False)
		
		self.vbox.pack_start(hbox, False, False)
		self.vbox.pack_start(self.child)
		
		self.tab.add(self.vbox)
		
		self.getDocState()
		
		self.tab.show_all()
		
	def deactivate(self):
		self.tab.remove(self.vbox)
		self.vbox.remove(self.child)
		self.tab.add(self.child)
		
		self.doc.disconnect(self.update_handler1)
		self.doc.disconnect(self.update_handler2)
		
		self.doc = None
		self.vbox = None
		self.child = None
		self.tab = None
		
	def getDocState(self):
		uri = self.doc.get_uri_for_display()
		cwd = os.path.dirname(uri)
		bname = os.path.basename(uri)
		
		self.cached = False;
		self.unmerged = False;
		self.deleted = False;
		self.changed = False;
		self.toBeKilled = False;
		self.other = False;
		
		if not self.doc.is_untitled():
			statusStr = subprocess.Popen(["git-ls-files","--exclude-standard","-m","-c","-d","-o","-v",os.path.basename(uri)],stdout=subprocess.PIPE,cwd=cwd).communicate()[0] 
			statusLines = statusStr.split("\n")
			for statusLine in statusLines[:-1]:
				status = statusLine.split()[0]
				if status == "H": self.cached = True
				if status == "M": self.unmerged = True
				if status == "R": self.deleted = True
				if status == "C": self.changed = True
				if status == "K": self.toBeKilled = True
				if status == "?": self.other = True
		self.setDocInfo()
		pass
	
	def setDocInfo(self):
		self.btn_add.set_sensitive(False)
		self.btn_commit.set_sensitive(False)
		if self.doc.is_untitled():
			self.lbl_status.set_label("Nouveau fichier")
		else:
			if self.other:
				self.lbl_status.set_label("not in the index and doesn't differ (may be tracked or not)")
				self.btn_add.set_sensitive(True)
			if self.cached:
				self.lbl_status.set_label("in the index (will be commited)")
				self.btn_commit.set_sensitive(True)
			if self.changed:
				self.lbl_status.set_label("differ from the index (will not be commited)")
				self.btn_add.set_sensitive(True)
			if self.cached and self.changed:
				self.lbl_status.set_label("In the index but contain uncached modifications")
		pass
	
	def doc_changed(self,doc,arg1):
		self.getDocState()
		
	def add_file(self,button):
		uri = self.doc.get_uri_for_display()
		subprocess.call(["git-add",os.path.basename(uri)],stdout=subprocess.PIPE,cwd=os.path.dirname(uri))
		self.getDocState()
		pass
		
	def commit_file(self,button):
		uri = self.doc.get_uri_for_display()
		self.commitDialog.show(uri)
		self.getDocState()
		pass
		
