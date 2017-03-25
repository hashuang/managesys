# -*- coding:utf-8 -*-
import math
'''
scientific calculate packages
'''
import numpy as np
import pandas as pd
from sklearn.cross_validation import train_test_split
from sklearn import preprocessing
'''
ELM
'''
from data_import.SteelPricePredict.RegressionModels.ExtremeLM import elm_

class ExtremeLM(object):
    """docstring for ExtremeLM."""
    def __init__(self):
        super(ExtremeLM, self).__init__()
        print('ExtremeLM init')

    def log(self):
        print('ExtremeLM predict')
        return 'ExtremeLM predict'

    def predict(self,model_data,exnum):
        return elm_(model_data,exnum)



class SVM(object):
    """docstring for SVM."""
    def __init__(self):
        super(SVM, self).__init__()
        print('SVM:init')

    def log(self):
        print('SVM predict')
        return 'SVM predict'

    def predict(self,model_data,exnum):
    	return elm_(model_data,0.3)

class LR(object):
    """docstring for SVM."""
    def __init__(self):
        super(LR, self).__init__()
        print('LR:init')

    def log(self):
        print('LR predict')
        return 'LR predict'

    def predict(self,model_data,exnum):
    	return elm_(model_data,0.2)

class BP(object):
    """docstring for SVM."""
    def __init__(self):
        super(BP, self).__init__()
        print('BP:init')

    def log(self):
        print('BP predict')
        return 'BP predict'

    def predict(self,model_data,exnum):
    	return elm_(model_data,0.15)

class RandomForest(object):
    """docstring for SVM."""
    def __init__(self):
        super(RandomForest, self).__init__()
        print('RandomForest:init')

    def log(self):
        print('RandomForest predict')
        return 'RandomForest predict'

    def predict(self,model_data,exnum):
    	return elm_(model_data,0.25)

if __name__ == '__main__':
    ExtremeLM('hello')
