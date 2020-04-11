from sentences import *
from copy import copy
from random import randint, choice

def setsenlist(l):
	global senlist
	senlist = l

# special copy function that adds all new sentences to claims
def sencopy(sen, claims):
	return sen.sencopy(claims)

# Helper negation function to prevent double negation
def _not(sen, claims):
	if sen.sym == Sym.NOT:
		claims.remove(sen.arg)
		arg = sen.arg
		sen.sym = arg.sym
		sen.left = arg.left
		sen.right = arg.right
		return sen
	temp = Sentence(sen.sym, sen.left, sen.right)
	claims.add(temp)
	sen.sym = Sym.NOT
	sen.arg = temp
	return sen

def _lassoc(sen, claims):
	if sen.left.sym == sen.sym:
		temp = sen.left.left
		sen.left.left = sen.left.right
		sen.left.right = sen.right
		sen.right = sen.left
		sen.left = temp
		return True
	return False

def _rassoc(sen, claims):
	if sen.sym == sen.right.sym:
		temp = sen.right.right
		sen.right.right = sen.right.left
		sen.right.left = sen.left
		sen.left = sen.right
		sen.right = temp
		return True
	return False

def assoc(sen, claims):
	print("- assoc")
	if randint(0,1):
		ret = _lassoc(sen, claims)
		return ret if ret else _rassoc(sen, claims)
	ret = _rassoc(sen, claims)
	return ret if ret else _lassoc(sen, claims);

def comm(sen, claims):
	print("- comm")
	sen.left, sen.right = sen.right, sen.left
	return True

def _aoneg(sen, sym, claims):
	sen.sym = sym
	_not(sen.left, claims)
	_not(sen.right, claims)
	_not(sen, claims)
	return True

def andneg(sen, claims):
	print("- andneg")
	return _aoneg(sen, Sym.OR, claims)

def orneg(sen, claims):
	print("- orneg")
	return _aoneg(sen, Sym.AND, claims)

def impneg(sen, claims):
	raise Exception

def iffneg(sen, claims):
	print("- iffneg")
	_not(sen.left, claims)
	_not(sen, claims)
	return True

#def xorneg(sen):
#	return _ixneg(sen, Xor, Iff)

def _ldist(sen, claims):
	if (sen.left.sym != Sym.AND and sen.left.sym != Sym.OR) or sen.left.sym == sen.sym:
		return False
	sen.sym, sen.left.sym = sen.left.sym, sen.sym
	temp = sen.left.right
	sen.left.right = sen.right
	sen.right = Sentence(sen.left.sym, temp, sencopy(sen.right, claims))
	claims.add(sen.right)
	return True

def _rdist(sen, claims):
	if (sen.right.sym != Sym.AND and sen.right.sym != Sym.OR) or sen.right.sym == sen.sym:
		return False
	sen.sym, sen.right.sym = sen.right.sym, sen.sym
	temp = sen.right.left
	sen.right.left = sen.left
	sen.left = Sentence(sen.right.sym, sencopy(sen.left, claims), temp)
	claims.add(sen.left)
	return True

def aodist(sen, claims):
	print("- aodist")
	if randint(0,1):
		ret = _ldist(sen, claims)
		return ret if ret else _rdist(sen, claims)
	ret = _rdist(sen, claims)
	return ret if ret else _ldist(sen, claims)

def impdist(sen, claims):
	print("- impdist")
	if randint(0,1):
		ret = _rdist(sen, claims)
		if ret:
			return True
		if not _ldist(sen, claims):
			return False
		sen.sym = Sym.AND if sen.sym == Sym.OR else Sym.OR
		return True
	if _ldist(sen, claims):
		sen.sym = Sym.AND if sen.sym == Sym.OR else Sym.OR
		return True
	return _rdist(sen, claims)

def idem(sen, claims):
	print("- idem")
	rand = randint(0,2)
	sen.left = Sentence(sen.sym, sen.left, sen.right)
	claims.add(sen.left)
	sen.right = sencopy(sen.left, claims)
	if rand == 0:
		sen.sym = Sym.AND
	elif rand == 1:
		sen.sym = Sym.OR
	else:
		_not(sen.left, claims)
		sen.sym = Sym.IMP
	return True

