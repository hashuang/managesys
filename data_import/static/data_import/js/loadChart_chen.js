// 正态分布
function drawBarChart_norm(result){
	var myChart = echarts.init(document.getElementById('main2'));
    var bookname=document.getElementById('bookno1')
        // 指定图表的配置项和数据
        var option = {
            title: {
                text: bookno = bookname.options[bookname.selectedIndex].text+result.fieldname+'的正态分布'+result.singleheat+','+result.singleheat_value+','+result.normy[result.singleheat_index]+result.offset_value,
                x:'center'
            },
            tooltip: {
                trigger: 'axis',
                axisPointer : {            // 坐标轴指示器，坐标轴触发有效
                    type : 'shadow'        // 默认为直线，可选为：'line' | 'shadow'
                 }
            },
            legend: {
                data:['']
            },
            xAxis: {
                data: result.normx,
                axisLabel :{  
                        //interval:0,//横轴信息全部显示
                        //rotate: 60//60度角倾斜显示  
                    } 
            },
            yAxis: {
                name:'Y'
            },
            series: [{
                name: '',
                type: 'bar',
                data: result.normy,
                markPoint: {
                    itemStyle : {
                         normal: {
                             color:'#1e90ff'
                         }
                     },
                    data:[
                            {type : 'max', name: '最大值'},
                            {type : 'min', name: '最小值'},
                            {name : '测试点'+'aaa', value : result.singleheat, xAxis: result.singleheat_value, yAxis: result.normy[result.singleheat_index]},
                            //{name : '测试点1', value : result.singleheat, xAxis: '97840.0000', yAxis: '0.0003'}
                    ]
                },
                // markLine: {
                //     name:'炉次号'+result.fieldname+'的标线'
                //     itemStyle : {
                //         normal: {
                //             color:'#1e90ff'
                //         }
                //     },
                //     data:[
                //             [
                //             {name: '标线1起点', value: result.singleheat, xAxis: result.singleheat, yAxis: 0},
                //             {name: '标线1终点', xAxis: result.singleheat, yAxis: 0.3}
                //             ]
                //            ] 
                    
                // }
                // itemStyle: {
                //         normal: {
                //         //color: 'tomato',
                //         //barBorderColor: 'tomato',
                //         barBorderWidth: 6,
                //         barBorderRadius:0,
                //         label : {
                //             show: true, position: 'top'
                //         }
                //     }
                // }

            },
              {
                name: '',
                type: 'line',
                data: result.normy
            }
            ]

        };

    // 使用刚指定的配置项和数据显示图表。
    myChart.setOption(option);
}

// 条形图（投入和产出）
function drawBarChart(result){
    var myChart = echarts.init(document.getElementById('main1'));
        // 指定图表的配置项和数据
        var option = {
            title: {
                text: '炉次号'+result.heat_no+'的'+result.attribute+'组成',
                x:'center'
            },
            tooltip: {
                trigger: 'axis',
                axisPointer : {            // 坐标轴指示器，坐标轴触发有效
                    type : 'shadow'        // 默认为直线，可选为：'line' | 'shadow'
                 }
            },
            legend: {
                data:['']
            },
            xAxis: {
                data: result.xname,
                axisLabel :{  
                        interval:0,//横轴信息全部显示
                        //rotate: 60//60度角倾斜显示  
                    } 
            },
            yAxis: {
                name:'Kg'
            },
            series: [{
                name: '投入量(Kg)',
                type: 'bar',
                data: result.yvalue,
                markPoint: {
                    data:[
                            {type : 'max', name: '最大值'},
                            {type : 'min', name: '最小值'}
                            //{name : '标记点测试', value : 100, xAxis: result.scope[1], yAxis: 0.2}  
                    ]
                },
                itemStyle: {
                    normal: {
                        //color: 'tomato',
                        //barBorderColor: 'tomato',
                        barBorderWidth: 6,
                        barBorderRadius:0,
                        label : {
                            show: true, position: 'top'
                        }
                    }
                }

            }
            ]

        };

    // 使用刚指定的配置项和数据显示图表。
    // myChart.setOption(option);
//--------------------------------------------------
   //var ecConfig = require('echarts/config');
   var ecConfig = echarts.config;  
    function eConsole(param) {
        var mes = '【' + param.type + '】';
        if (typeof param.seriesIndex != 'undefined') {
            mes += '  seriesIndex : ' + param.seriesIndex;
            mes += '  dataIndex : ' + param.dataIndex;
        }
        if (param.type == 'hover') {
            document.getElementById('hover-console').innerHTML = 'Event Console : ' + mes;
        }
        else {
            document.getElementById('console').innerHTML = mes;
        }
        console.log(param);
    }

    myChart.on(ecConfig.EVENT.CLICK, eConsole);
    myChart.on(ecConfig.EVENT.DBLCLICK, eConsole);
    //myChart.on(ecConfig.EVENT.HOVER, eConsole);
    myChart.on(ecConfig.EVENT.DATA_ZOOM, eConsole);
    myChart.on(ecConfig.EVENT.LEGEND_SELECTED, eConsole);
    myChart.on(ecConfig.EVENT.MAGIC_TYPE_CHANGED, eConsole);
    myChart.on(ecConfig.EVENT.DATA_VIEW_CHANGED, eConsole);
    myChart.setOption(option);
//------------------------------------------------------------
}

