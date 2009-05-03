#!/usr/bin/env python

import subprocess
import sys

class TestException(Exception):
	def __init__(msg):
		Exception(msg)

class Test:
	def runTest(self):
		raise Exception("Run test not implemented")
	def printTest(self):
		raise Exception("Print test not implemented")

class RandomTest(Test):	
	def runTest(self):
		self.random_bits = self.getRandom()
	
	def printTest(self):
		print("%40s: %d bits" % (self.description, self.random_bits))
	
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

class RandomLineTest(RandomTest):
	def __init__(self, exeName, description, lineToUse):
		self.description=description
		self.exeName = exeName
		self.lineToUse = lineToUse
	
	def getValue(self):
		p = subprocess.Popen([self.exeName], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		p.wait()
		lines = p.stdout.read().split("\n")
		if len(lines) >= self.lineToUse:
			return int(lines[self.lineToUse], 16)
		else:
			raise TestException("Wanted output line not found")

class ExitValueTest(Test):
	def __init__(self, exeName, description):
		self.description=description
		self.exeName = exeName
	
	def runTest(self):
		p = subprocess.Popen([self.exeName], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		p.wait()
		self.returncode = p.returncode
	
	def printTest(self):
		if self.returncode == 0:
			print("%40s: VULNERABLE" % (self.description))
		else:
			print("%40s: PROTECTED" % (self.description))
	
tests = [
		RandomSimpleTest("getamap", "mmap randomisation"),
		RandomSimpleTest("getdll", "dll randomisation"),
		RandomSimpleTest("getmain", "executable randomisation"),
		RandomSimpleTest("getstack", "stack randomisation"),
		RandomSimpleTest("getvsyscall", "vsyscall randomisation"),
		RandomSimpleTest("getheap", "heap randomisation"),
		RandomLineTest("getstackprotector", "stack protector canary randomisation", 1),
		ExitValueTest("execbss", "Executable BSS"),
		ExitValueTest("execdata", "Executable Data"),
		ExitValueTest("execheap", "Executable Heap"),
		ExitValueTest("execstack", "Executable Stack"),
		ExitValueTest("heap_double_free", "Heap Double Free"),
		ExitValueTest("heap_overflow", "Heap Overflow"),
		ExitValueTest("format", "Format string"),
		ExitValueTest("memcpy_ptr", "Memcpy Return To Function"),
		ExitValueTest("strncpy_ptr", "Strncpy Return To Function"),
		ExitValueTest("strncpys", "Strncpy Return To Function"),
		ExitValueTest("stackoverflow", "Manual stack overflow")
	]

for test in tests:
	test.runTest()

for test in tests:
	test.printTest()
