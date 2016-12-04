from pandas import DataFrame
from pandas import DataFrame
import pandas as pd
import numpy as np
import math

def Wushu(x):
    L=np.percentile(x,25)-1.5*(np.percentile(x,75)-np.percentile(x,25))
    U=np.percentile(x,75)+1.5*(np.percentile(x,75)-np.percentile(x,25))
    return x[(x<U)&(x>L)]	
def num(request):
	clean=Wushu(dfr[bookno])
	if clean is not None:
		bc=(clean.max()-clean.min())/10
		bcq=math.ceil(bc*1000)/1000
		try:
			section=pd.cut(clean,math.ceil((clean.max()-clean.min())/bcq+1))
			end=pd.value_counts(section,sort=False)/clean.count()
			describe=clean.describe()
		except ValueError as e:
		 	print(e)
	numx=[ele for ele in end.index]
	numy=[ele for ele in end]
	desx=[ele for ele in describe.index]
	desy=[ele for ele in describe]
	numy1=["%.2f%%"%(n*100) for n in numy]
	contentVO={
		'title':'测试',
		'state':'success'
	}
	ana_result={}
	ana_result['scope']=numx
	ana_result['num']=numy
	contentVO['result']=ana_result
	ana_describe={}
	ana_describe['scopeb']=desx
	ana_describe['numb']=desy
	contentVO['describe']=ana_describe
	return ana_result,ana_describe