// 字段数据统计条形图（带标线）
function drawBarChart1(result){
    var myChart = echarts.init(document.getElementById('main1'));
        // 指定图表的配置项和数据
        var option = {
            title: {
                text: '字段数据统计概率直方图',
                x:'center'
            },
            tooltip: {},
            legend: {
                data:['']
            },
            xAxis: {
                data: result.scope
            },
            yAxis: {},
            series: [{
                name: '占比(%)',
                type: 'bar',
                data: result.num,
                markPoint: {
                    data:[
                            {type : 'max', name: '最大值'},
                            {type : 'min', name: '最小值'},
                            {name : '标记点', value : result.vvalue_y, xAxis: result.vvalue_x, yAxis:0.3}  
                    ]
                },
                markLine: {
                    itemStyle : {
                        normal: {
                            color:'#1e90ff'
                        }
                    },
                    data:[
                            [
                            {name: '标线1起点', value: result.vvalue_y, xAxis: result.vvalue_x, yAxis: 0},
                            {name: '标线1终点', xAxis: result.vvalue_x, yAxis: 0.3}
                            ]
                           ] 
                    
                }
            },
            {
                name: '',
                type: 'line',
                data: result.num
            }
            ]

        };

    // 使用刚指定的配置项和数据显示图表。
    myChart.setOption(option);
}

// 字段数据统计条形图
function drawBarChart2(result){
    var myChart = echarts.init(document.getElementById('main1'));
        // 指定图表的配置项和数据
        var option = {
            title: {
                text: '时间范围内字段数据统计概率直方图',
                x:'center'
            },
            tooltip: {},
            legend: {
                data:['']
            },
            xAxis: {
                data: result.scope
            },
            yAxis: {},
            series: [{
                name: '占比(%)',
                type: 'bar',
                data: result.num,
                markPoint: {
                    data:[
                            {type : 'max', name: '最大值'},
                            {type : 'min', name: '最小值'},
                            //{name : '标记点', value : result.vvalue_y, xAxis: result.vvalue_x, yAxis:0.3}  
                    ]
                },
            },
            {
                name: '',
                type: 'line',
                data: result.num
            }
            ]

        };

    // 使用刚指定的配置项和数据显示图表。
    myChart.setOption(option);
}
//折线图
function drawBrokenLineChart(data){
    var myChart = echarts.init(document.getElementById('main2'));

    

    option = {
        title: {
            text: '折线图堆叠'
        },
        tooltip: {
            trigger: 'axis'
        },
        legend: {
            data:['邮件营销','联盟广告','视频广告','直接访问','搜索引擎']
        },
        grid: {
            left: '3%',
            right: '4%',
            bottom: '3%',
            containLabel: true
        },
        toolbox: {
            feature: {
                saveAsImage: {}
            }
        },
        xAxis: {
            type: 'category',
            boundaryGap: false,
            data: ['周一','周二','周三','周四','周五','周六','周日']
        },
        yAxis: {
            type: 'value'
        },
        series: [
            {
                name:'邮件营销',
                type:'line',
                stack: '总量',
                data:[120, 132, 101, 134, 90, 230, 210]
            },
            {
                name:'联盟广告',
                type:'line',
                stack: '总量',
                data:[220, 182, 191, 234, 290, 330, 310]
            },
            {
                name:'视频广告',
                type:'line',
                stack: '总量',
                data:[150, 232, 201, 154, 190, 330, 410]
            },
            {
                name:'直接访问',
                type:'line',
                stack: '总量',
                data:[320, 332, 301, 334, 390, 330, 320]
            },
            {
                name:'搜索引擎',
                type:'line',
                stack: '总量',
                data:[820, 932, 901, 934, 1290, 1330, 1320]
            }
        ]
    };
    // 使用刚指定的配置项和数据显示图表。
    myChart.setOption(option);
}

