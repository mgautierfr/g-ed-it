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
		
		self.btn_diff_head_index = gtk.Button("diff HEAD/INDEX")
		self.btn_diff_head_index.connect("clicked", self.diff_head_index)
		
		self.btn_diff_index_wt = gtk.Button("diff INDEX/WT")
		self.btn_diff_index_wt.connect("clicked", self.diff_index_wt)
		
		hbox.pack_start(self.btn_diff_head_index, False, False)
		hbox.pack_start(self.btn_diff_index_wt, False, False)
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
		
		self.HEAD2index = None
		self.index2WT = None
		
		if not self.doc.is_untitled():
			statusStr = subprocess.Popen(["git-diff","--cached","--name-status",os.path.basename(uri)],stdout=subprocess.PIPE,cwd=cwd).communicate()[0]
			if statusStr != "":
				status = statusStr[:-1].split()[0]
				self.HEAD2index = status
			statusStr = subprocess.Popen(["git-diff","--name-status",os.path.basename(uri)],stdout=subprocess.PIPE,cwd=cwd).communicate()[0]
			if statusStr != "":
				status = statusStr[:-1].split()[0]
				self.index2WT = status
		self.setDocInfo()
		pass
	
	def setDocInfo(self):
		self.btn_add.set_sensitive(self.index2WT!=None)
		self.btn_commit.set_sensitive(self.HEAD2index!=None)
		self.btn_diff_head_index.set_sensitive(self.HEAD2index!=None)
		self.btn_diff_index_wt.set_sensitive(self.index2WT!=None)
		if self.doc.is_untitled():
			self.lbl_status.set_label("Nouveau fichier")
		else:
			text = "HEAD -- "
			if self.HEAD2index == "A":
				text = text + "Added"
			elif self.HEAD2index == "C":
				text = text + "Copied"
			elif self.HEAD2index == "D":
				text = text + "Deleted"
			elif self.HEAD2index == "M":
				text = text + "Modified"
			elif self.HEAD2index == "R":
				text = text + "Renamed"
			elif self.HEAD2index == "T":
				text = text + "Type changed"
			elif self.HEAD2index == "U":
				text = text + "Unmerged"
			elif self.HEAD2index == "X":
				text = text + "Unknown"
			elif self.HEAD2index == "B":
				text = text + "pairing Broken"
			text = text + " --> INDEX -- "
			if self.index2WT == "A":
				text = text + "Added"
			elif self.index2WT == "C":
				text = text + "Copied"
			elif self.index2WT == "D":
				text = text + "Deleted"
			elif self.index2WT == "M":
				text = text + "Modified"
			elif self.index2WT == "R":
				text = text + "Renamed"
			elif self.index2WT == "T":
				text = text + "Type changed"
			elif self.index2WT == "U":
				text = text + "Unmerged"
			elif self.index2WT == "X":
				text = text + "Unknown"
			elif self.index2WT == "B":
				text = text + "pairing Broken"
			text = text + " --> WT"
			self.lbl_status.set_label(text)
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
		print "End of the commit !!!!!!!!"
		self.getDocState()
		pass

	def diff_head_index(self,button):
		uri = self.doc.get_uri_for_display()
		subprocess.call(["git-diff","--cached",os.path.basename(uri)],cwd=os.path.dirname(uri))
		pass
	
	def diff_index_wt(self,button):
		uri = self.doc.get_uri_for_display()
		subprocess.call(["git-diff",os.path.basename(uri)],cwd=os.path.dirname(uri))
		pass