# requires global 'senlist'
def tautcomp(sen, claims):
	print("- tautcomp")
	global senlist
	other = sencopy(choice(senlist), claims)
	sen.left = other
	sen.right = sencopy(other, claims)
	rand = randint(0,2)
	if rand == 0:
		sen.sym = Sym.OR
		_not(sen.left, claims)
	elif rand == 1:
		sen.sym = Sym.IMP
	sen.sym = Sym.IFF
	return True

def contcomp(sen, claims):
	print("- contcomp")
	global senlist
	sen.left = sencopy(choice(senlist), claims)
	sen.right = sencopy(sen.left, claims)
	_not(sen.left, claims)
	sen.sym = Sym.AND
	return True

	# include Imp ???		<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

def ident(sen, claims):
	print("- ident")
	rand = randint(0,3)
	sen.left = Sentence(sen.sym, sen.left, sen.right)
	claims.add(sen.left)
	if rand == 0:
		sen.right = T()
		sen.sym = Sym.AND
	elif rand == 1:
		sen.right = F()
		sen.sym = Sym.OR
	elif rand == 2:
		sen.sym = Sym.IMP
		if randint(0,1):
			sen.right = T()
		else:
			_not(sen.left, claims)
			sen.right = F()
	else:
		rand = randint(0,1)
		sen.sym = Sym.IFF
		if rand == 0:
			sen.right = T()
		else:
			_not(sen.left, claims)
			sen.right = F()
	claims.add(sen.right)
	return True

# requires global 'senlist'
def tautannih(sen, claims):
	print("- tautannih")
	global senlist
	rand = randint(0,2)
	other = sencopy(choice(senlist), claims)
	if rand == 0:
		sen.left = T()
		claims.add(sen.left)
		sen.right = other
		sen.sym = Sym.OR
	elif rand == 1:
		sen.right = T()
		claims.add(sen.right)
		sen.left = other
		sen.sym = Sym.IMP
	else:
		sen.right = other
		sen.left = F()
		claims.add(sen.left)
		sen.sym = Sym.IMP
	return True

def contannih(sen, claims):
	print("- contannih")
	global senlist
	rand = randint(0,2)
	other = sencopy(choice(senlist), claims)
	if rand == 0:
		sen.left = other
		sen.right = F()
		claims.add(sen.right)
		sen.sym = Sym.AND
	elif rand == 1:
		sen.sym = Sym.NOT
		sen.arg = Imp(other, T())
		claims.add(sen.arg)
		claims.add(sen.arg.right)
	else:
		sen.sym = Sym.NOT
		sen.arg = Imp(F(), other)
		claims.add(sen.arg)
		claims.add(sen.arg.left)
	return True

def tautinv(sen, claims):
	print("- tautinv")
	sen.sym = Sym.NOT
	sen.arg = F()
	claims.add(sen.arg)
	return True

def continv(sen, claims):
	print("- continv")
	sen.sym = Sym.NOT
	sen.arg = T()
	claims.add(sen.arg)
	return True

def impl(sen, claims):
	print("- impl")
	sen.sym = Sym.IMP
	if randint(0,1):
		_not(sen.left, claims)
	else:
		sen.left, sen.right = _not(sen.right, claims), sen.left
	return True

#prob best not to implement
#def andequiv(sen, claims):
	
#def orequiv(sen, claims):

def contra(sen, claims):
	print("- contra")
	sen.left, sen.right = _not(sen.right, claims), _not(sen.left, claims)
	return True

def _impexp(sen, claims):
	if sen.right.sym != Sym.IMP:
		return False
	temp = sen.right.right
	sen.right.right = sen.left
	sen.left = sen.right
	sen.right = temp
	return True

def _andexp(sen, claims):
	if sen.left.sym != Sym.AND:
		return False
	temp = sen.left.left
	sen.left.left = sen.right
	sen.right = sen.left
	sen.left = temp
	return True

def exp(sen, claims):
	print("- exp")
	if randint(0,1):
		ret = _impexp(sen, claims)
		return ret if ret else _andexp(sen, claims)
	ret = _andexp(sen, claims)
	return ret if ret else _impexp(sen, claims)