//折柱混合图
function drawBarAndBrokenLineChart(data){
    var myChart = echarts.init(document.getElementById('main3'));

    

    option = {
    tooltip: {
        trigger: 'axis'
    },
    toolbox: {
        feature: {
            dataView: {show: true, readOnly: false},
            magicType: {show: true, type: ['line', 'bar']},
            restore: {show: true},
            saveAsImage: {show: true}
        }
    },
    legend: {
        data:['蒸发量','降水量','平均温度']
    },
    xAxis: [
        {
            type: 'category',
            data: ['1月','2月','3月','4月','5月','6月','7月','8月','9月','10月','11月','12月']
        }
    ],
    yAxis: [
        {
            type: 'value',
            name: '水量',
            min: 0,
            max: 250,
            interval: 50,
            axisLabel: {
                formatter: '{value} ml'
            }
        },
        {
            type: 'value',
            name: '温度',
            min: 0,
            max: 25,
            interval: 5,
            axisLabel: {
                formatter: '{value} °C'
            }
        }
    ],
    series: [
        {
            name:'蒸发量',
            type:'bar',
            data:[2.0, 4.9, 7.0, 23.2, 25.6, 76.7, 135.6, 162.2, 32.6, 20.0, 6.4, 3.3]
        },
        {
            name:'降水量',
            type:'bar',
            data:[2.6, 5.9, 9.0, 26.4, 28.7, 70.7, 175.6, 182.2, 48.7, 18.8, 6.0, 2.3]
        },
        {
            name:'平均温度',
            type:'line',
            yAxisIndex: 1,
            data:[2.0, 2.2, 3.3, 4.5, 6.3, 10.2, 20.3, 23.4, 23.0, 16.5, 12.0, 6.2]
        }
    ]
};
    // 使用刚指定的配置项和数据显示图表。
    myChart.setOption(option);
}
//地图
function drawMapChart(data){
    echarts.registerMap('china', data.chinaJson);
    var myChart = echarts.init(document.getElementById('main4'));
    
        // 指定图表的配置项和数据
    option = {
        tooltip: {
            trigger: 'item',
            formatter: '{b}'
        },
        series: [
            {
                name: '中国',
                type: 'map',
                mapType: 'china',
                selectedMode : 'multiple',
                label: {
                    normal: {
                        show: true
                    },
                    emphasis: {
                        show: true
                    }
                },
                data:[
                    {name:'广东', selected:true}
                ]
            }
        ]
    };

    // 使用刚指定的配置项和数据显示图表。
    myChart.setOption(option);
}
function loadjson(){
	var chart = echarts.init(document.getElementById('main'),'vintage');
		chart.setOption({
		    series: [{
		        type: 'map',
		        map: 'china'
		    }]
		});
}

function loadtheme(){
	var chart = echarts.init(document.getElementById('theme'),'vintage');
		chart.setOption({
			series: [{
		        type: 'map',
		        map: 'china'
		    }]
		    
		});
}



//折柱混合图
function drawBarAndBrokenLineBofItChart(data){
    var myChart = echarts.init(document.getElementById('main6'));


    option = {
    tooltip: {
        trigger: 'axis'
    },
    toolbox: {
        feature: {
            dataView: {show: true, readOnly: false},
            magicType: {show: true, type: ['line', 'bar']},
            restore: {show: true},
            saveAsImage: {show: true}
        }
    },
    legend: {
        data:['概率','概率']
    },
    xAxis: [
        {
            type: 'category',
            data: data.x
        }
    ],
    yAxis: [
        {
            type: 'value',
            name: '概率',
            min: 0,
            max: 0.2,
            interval: 0.05,
            axisLabel: {
                formatter: '{value}%'
            }
        },
    ],
    series: [
        {
            name:'概率',
            type:'bar',
            data:data.y
        },
        {
            name:'概率',
            type:'line',
            data:data.y
        }
    ]
};
    // 使用刚指定的配置项和数据显示图表。
    myChart.setOption(option);
}