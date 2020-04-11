
class Seqset:
	def __init__(self, items=[]):
		self.idxs = {}
		self.items = [i for i in items]

	def add(self, item):
		if item in self.idxs:
			return
		self.idxs[item] = len(self.items)
		self.items.append(item)

	def remove(self, item):
		idx = self.idxs.pop(item, -1)
		if idx < 0:
			return
		swap = self.items.pop()
		if swap is item:
			return
		self.items[idx] = swap
		self.idxs[swap] = idx

	def __getitem__(self, idx):
		return self.items[idx]
	
	def __delitem__(self, idx):
		self.remove(self.items[idx])

	def __len__(self):
		return len(self.items)
	
	def __iter__(self):
		return self.items.__iter__()
	
	def __contains__(self, item):
		return item in self.idxs
	
	def choice(self):
		import random
		return random.choice(self.items)
	
	def __str__(self):
		if len(self) == 0:
			return "{}"
		s = "{" + repr(self[0])
		for i in range(1, len(self)):
			s += ", " + repr(self[i])
		s += "}"
		return s
	
	def __repr__(self):
		return str(self)
