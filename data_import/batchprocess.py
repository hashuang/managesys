# -*- coding: utf-8 -*-
import json

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, StreamingHttpResponse, Http404
import numpy as np
import pandas as pd
from sklearn import preprocessing, linear_model
from openpyxl import Workbook

from . import models

from .zhuanlu import PRO_BOF_HIS_ALLFIELDS
from QinggangManageSys.settings import MAIN_OUTFIT_BASE,MEDIA_ROOT,MEDIA_URL

# def load(request):
#     if not request.user.is_authenticated():
#         return HttpResponseRedirect("/login")
#     contentVO={
#         'title':'数据分析工具',
#         'state':'success'
#     }
#     return render(request, 'data_import/analysis_tool.htm',contentVO)

def relation_ana(request):
    if not request.user.is_authenticated():
            return HttpResponseRedirect("/login")
    contentVO={
        'title':'数据分析工具——关联性分析',
        'state':'success'
    }

    return HttpResponse(json.dumps(contentVO), content_type='application/json')
def data_cleaning(data):
    return data.fillna(0)

def linear_regression_model(data):
    cols = list(data.columns)
    length_cols = len(cols)
    features = cols[:-1]
    out = cols[-1]

    data_array = np.array(data)
    scale_data_array = preprocessing.scale(data_array)
    data_scale_df = pd.DataFrame(scale_data_array,columns=cols)

    X_scale = data_scale_df[features]
    Y_scale = data_scale_df[out]

    regr = linear_model.LinearRegression()
    regr.fit(X_scale, Y_scale)

    return regr.coef_, regr.intercept_

def regression(output,selected_eles,db_table_name):
    """
    @param output 回归应变量 str
    @param selected_eles 回归自变量list
    @param db_table_name 存储回归结果的表
    @rtn coef 与selected_eles对应的回归系数list
    @rtn intercep 回归方程截距
    """
    sqlVO = {"db_name": 'l2own'}
    sql = 'SELECT ' + ', '.join(selected_eles) + ', ' + output + ' from QG_USER.PRO_BOF_HIS_ALLFIELDS'
    sqlVO["sql"] = sql
    rs = models.BaseManage().direct_select_query_orignal_sqlVO(sqlVO)

    data_ready = data_cleaning(pd.DataFrame(list(rs)))
    #i'm supposed to use scale method to reduce the impact of the differ of magnitude.
    coef, intercept = linear_regression_model(data_ready)
    coef = list(map(lambda x: str(x), coef))
    # save result to database
    for i in range(len(selected_eles)):
        sql = 'insert into QG_USER.%s values(\'%s\', \'%s\', \'%s\')'%(db_table_name, output, selected_eles[i], coef[i])
        sqlVO['sql'] = sql
        models.BaseManage().direct_execute_query_sqlVO(sqlVO)
    sql = 'insert into QG_USER.%s values(\'%s\', \'BIAS\', \'%s\')'%(db_table_name, output, str(intercept))
    sqlVO['sql'] = sql
    models.BaseManage().direct_execute_query_sqlVO(sqlVO)
    return coef, intercept

def regression_ana(result):
    pass


def report(request):
    if not request.user.is_authenticated():
            return HttpResponseRedirect("/login")
    contentVO={
        'title':'数据分析工具——生成分析结果报表',
        'state':'success'
    }
    db_table_names = {
        '321':"relation_cof_output_middle",
        '311':"relation_cof_output_input",
        '211':"relation_cof_middle_input",
        '322':"regression_cof_output_middle",
        '312':"regression_cof_output_input",
        '212':"regression_cof_middle_input",
    }
    sheetnames = {
        "relation_cof_output_middle":"相关系数_输出-控制",
        "relation_cof_output_input":"相关系数_输出-输入",
        "relation_cof_middle_input":"相关系数_控制-输入",
        "regression_cof_output_middle":"回归系数_输出-控制",
        "regression_cof_output_input":"回归系数_输出-输入",
        "regression_cof_middle_input":"回归系数_控制-输入",
    }
    entrance = [(3,2,1) ,(3,1,1), (2,1,1), (3,2,2) ,(3,1,2), (2,1,2)]

    import uuid
    filename = '相关性_回归分析汇总%s.xlsx' % str(uuid.uuid1())
    save_filename = MEDIA_ROOT + '/' + filename
    print(save_filename)
    contentVO['filepath'] = MEDIA_URL + filename
    wb = Workbook()
    i = 0
    for tags in entrance:
        tablekey = '%s%s%s' % tags
        table_name = db_table_names[tablekey]
        if i == 0:
            ws = wb.active
            ws.title = sheetnames[table_name]
            i += 1
        else:
            ws = wb.create_sheet(sheetnames[table_name])

        sql = 'SELECT * FROM QG_USER.%s' % table_name.upper()
        sqlVO = dict()
        sqlVO["db_name"] = "l2own"
        sqlVO["sql"] = sql

        rs = models.BaseManage().direct_select_query_orignal_sqlVO(sqlVO)
        rs_df = pd.DataFrame(list(rs))

        #sorted by column 1 and 3
        cols = list(rs_df.columns)
        rs_df['abs'] = rs_df[cols[2]].map(lambda x: abs(float(x)))
        # fout_sort = open('sort.txt', 'w+',encoding='utf-8')
        rs_df = rs_df.sort_values(by=[cols[0],'abs'],ascending=False)
        for ind in rs_df.index:
            temp = tuple(rs_df.loc[ind,cols])
            keyA, keyB, value = temp
            keyB = keyB.strip()
            if keyB == 'BIAS':
                nameB = "偏离-截距"
            else:
                nameB = PRO_BOF_HIS_ALLFIELDS[keyB]
            ws.append((PRO_BOF_HIS_ALLFIELDS[keyA.strip()], nameB, value))
            # fout_sort.write('%s,%s,%s\n'% tuple(rs_df.loc[ind,cols]))
        # fout_sort.close()
    print(save_filename)
    wb.save(save_filename)
    return HttpResponse(json.dumps(contentVO), content_type='application/json')
