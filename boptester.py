#!/usr/bin/env python

import subprocess
import sys

class RandomTest:	
	def runTest(self):
		random_bits = self.getRandom()
		print("%s: %d bits" % (self.description, random_bits))
	
	def getRandom(self):
		randomness = None
		randomValue = self.getValue()
		for x in xrange(0,99):
			lRandomValue = randomValue
			randomValue = self.getValue()
			matchedBytes = ~(lRandomValue ^ randomValue)
			if randomness:
				randomness &= matchedBytes
			else:
				randomness = matchedBytes
		random_bits = 0
		if sys.maxint > (1 << 33):
			num_bits = 64
		else:
			num_bits = 32
		for x in xrange(0,num_bits):
			if not(randomness & (1 << x)):
				random_bits += 1
		return random_bits
		
class RandomSimpleTest(RandomTest):
	def __init__(self, exeName, description):
		self.description=description
		self.exeName = exeName
	
	def getValue(self):
		p = subprocess.Popen([self.exeName], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		p.wait()
		return int(p.stdout.read(), 16)

randomTests = [
		RandomSimpleTest("getamap", "mmap randomisation"),
		RandomSimpleTest("getdll", "dll randomisation"),
		RandomSimpleTest("getmain", "executable randomisation"),
		RandomSimpleTest("getstack", "stack randomisation"),
		RandomSimpleTest("getvsyscall", "vsyscall randomisation"),
		RandomSimpleTest("getheap", "heap randomisation")
	]

for rtest in randomTests:
	rtest.runTest()
