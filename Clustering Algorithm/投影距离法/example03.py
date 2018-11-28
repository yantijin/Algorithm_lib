import proclus as prc
import plotter
import arffreader as ar
import numpy as np
import adjrand

X, sup = ar.readarff("data/subspace_stream.arff")

Dims = [0, 3]
# plotter.plotDataset(X, D = Dims)

R = 1 # toggle run proclus
RS = 0 # toggle use random seed

if R: # run proclus
	rseed = 489132
	if RS:
		rseed = np.random.randint(low = 0, high = 1239831)

	print "Using seed %d" % rseed

	M, D, A = prc.proclus(X, k = 4, l = 2, seed = rseed, A = 30, B = 5)
	print "Accuracy: %.4f" % prc.computeBasicAccuracy(A, sup)
	adj = adjrand.computeAdjustedRandIndex(A, sup)
	print "Adjusted rand index: %.4f" % adj

	plotter.plotClustering(X, M, A, D = Dims)