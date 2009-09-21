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

import subprocess


def gitRun(action, arguments, cwd):
	command_line = 'git %s'%action
	if isinstance(arguments, list):
		arguments = " ".join(arguments)
	command_line = command_line+' '+arguments
	command = subprocess.Popen(command_line,shell=True,cwd=cwd,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
	(stdoutdata, stderrdata) = command.communicate()
	return (command.returncode, stdoutdata, stderrdata)
