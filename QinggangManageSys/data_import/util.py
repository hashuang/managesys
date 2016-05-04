import openpyxl



def get_model_attrs(model):
	attrs_str= model.__doc__
	attrs_str=attrs_str[attrs_str.index('(')+1:attrs_str.index(')')]
	attrs_list=attrs_str.split(',')
	attrs_list_final=[]
	for each in attrs_list:
		if each.endswith("_ptr") or each=='id':
			continue
		each=each.strip(' ')
		attrs_list_final.append(each)
	print(attrs_list_final)
	return attrs_list_final


def batch_import_data(path,model):
	attrs = get_model_attrs(model)
	entities=[]
	#records=model.objects.get_all_tr()
	wb2 = openpyxl.load_workbook(path)
	sheet_names = wb2.get_sheet_names()
	ws = wb2[sheet_names[0]]
	j=1
	entity={}
	for row in ws.rows:
		if(j==1):
			entity["own_uid"]=row[j].value
			j+=1
			continue
		elif(j==2):
			j+=1
			continue
		print(row)
		for i in range(len(row)):
			print('{0}:{1}'.format(attrs[i+1],row[i].value))
			entity[attrs[i+1]]=row[i].value
		print(entity)
		entities.append(entity)
		entity={}
	print(entities)
	for entity in entities:
		#m=model(uid='1',own_col='entity')
		m=model()
		m.set_attr(attr = entity)
		#print(m.own_col)
		m.save()


def create_insert_sql(model,dictVO):
	pass


def create_update_sql(model,dictVO):
	pass


def create_delete_sql(model,dictVO):
	pass