def andred(sen, claims):
	print("- andred")
	sen.right = Sentence(None, sencopy(sen.left, claims), sen.right)
	claims.add(sen.right)
	rand = randint(0,2)
	if rand == 0:
		sen.right.sym = Sym.OR
		_not(sen.right.left, claims)
	elif rand == 1:
		sen.right.sym = Sym.IMP
	else:
		sen.right.sym = Sym.IFF
	return True

def orred(sen, claims):
	print("- orred")
	rand = randint(0,1)
	if rand == 0:
		sen.right = And(sencopy(sen.left, claims), sen.right)
		claims.add(sen.right)
		_not(sen.right.left, claims)
	elif rand == 1:
		sen.left = And(sencopy(sen.right, claims), sen.left)
		claims.add(sen.left)
		_not(sen.left.left, claims)
	return True

def knikna(sen, claims):
	print("- knikna")
	if randint(0,1):
		sen.right = And(sencopy(sen.left, claims), sen.right)
		claims.add(sen.right)
		sen.sym = Sym.IFF
	else:
		sen.left = Or(sencopy(sen.right, claims), sen.left)
		claims.add(sen.left)
		sen.sym = Sym.IFF
	return True

# requires global 'senlist'
def absorb(sen, claims):
	print("- absorb")
	global senlist
	other = sencopy(choice(senlist), claims)
	sen.left = Sentence(sen.sym, sen.left, sen.right)
	claims.add(sen.left)
	rand = randint(0,1)
	if rand == 0:
		sen.right = Or(sencopy(sen.left, claims), other)
		claims.add(sen.right)
		sen.sym = Sym.AND
	elif rand == 1:
		sen.right = And(sencopy(sen.left, claims), other)
		claims.add(sen.right)
		sen.sym = Sym.OR
	return True

# requires global 'senlist'
def adj(sen, claims):
	print("- adj")
	global senlist
	other = sencopy(choice(senlist), claims)
	temp = Sentence(sen.sym, sen.left, sen.right)
	claims.add(temp)
	if randint(0,1):
		sen.sym = Sym.AND
		sen.left = Or(temp, other)
		claims.add(sen.left)
		sen.right = Or(sencopy(temp, claims), sencopy(other, claims))
		claims.add(sen.right)
		_not(sen.right.right, claims)
	else:
		sen.sym = Sym.OR
		sen.left = And(temp, other)
		claims.add(sen.left)
		sen.right = And(sencopy(temp, claims), sencopy(other, claims))
		claims.add(sen.right)
		_not(sen.right.right, claims)
	return True

def dneg(sen, claims):
	print("- dneg")
	if sen.arg.sym != Sym.NOT:
		return False
	claims.remove(sen.arg)
	claims.remove(sen.arg.arg)
	sen.sym, sen.left, sen.right = sen.arg.arg.sym, sen.arg.arg.left, sen.arg.arg.right
	return True

andrules = [assoc, comm, andneg, aodist, andred]
orrules = [assoc, comm, orneg, aodist, orred, impl]
notrules = [dneg]
#impneg
imprules = [impdist, contra, exp, knikna]
iffrules = [assoc, comm, iffneg]
tautrules = [tautcomp, tautannih, tautinv]
contrules = [contcomp, contannih, continv]
varrules = [idem, ident, absorb, adj]

rules = {
	Sym.AND: andrules,
	Sym.OR: orrules,
	Sym.NOT: notrules,
	Sym.IMP: imprules,
	Sym.IFF: iffrules,
	Sym.TAUT: tautrules,
	Sym.CONT: contrules,
	Sym.VAR: varrules
}

def op(sen, claims):
	symrules = rules[sen.sym]
	for i in range(3):
		rule = choice(symrules)
		if rule(sen, claims):
			if None in claims:
				print("sym: {}".format(str(sen.sym)))
				print("rule: {}".format(str(symrules.index(rule))))
				print("sen: {}".format(str(sen)))
				print("claims: {}".format(str(claims)))
				raise Exception
			return True
	return False
