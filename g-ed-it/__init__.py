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

import os
import os.path

import windowHelper
import gitAction

class G_ed_it(gedit.Plugin):
	def __init__(self):
		gedit.Plugin.__init__(self)
		self.windowHelpers = {}
		self.gitAction = gitAction.GitAction(self)
		
	def activate(self, window):
		self.windowHelpers[window] = windowHelper.WindowHelper(self, window, self.gitAction)
		
	def deactivate(self, window):
		self.windowHelpers[window].deactivate()
		
	def update_ui(self, window):
		self.windowHelpers[window].update_ui()
	
		
