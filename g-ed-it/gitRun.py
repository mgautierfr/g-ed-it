#!/usr/bin/env python
#-*- coding:utf-8 -*-

import subprocess


def gitRun(action, arguments, cwd):
	command_line = 'git %s'%action
	if isinstance(arguments, list):
		arguments = " ".join(arguments)
	command_line = command_line+' '+arguments
	command = subprocess.Popen(command_line,shell=True,cwd=cwd,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
	(stdoutdata, stderrdata) = command.communicate()
	return (command.returncode, stdoutdata, stderrdata)
