"""
@author: vsgarg
"""

import numpy
import math

def getMembershipValues(datapoints):
	inputFile = open('input/centers.data')
	beta = float(inputFile.readline())
	centers = []	

	for line in inputFile:
		(col1, col2, col3, col4, col5, col6, col7, col8, col9, col10, col11, col12) = line.split(',')
		centers.append(numpy.asarray([float(col1), float(col2), float(col3), float(col4), float(col5), float(col6), float(col7), float(col8), float(col9), float(col10), float(col11)]))

	centersCount = len(centers)
	numberOfPoints = len(datapoints)
	resultMU = []
	instanceMU = [0]*4
	dist = [0]*4
	denomSum = 0
	for i in range(numberOfPoints):
		for j in range(centersCount):
			dist[j] = numpy.linalg.norm(datapoints[i]-centers[j])
			dist[j] = math.pow(dist[j], 2)
			denomSum += (1/ (1 - math.exp(-beta * dist[j])))

		for j in range(len(centers)):
			numerator = (1 /(1 - math.exp(-beta * dist[j])))
			instanceMU[j] = numerator/denomSum

		denomSum = 0
		resultMU.append(instanceMU)
		
	return resultMU	  		


			