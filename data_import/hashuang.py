def num_descibe(scrapy_records):
	frame=DataFrame(scrapy_records)
	df=frame.sort_values(by=bookno)
	dfr=df[df>0].dropna(how='any')
	clean=Wushu(dfr[bookno])
	if clean is not None:
		bc=(clean.max()-clean.min())/10
		bcq=math.ceil(bc*1000)/1000
		try:
			section=pd.cut(clean,(clean.max()-clean.min())/bcq)
			end=pd.value_counts(section,sort=False)/clean.count()
			describe=clean.describe()
		except ValueError:
		 	pass
	numx=[ele for ele in end.index]
	numy=[ele for ele in end]
	desx=[ele for ele in describe.index]
	desy=[ele for ele in describe]
	numy1=["%.2f%%"%(n*100) for n in numy]
	#List=clean.describe()
	#List1=map(str,numx)
	#List2=map(str,end)
	
	ana_result={}
	#ana_result['scope']=['(1256.303, 1276.15]','(1276.15, 1295.8]','(1295.8, 1315.45]']
	#ana_result['num']=[0.01897,0.034812,0.048201]
	ana_result['scope']=numx
	ana_result['num']=numy
	contentVO['result']=ana_result
	ana_describe={}
	ana_describe['scopeb']=desx
	ana_describe['numb']=desy
	return ana_result,ana_describe