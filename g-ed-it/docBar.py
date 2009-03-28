#!/usr/bin/env python
#-*- coding:utf-8 -*-

import gedit
import gtk
   
class DocBar (object):

	def __init__(self, tab):
		self.tab = tab
		self.child = self.tab.get_children()[0]
		self.tab.remove(self.child)
		self.vbox = gtk.VBox()
		hbox = gtk.HBox() 
		
		self.btn_cancel = gtk.Button("End Splitview")
		self.btn_cancel.connect("clicked", self.end_split_view)
		
		
		hbox.pack_start(self.btn_cancel, False, False)
		
		self.vbox.pack_start(hbox, False, False)
		self.vbox.pack_start(self.child)
		
		self.tab.add(self.vbox)
		
		self.tab.show_all()
		
		print "bar inserted"
		
	def deactivate(self):
		self.tab.remove(self.vbox)
		self.vbox.remove(self.child)
		self.tab.add(self.child)
		
		self.vbox = None
		self.child = None
		self.tab = None
		print "bar removed"
		
	def end_split_view(self):
		pass
