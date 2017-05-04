import threading


class my_hread(threading.Thread):
	def __init__(self, i):
		threading.Thread.__init__(self)
		self.i = i

	def add(self):
		self.i += 1
		print self.i

	def run(self):
		self.add()


if __name__ == "__main__":
	t1 = my_hread(10)
	t2 = my_hread(10)
	t1.start()
	t2.start()
