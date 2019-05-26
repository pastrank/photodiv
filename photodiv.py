#!/usr/bin/python3
# -*- coding: utf-8 -*-
""" this script is to divide an imaged, composed by white background and other
	multiple images, in more files"""

import os
import subprocess
import shutil
import sys


def extgetcmd(comando):
	""" run a program and get the results
	:param comando: the command line that will be launched
	:return: output of the command line
	"""
	if os.name == "nt":
		comando = comando.replace("'", "\"")

	arr = []
	p = subprocess.Popen(comando, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	for line in p.stdout.readlines():
		try:
			arr.append(line.strip().decode('ascii'))
		except:
			try:
				arr.append(line.strip().decode('utf-8'))
			except:
				arr.append(line.strip().decode('ascii', 'ignore'))
		p.wait()
		#retval = p.wait()

	return "\n".join(arr)


def extruncmd(comando, showoutput):
	"""
	:param comando:
	:param showoutput:
	:return:
	run a program without getting results """
	if os.name == "nt":
		comando = comando.replace("'", "\"")

	arr = []
	p = subprocess.Popen(comando, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	if showoutput:
		for line in p.stdout.readlines():
			arr.append(line.strip().decode('ascii'))
			print("  executing:\n" + comando, 0)
		p.wait()


def processall(res, mypath, myimage):
	nomedir = os.path.join(mypath, os.path.splitext(myimage)[0])
	lista = res.split("\n")
	contatore = 0
	
	if os.path.isdir(nomedir):
		shutil.rmtree(nomedir, True)
		
	os.makedirs(nomedir)
		
	if lista:
		for l in lista:
			contatore += 1
			tok = l.split()
			prov = ""
			try:
				prov = tok[1]
			except:
				pass
			if prov != "":
				if prov.find("+0+") < 0:
					rescont = '{:04d}'.format(contatore)
					comando = "convert '" + os.path.join(mypath, myimage) + "' -crop " + prov 
					comando += " '" + os.path.join(nomedir, rescont + ".jpg")  + "'"
					extruncmd(comando, False)
					print("Done: " + rescont + ".jpg, " + prov)


if __name__ == "__main__":
	arg = sys.argv[1]
	if arg:
		arg = os.path.abspath(arg)
		spath = os.path.dirname(arg)
		immagine = os.path.basename(arg)
		comando = "convert '" + arg + "' -threshold 90% -morphology dilate octagon -define connected-components:area-threshold=700 "
		comando += "-define connected-components:verbose=true -connected-components 8 -auto-level PNG8:" + spath + "/abcde.png" 
		res = extgetcmd(comando)
		print(res)
		processall(res, spath, immagine)
