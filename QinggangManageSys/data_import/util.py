import openpyxl

def get_primary_key(model):
    primary_key=None
    attrs_fields= model._meta.fields
    for field in attrs_fields:
        if field.primary_key:
            primary_key=field.attname
    return primary_key

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
	own_uid=''
	for row in ws.rows:
		if(j==1):
			own_uid=row[j].value
			j+=1
			continue
		elif(j==2):
			j+=1
			continue
		print(row)
		entity['own_uid']=own_uid
		for i in range(len(row)):
			#print('{0}:{1}'.format(attrs[i+1],row[i].value))
			entity[attrs[i+1]]=row[i].value
		entities.append(entity)
		entity={}
	print(entities)
	for entity in entities:
		m=model()
		m.set_attr(attr = entity)
		m.save()

		
#通过传值的dictVO拼接成条件传入即‘SELECT * FROM WHERE ** and **’
def create_select_condition(dictVO):
	result={}
	varlist=[]
	whereCondition=" where "
	for each in dictVO:
		whereCondition+=each+'=:'+each+' and '
		varlist.append(dictVO[each])
	whereCondition=whereCondition[:len(whereCondition)-1]+')'
	print('{0}'.format(whereCondition))
	result['whereCondition']=whereCondition
	result['vars']=varlist
	return result

def create_select_sqlVO(model,dictVO):
	condition = create_select_condition(dictVO)
	whereCondition=condition.get('whereCondition')
	if(model!=None):
		table_name = model._meta.db_table
	sql ='SELECT * INTO '+table_name+whereCondition
	print(sql)
	return {'sql':sql,'vars':condition.get('vars')}



def create_insert_condition(dictVO):
	result={}
	varlist=[]
	columnCondition=" ("
	valueCondition=" ("
	for each in dictVO:
		columnCondition+=each+','
		ele = dictVO[each]
		if isinstance(ele,int) or isinstance(ele,float):
			valueCondition+='%s,'
		valueCondition+="'%s',"
		varlist.append(dictVO[each])
	columnCondition=columnCondition[:len(columnCondition)-1]+')'
	valueCondition=valueCondition[:len(valueCondition)-1]+')'
	result['columnCondition']=columnCondition
	result['valueCondition']=valueCondition
	result['vars']=varlist
	return result

def create_insert_sqlVO(model,dictVO):
	condition = create_insert_condition(dictVO)
	columnCondition=condition.get('columnCondition')
	valueCondition=condition.get('valueCondition')
	if(model!=None):
		table_name = model._meta.db_table
	sql ='INSERT INTO '+table_name+columnCondition+' VALUES'+valueCondition
	return {'sql':sql,'vars':condition.get('vars')}

#UODATE语句只能通过own_uid（即关联字段,同时也是每个表的主键字段）来更新
def create_update_condition(dictVO,primary_key):
	result={}
	varlist=[]
	setCondition=" "
	whereCondition=''
	for each in dictVO:
		if each==primary_key:
			whereCondition=' where '+each+'=:'+each
		setCondition+= each+'=:'+each+','
		varlist.append(dictVO[each])
	setCondition=setCondition[:len(setCondition)-1]
	result['setCondition']=setCondition
	result['whereCondition']=whereCondition
	result['vars']=varlist
	return result

def create_update_sqlVO(model,dictVO):
	primary_key=get_primary_key(model)
	condition=create_update_condition(dictVO,primary_key)
	whereCondition=condition.get('whereCondition')
	if(whereCondition==''):
		print('传入的属性没有提供主键属性，故无法更新')
		return
	setCondition=condition.get('setCondition')
	if(model!=None):
		table_name = model._meta.db_table
	sql='UPDATE '+table_name+' SET '+setCondition
	return {'sql':sql,'vars':condition.get('vars')}
#DELETE
def create_delete_condition(dictVO,primary_key):
	result={}
	varlist=[]
	whereCondition=''
	for each in dictVO:
		if each==primary_key:
			whereCondition=' where '+each+'=:'+each
			varlist.append(dictVO[each])
	result['whereCondition']=whereCondition
	result['vars']=varlist
	return result
#‘DELETE FROM TABBLE_NAME WHERE ’
def create_delete_sqlVO(model,dictVO):
	primary_key=get_primary_key(model)
	condition=create_update_condition(dictVO,primary_key)
	whereCondition=condition.get('whereCondition')
	if(whereCondition==''):
		print('传入的属性没有提供主键属性，故无法删除')
		return
	if(model!=None):
		table_name = model._meta.db_table
	sql='DELETE FROM '+table_name+ whereCondition
	return {'sql':sql,'vars':condition.get('vars')}
'''
我为oracle数据库专门写一个
'''
#INSERT
def create_ora_insert_condition(dictVO):
	result={}
	varlist=[]
	columnCondition=" ("
	valueCondition=" ("
	for each in dictVO:
		columnCondition+=each+','
		valueCondition+=":"+each+","
	columnCondition=columnCondition[:len(columnCondition)-1]+')'
	valueCondition=valueCondition[:len(valueCondition)-1]+')'
	result['columnCondition']=columnCondition
	result['valueCondition']=valueCondition
	result['vars']=dictVO
	return result

