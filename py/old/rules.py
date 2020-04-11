from sentences import *
from copy import copy
from random import randint, choice

def _not(sen):
	return copy(sen.arg) if sen.sym == Sym.NOT else Not(sen)

def _lassoc(sen):
	if sen.left.sym == sen.sym:
		return Biop(sen.sym, sen.left.left, Biop(sen.sym, sen.left.right, sen.right))
	return None

def _lassoc(sen):
	if sen.sym == sen.right.sym:
		return Biop(sen.sym, Biop(sen.left, sen.right.left), sen.right.right)
	return None

def assoc(sen):
	if randint(0,1):
		ret = _lassoc(sen)
		return ret if ret else _rassoc(sen)
	ret = _rassoc(sen)
	return ret if ret else _lassoc(sen);

def comm(sen):
	return Biop(sen.sym, sen.right, sen.left)

def _aoneg(sen, op):
	return Not(op(_not(sen.left), _not(sen.right)))

def andneg(sen):
	return _aoneg(sen, Or)

def orneg(sen):
	return _aoneg(sen, And)

def impneg(sen):
	return Not(And(sen.left, _not(sen.right)))

#def _ixneg(sen, curop, oop):
#	rand = randint(0,3)
#	if rand == 0:
#		return Not(oop(sen.left, sen.right))
#	if rand == 1:
#		return Not(curop(_not(sen.left), sen.right))
#	if rand == 2
#		return Not(curop(sen.left, _not(sen.right)))
#	return  curop(_not(sen.left), _not(sen.right))

def iffneg(sen):
#	return _ixneg(sen, Iff, Xor)
	rand = randint(0,2)
	if rand == 0:
		return Not(Iff(_not(sen.left), sen.right))
	if rand == 1:
		return Not(Iff(sen.left, _not(sen.right)))
	return  Iff(_not(sen.left), _not(sen.right))

#def xorneg(sen):
#	return _ixneg(sen, Xor, Iff)

def _ldist(sen):
	if (sen.left.sym != Sym.AND and sen.left.sym != Sym.OR) or sen.left.sym == sen.sym:
		return None
	return Biop(sen.left.sym, Biop(sen.sym, sen.left.left, sen.right), Biop(sen.sym, sen.left.right, sen.right))

def _rdist(sen):
	if (sen.right.sym != Sym.AND and sen.right.sym != Sym.OR) or sen.right.sym == sen.sym:
		return None
	return Biop(sen.right.sym, Biop(sen.sym, sen.left, sen.right.left), Biop(sen.sym, sen.left, sen.right.right))

def aodist(sen):
	if randint(0,1):
		ret = _ldist(sen)
		return ret if ret else _rdist(sen)
	ret = _rdist(sen)
	return ret if ret else _ldist(sen)

def impdist(sen):
	if randint(0,1):
		ret = _rdist(sen)
		if ret:
			return ret
		ret = _ldist(sen)
		ret.sym = Sym.AND if ret.sym == Sym.OR else Sym.OR
		return ret
	ret = _ldist(sen)
	if ret:
		ret.sym = Sym.AND if ret.sym == Sym.OR else Sym.OR
		return ret
	return _rdist(sen)

def idem(sen):
	rand = randint(0,2)
	if rand == 0:
		return And(sen, sen)
	if rand == 1:
		return Or(sen, sen)
	return Imp(_not(sen), sen)

def tautcomp(senlist):
	sen = choice(senlist)
	rand = randint(0,3)
	if rand == 0:
		return Or(_not(sen), sen)
	if rand == 1:
		return Or(sen, _not(sen))
	if rand == 2:
		return Imp(sen, sen)
	return Iff(sen, sen)

def contcomp(senlist):
	sen = choice(senlist)
	rand = randint(0,2)
	if rand == 0:
		return And(_not(sen), sen)
	if rand == 1:
		return And(sen, _not(sen))
	return iffneg(Iff(sen, sen))
	# include Imp ???		<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

def ident(sen):
	rand = randint(0,3)
	if rand == 0:
		if randint(0,1):
			return And(T, sen)
		return And(sen, T)
	if rand == 1:
		if randint(0,1):
			return Or(F, sen)
		return Or(sen, F)
	if rand == 2:
		if randint(0,1):
			return Imp(sen, T)
		return Imp(_not(sen), F)
	rand = randint(0,3)
	if rand == 0:
		return Iff(sen, T)
	if rand == 1:
		return Iff(T, sen)
	if rand == 2:
		return Iff(_not(sen), F)
	return Iff(F, _not(sen))

