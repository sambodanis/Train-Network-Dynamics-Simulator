from util import *
from netClasses import *
import parsing
# import numpy as np
# import matplotlib.pyplot as plt


class State(object):
	"""docstring for State"""
	def __init__(self, ug):
		self.ug = ug
		self.trains = {}
		
	def add_train(self, train):

		self.trains[train] = (0.0, self.connect(train))
		# for s in self.trains:
		# 	print self.trains[s][1]

	def connect(self, train):
		return self.ug.get_connection(train.location, train.line, train.direction)

	def travel(self, time):
		for train in self.trains:
			time_taken = 0.0
			percent_done, curr_conn = self.trains[train]
			# print percent_done
			while True:
				if (1.0 - percent_done) * curr_conn._min_time + time_taken < time:
					# percent_done = 0.0 ## move below but fix self.connect crash
					time_taken += (1.0 - percent_done) * curr_conn._min_time
					# print time_taken, percent_done, curr_conn._min_time
					percent_done = 0.0
					train.location = curr_conn._end
					print train.location
					for c in self.ug[train.location]._connections:
						print c
					curr_conn = self.connect(train)
					if not curr_conn:
						train.reverse_direction()
						curr_conn = self.connect(train)
				else:
					percent_done = (time - time_taken) / curr_conn._min_time
					break
			self.trains[train] = (percent_done, curr_conn)
			time_taken = 0.0




def degree_distribution(ug):
	degs = sorted([len(ug[x]._connections) for x in ug.stations])
	return degs

def main():
	ug = parsing.load_underground()
	# for line in ug._lines:
	# 	print line
	# degrees = degree_distribution(ug)
	# freq = [0] * 10
	# degs = range(1, 11)
	# print freq
	# for i in degrees:
	# 	freq[i-1] += 1
	# plt.plot(degs, freq)
	# plt.show()


	# print ug.path('green_park', 'camden_town')
	s = State(ug)
	s.add_train(Train(1, 'burnt_oak', 'northern', 'northbound'))
	# s.add_train(Train(2, 'euston', 'northern', 'southbound'))
	s.travel(10)
	for train in s.trains:
		print s.trains[train][0], s.trains[train][1], train.id
	s.travel(10)
	for train in s.trains:
		print s.trains[train][0], s.trains[train][1]


	## Floyd Warshall method for reachability


if __name__ == '__main__':
	main()