def create_ora_insert_sqlVO(model,dictVO):
	condition = create_ora_insert_condition(dictVO)
	columnCondition=condition.get('columnCondition')
	valueCondition=condition.get('valueCondition')
	if(model!=None):
		table_name = model._meta.db_table
	sql ='INSERT INTO '+table_name+columnCondition+' VALUES'+valueCondition
	return {'sql':sql,'vars':condition.get('vars')}
#SELECT
def create_ora_select_condition(dictVO):
	result={}
	varlist=[]
	whereCondition=" where "
	for each in dictVO:
		whereCondition+=each+'=:'+each+' and '
	whereCondition=whereCondition[:len(whereCondition)-5]
	print('{0}'.format(whereCondition))
	result['whereCondition']=whereCondition
	result['vars']=dictVO
	return result

def create_ora_select_sqlVO(model,dictVO):
	condition = create_ora_select_condition(dictVO)
	whereCondition=condition.get('whereCondition')
	if(model!=None):
		table_name = model._meta.db_table
	sql ='SELECT * FROM '+table_name+whereCondition
	print(sql)
	return {'sql':sql,'vars':condition.get('vars')}

	#update
def create_ora_update_condition(dictVO,primary_key):
	result={}
	varlist=[]
	setCondition=" "
	whereCondition=''
	print(primary_key)
	for each in dictVO:
		print(each)
		print(each==primary_key)
		if each==primary_key:
			whereCondition=' where '+each+'=:'+each
			continue
		setCondition+= each+'=:'+each+','
		varlist.append(dictVO[each])
	setCondition=setCondition[:len(setCondition)-1]
	result['setCondition']=setCondition
	result['whereCondition']=whereCondition
	result['vars']=dictVO
	return result

def create_ora_update_sqlVO(model,dictVO):
	primary_key=get_primary_key(model)
	condition=create_ora_update_condition(dictVO,primary_key)
	whereCondition=condition.get('whereCondition')
	if(whereCondition==''):
		print('传入的属性没有提供主键属性，故无法更新')
		return
	setCondition=condition.get('setCondition')
	if(model!=None):
		table_name = model._meta.db_table
	sql='UPDATE '+table_name+' SET '+setCondition+whereCondition
	return {'sql':sql,'vars':condition.get('vars')}

#DELETE
def create_ora_delete_condition(dictVO,primary_key):
	result={}
	varlist=[]
	whereCondition=''
	whereValue={}
	for each in dictVO:
		if each==primary_key:
			whereCondition=' where '+each+'=:'+each
			whereValue[each]=dictVO[each]
			continue
		
	result['whereCondition']=whereCondition
	result['vars']=whereValue
	return result
#‘DELETE FROM TABBLE_NAME WHERE ’
def create_ora_delete_sqlVO(model,dictVO):
	primary_key=get_primary_key(model)
	condition=create_ora_delete_condition(dictVO,primary_key)
	whereCondition=condition.get('whereCondition')
	if(whereCondition==''):
		print('传入的属性没有提供主键属性，故无法删除')
		return
	if(model!=None):
		table_name = model._meta.db_table
	sql='DELETE FROM '+table_name+ whereCondition
	return {'sql':sql,'vars':condition.get('vars')}



#由record和从自己设计的数据库里取出的数据own_uid去对应的数据库里取值并返回
def get_all_uid_sqlVO(record):
	sqlVO={}
	select_uid_sql = 'SELECT ' +record['FROM_UID'] +' FROM ' +record['FROM_TABLE']+' where rownum<10'
	db_name=record['FROM_SYSTEM'].lower()
	sqlVO={'sql':select_uid_sql,'db_name':db_name}
	return sqlVO


def get_value_by_uid_sqlVO(record,own_id):
	sqlVO={}
	select_uid_sql = 'SELECT ' +record['FROM_COL'] +' FROM ' +record['FROM_TABLE']+' where '+record['FROM_UID']+'='+own_id
	db_name=record['FROM_SYSTEM'].lower()
	sqlVO={'sql':select_uid_sql,'db_name':db_name}
	return sqlVO

def create_update_by_uid_sqlVO(dictVO):
	sqlVO={}
	#dictVO={'record':record,'value':insert_value,'table_name':table_name,'own_id':own_id}
	record=dictVO['record']
	select_uid_sql = 'UPDATE '+dictVO['table_name']+' SET ' +record['OWN_COL'] +'=:'+record['OWN_COL']+' WHERE '+ record['OWN_UID']+'='+dictVO['own_id']
	sqlVO={'sql':select_uid_sql,'vars':{record['OWN_COL']:dictVO['value'][0][record['OWN_COL'].upper()]}}
	return sqlVO


#多个数据组合到一起类型问题
def change_value_2_insert(value):
	return value