def tautannih(senlist):
	rand = randint(0,3)
	sen = choice(senlist)
	if rand == 0:
		return Or(sen, T)
	if rand == 1:
		return Or(T, sen)
	if rand == 2:
		return Imp(sen, T)
	return Imp(F, sen)

def contannih(senlist):
	rand = randint(0,3)
	sen = choice(senlist)
	if rand == 0:
		return And(sen, F)
	if rand == 1:
		return And(F, sen)
	# want this?????		<<<<<<<<<<<<<<<<<<<<<<<<
	if rand == 2:
		return Not(Imp(sen, T))
	return Not(Imp(F, sen))

def tautinv(senlist):
	return Not(F)

def continv(senlist):
	return Not(T)

def impl(sen):
	if randint(0,1):
		return Imp(_not(sen.left), sen.right)
	return Imp(_not(sen.right), sen.left)

#prob best not to implement
#def andequiv(sen):
	
#def orequiv(sen):

def contra(sen):
	return Imp(_not(sen.right), _not(sen.left))

def _impexp(sen):
	if sen.right.sym != Sym.IMP:
		return None
	return Imp(And(sen.left, sen.right.left), sen.right.right)

def _andexp(sen):
	if sen.left.sym != Sym.AND:
		return None
	return Imp(sen.left.left, Imp(sen.left.right, sen.right))

def exp(sen):
	if randint(0,1):
		ret = _impexp(sen)
		return ret if ret else _andexp(sen)
	ret = _andexp(sen)
	return ret if ret else _impexp(sen)

def andred(sen):
	rand = randint(0,1)
	if rand == 0:
		rand = randint(0,3)
		if rand == 0:
			return And(sen.left, Or(_not(sen.left), sen.right))
		if rand == 1:
			return And(sen.left, Or(sen.right, _not(sen.left)))
		if rand == 2:
			return And(Or(sen.left, _not(sen.right)), sen.right)
		return And(Or(_not(sen.right), sen.left), sen.right)
	if rand == 1:
		rand = randint(0,3)
		if rand == 0:
			return And(sen.left, Imp(sen.left, sen.right))
		if rand == 1:
			return And(Imp(sen.right, sen.left), sen.right)
		if rand == 2:
			return And(sen.right, Imp(_not(sen.left), _not(sen.right)))
		return And(Imp(_not(sen.right), _not(sen.left)), sen.left)
	rand = randint(0,3)
	if rand == 0:
		return And(sen.left, Iff(sen.left, sen.right))
	if rand == 1:
		return And(Iff(sen.left, sen.right), sen.right)
	if rand == 2:
		return And(sen.left, Iff(_not(sen.left), _not(sen.right)))
	return And(Iff(_not(sen.left), _not(sen.right)), sen.right)

def orred(sen):
	rand = randint(0,3)
	if rand == 0:
		return Or(sen.left, And(_not(sen.left), sen.right))
	if rand == 1:
		return Or(sen.left, And(sen.right, _not(sen.left)))
	if rand == 2:
		return Or(And(sen.left, _not(sen.right)), sen.right)
	return Or(And(_not(sen.right), sen.left), sen.right)

def knikna(sen):
	if randint(0,1):
		return Iff(sen.left, And(sen.left, sen.right))
	return Iff(sen.right, Or(sen.right, sen.left))

def absorb(sen, senlist):
	psi = choice(senlist)
	rand = randint(0,3)
	if rand == 0:
		return And(sen, Or(sen, psi))
	if rand == 1:
		return And(sen, Or(psi, sen))
	if rand == 2:
		return Or(sen, And(sen, psi))
	return Or(sen, And(psi, sen))

def adj(sen, senlist):
	psi = choice(senlist)
	if randint(0,1):
		return And(Or(sen, psi), Or(sen, _not(psi)))
	return Or(And(sen, psi), And(sen, _not(psi)))

def dneg(sen):
	if sen.arg.sym != NOT:
		return None
	return copy(sen.arg.arg)

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

def op(sen, senlist):
	if sen.sym == TAUT or sen.sym == CONT:
		return choice(rules[sen.sym])(senlist)
	symrules = rules[sen.sym]
	for i in range(3):
		rule = choice(symrules)
		if rule == andred or rule == orred:
			ret = rule(sen, senlist)
		else:
			ret = rule(sen)
		if ret:
			return ret
	return sen
