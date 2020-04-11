from sentences import *
from rules import *
from random import choice
from random import randint
from copy import copy
from seqset import Seqset

names = ["Tom", "Bob", "Mary", "Joe", "Lucy", "Tim", "Jerry", "Paul", "Karen", "Fill", "Jessie"]

numvars = 4
varlist = [] # list of vars which represent characters
ids = {} # truth value assigned to vars
senlist = [] # list of all sentences ever, except cont and taut
claims = {} # active sentences associated with vars
finalclaims = {}

for i in range(numvars):
	name = choice(names)
	names.remove(name)
	newVar = Var(name)
	varlist.append(newVar)
	ids[newVar] = T() if randint(0,1) else F()
	senlist.append(newVar)
	claims[newVar] = Seqset([ids[newVar]])
	finalclaims[newVar] = ids[newVar]

setsenlist(senlist)

print(finalclaims)
print("-" * 10)

maxsenlen = 3

numcyc = 10
def cyc():
	for i in range(numcyc):
		v = choice(varlist)
		vclaims = claims[v]
		if len(vclaims) >= maxsenlen:
			print("skip")
			continue
		c = choice(vclaims)
		op(c, vclaims)
		print(finalclaims)

cyc()
print("done")
print("---------------------------\n")
print(finalclaims)
