import numpy as np
from keras.utils import np_utils
from generateWordVectors import preprocess_text

def question2VecTimeSeries(word_vectors, q, featureDim, maxLen):
	
	outputvec = np.zeros((maxLen, featureDim))
	'''
	doc = nlp(q)
	for i in xrange(len(doc)):
		if i<maxLen:
			outputvec[i, :] = doc[i].vector
	'''
	return outputvec

def question2VecSum(word_vectors, q, featureDim):
	outputvec = np.zeros((featureDim,))
	words = preprocess_text(q)

	for i in xrange(len(words)):
		try:
			outputvec += word_vectors[words[i]]
		except:
			pass
	
	return outputvec

def computeVectors(qu,an,img,VGGfeatures,word_vectors,img_map,encoder,nb_classes):
	features = np.zeros((1,4096+300))
	
	features[0,0:300] = question2VecSum(word_vectors,qu,300)
	features[0,300:] = VGGfeatures[:,img_map[img]]

	return features

def computeVectorsTimeSeries(qu,an,img,VGGfeatures,word_vectors,img_map,encoder,nb_classes, maxLen):
	featureDim = 300
	img_dim = 4096
	features_q = np.zeros((1, maxLen, featureDim))
	features_i = np.zeros((1, img_dim))

	features_q[0,:,:] = question2VecSum(word_vectors,qu,300)
	features_i[0,:] = VGGfeatures[:,img_map[img]]

	return features_i,features_q


def computeVectorsBatch(qu,an,img,VGGfeatures,word_vectors,img_map,encoder,nb_classes):
	word2vecDim = 300
	img_dim = VGGfeatures.shape[0]
	features = np.zeros((len(qu),img_dim+word2vecDim))
	for i in xrange(len(qu)):
		features[i,:word2vecDim] = question2VecSum(word_vectors,qu[i],word2vecDim)
		features[i,word2vecDim:] = VGGfeatures[:,img_map[img[i]]]

	y = encoder.transform(an)
	Y = np_utils.to_categorical(y, nb_classes)

	return (features, Y)

def computeVectorsBatchTimeSeries(qu, an, img, VGGfeatures,img_map, word_vectors, encoder, nb_classes, maxLen):
	featureDim = 300
	img_dim = VGGfeatures.shape[0]
	
	features_q = np.zeros((len(qu), maxLen, featureDim))
	features_i = np.zeros((len(qu), img_dim))
	for i in xrange(len(qu)):
		features_q[i,:,:] = question2VecTimeSeries(word_vectors, qu[i], featureDim, maxLen)
		features_i[i,:] = VGGfeatures[:,img_map[img[i]]]

	y = encoder.transform(an)
	Y = np_utils.to_categorical(y, nb_classes)
	return (features_i, features_q, Y)
