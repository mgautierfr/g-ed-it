#!/usr/bin/env python
#-*- coding:utf-8 -*-

import subprocess


def gitRun(action, arguments, cwd):
	command_line = 'git %s '%action
	command_lines = [command_line]
	command_lines.append(arguments)
	print command_lines
	command = subprocess.Popen(command_lines,shell=True,cwd=cwd,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
	(stdoutdata, stderrdata) = command.communicate()
	return (command.returncode, stdoutdata, stderrdata)
