import enum
from copy import copy
class Sym(enum.Enum):
	AND = " & "
	OR = " | "
	NOT = "~"
	IMP = " -> "
	IFF = " <-> "
	XOR = " ^ "
	TAUT = "T"
	CONT = "F"
	VAR = None
	def __str__(self):
		return self.value
	def __repr__(self):
		return str(self)

class Sentence:
	def __init__(self, sym, left = None, right = None):
		self.sym = sym
		self.left = left
		self.right = right
	def __str__(self):
		if self.sym == Sym.VAR:
			return str(self.name)
		if self.sym in [Sym.TAUT, Sym.CONT]:
			return str(self.sym)
		if self.sym == Sym.NOT:
			return str(self.sym) + str(self.arg)
		return "(" + str(self.left) + str(self.sym) + str(self.right) + ")"
	def __repr__(self):
		return str(self)
	def __copy__(self):
		return self if self.sym in [Sym.TAUT, Sym.CONT, Sym.VAR] else Sentence(sen.sym, copy(sen.left), copy(sen.right))
	def sencopy(self, claims):
		if self.sym in [Sym.TAUT, Sym.CONT, Sym.VAR]:
			cpy = Sentence(self.sym, self.name)
		elif self.sym == Sym.NOT:
			cpy = Sentence(Sym.NOT, self.arg.sencopy(claims))
		else:
			cpy = Sentence(self.sym, self.left.sencopy(claims), self.right.sencopy(claims))
		claims.add(cpy)
		return cpy
	@property
	def name(self):
		return self.left
	@name.setter
	def name(self, n):
		self.left = n
		self.right = None
	@property
	def arg(self):
		return self.left
	@name.setter
	def arg(self, a):
		self.left = a
		self.right = None

#class Var(Sentence):
#	def __init__(self, name):
#		super().__init__(Sym.VAR)
#		self.name = name
#	def __str__(self):
#		return self.name
#
#class Unop(Sentence):
#	def __init__(self, sym, arg):
#		super().__init__(sym)
#		self.arg = copy(arg)
#	def __str__(self):
#		return str(self.sym) + str(self.arg)
#	def __copy__(self):
#		return Unop(self.sym, self.arg)
#
#class Biop(Sentence):
#	def __init__(self, sym, left, right):
#		super().__init__(sym)
#		self.left = copy(left)
#		self.right = copy(right)
#	def __str__(self):
#		return str(self.left) + str(self.sym) + str(self.right)
#	def __copy__(self):
#		return Biop(self.sym, self.left, self.right)

def Var(name):
	return Sentence(Sym.VAR, name)

def Not(arg):
	return Sentence(Sym.NOT, arg)

def And(left, right):
	return Sentence(Sym.AND, left, right)

def Or(left, right):
	return Sentence(Sym.OR, left, right)

def Imp(left, right):
	return Sentence(Sym.IMP, left, right)

def Iff(left, right):
	return Sentence(Sym.IFF, left, right)

def Xor(left, right):
	return Sentence(Sym.XOR, left, right)

def T():
	return Sentence(Sym.TAUT)
def F():
	return Sentence(Sym.CONT)
