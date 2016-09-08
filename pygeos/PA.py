#!/usr/bin/env python
__author__ = "Eric Daniels"

# -*- coding: utf-8 -*-
# @Author: edaniels
# @Date:   2015-10-08 10:50:11
# @Last Modified by:   edaniels
# @Last Modified time: 2016-03-18 08:30:14

"""
This module is intended to capture common predictive analytics workflows 
"""

import matplotlib.pyplot as plt
import matplotlib.style as style
import matplotlib.cm as cm
import pandas as pd 
import pygslib as gs
from sklearn.neighbors import KDTree
from sklearn.ensemble import RandomForestClassifier as RF
import numpy as np 

#def NearestNeighbor(inputPts, searchPts):
#	"""
#	Function for finding nearest neighbor within same dataset or different
#
#	Args:
#		inputPts: Pandas DataFrame including X and Y columns
#		searchPts: Pandas DataFrame to search for neighboring points including X and Y columns
#
#	Returns:
#		(Pandas DataFrame): Input points
#	"""


def zscore(inputDF):
	"""
	Return a DataFrame of Zscore values

	Args:
		inputDF: Pandas Dataframe of values to be returned as zscore 

	Returns: 
	"""
	zscore = (DF - DF.mean())/DF.std()
	return zscore


	def RandomForest(TrainingData, TrainingResults, TestData, n_estimators=1000):
		"""
		Returns test data with additional column of 'predicted' results

		Args:
			TrainingData: Pandas DataFrame for training RandomForest
			TrainingResults: Column or Series of known results for training data
			TestData: Pandas DataFrame with same column names as TrainingData 
			n_estimators: number of 'trees' used to estimate. Default is 1000.

		Returns:
			(Tuple): 
			|  DataFrame with TestData and additional column of predictions
			|  DataFrame of Relative Variable Importance
		"""

		#create RandomForest
		clf = RF(n_estimators=n_estimators)

		#train RandomForest
		clf.fit(TrainingData, TrainingResults)

		#predict
		predictions = clf.predict(TestData)
		predictions = pd.DataFrame(predictions, columns = ['Predicted'])
		
		#join with test data
		Testwithpred = TestData.join(predictions)

		#get feature importance
		importances = pd.DataFrame(clf.feature_importances_, names=TestData.columns)

		return Testwithpred, importances