# coding = utf-8
"""
	定义点类
"""
class point(object):

	def __init__(self, x, y, classtype):
		self._x = x
		self._y = y
		self._ClassType = classtype
		self._Probably = 0

	def getX(self):
		return self._x

	def getY(self):
		return self._y

	def getClassType(self):
		return self._ClassType

	def getProbably(self):
		return self._Probably

	def setX(self, x):
		self._x = x

	def setY(self, y):
		self._y = y

	def setClassType(self, classtype):
		self._ClassType = classtype

	def setProbably(self, probably):
		self._Probably = probably







