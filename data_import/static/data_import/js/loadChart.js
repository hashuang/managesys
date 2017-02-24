//条形图
// function drawBarChart(result){
//     var myChart = echarts.init(document.getElementById('main1'));
//         //alert(result.scope)
//         // 指定图表的配置项和数据
//         var option = {
//             title: {
//                 text: ''
//             },
//             tooltip: {},
//             legend: {
//                 data:['']
//             },
//             xAxis: {
//                 data: result.scope
//             },
//             yAxis: {},
//             series: [{
//                 name: '',
//                 type: 'bar',
//                 data: result.num
//             }]

//         };

//     // 使用刚指定的配置项和数据显示图表。
//     myChart.setOption(option);
// }

function drawBarChart(result){
    var myChart = echarts.init(document.getElementById('main1'));
        //alert(result.scope)
       var option = {
            title: {
                text: '',
                x:'center'
            },
            tooltip: {},
            legend: {
                data:['']
            },
            toolbox: {
                show : true,
                feature : {
                    dataView : {show: true, readOnly: false},
                    magicType : {show: true, type: ['line', 'bar']},
                    restore : {show: true},
                    saveAsImage : {show: true}
                }
            },
            xAxis: {
                data: result.scope
            },
            yAxis: {},
            series: [{
                name: '',
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
            
            ]

        };

    //使用刚指定的配置项和数据显示图表。
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


//地图----中国地图
function drawMapChartChina(data,tradeNo,aspect_name,maxValue,module_name,sql_date1,sql_date2,dateChoose_name,space_name,unite){
    // echarts.registerMap('china', data.chinaJson);
    var myChart = echarts.init(document.getElementById('main4'));
    
        // 指定图表的配置项和数据
    option = {
        title : {
            text: module_name + '——' + aspect_name + '（' + space_name + '）',
            subtext: sql_date1 + '至' + sql_date2 + '内，以' + dateChoose_name + '为依据的' + space_name + '范围内' + aspect_name,
            x:'center'
        },
        tooltip: {
            trigger: 'item',
            formatter : function (params) {
                //console.log(params);
                if (typeof params.value =='object'){
                   return aspect_name + '<br/>' + params.name + ' : 总销量为0，无法计算退货率！';
                }else{
                    return aspect_name + '<br/>' + params.name + ' : ' + params.value + unite;
                }
            }
        },
        legend: {
            orient: 'vertical',
            x:'left',
            data:[tradeNo]
        },
        dataRange: {
            min: 0,
            max:  (maxValue + 1),
            x: 'left',
            y: 'bottom',
            text:['高','低'],           // 文本，默认为数值文本
            calculable : true,
            color: ['orangered','yellow','lightskyblue']
            //color: ['red','lightgray']
        },
        toolbox: {
            show: true,
            orient : 'vertical',
            x: 'right',
            y: 'center',
            feature : {
                //mark : {show: true},
                dataView : {show: true, readOnly: false},
                //restore : {show: true},
                saveAsImage : {show: true}
            }
        },
        roamController: {
            show: true,
            x: 'right',
            mapTypeControl: {
                'china': true
            }
        },
        series: [
            {
                name: tradeNo,
                type: 'map',
                mapType: 'china',
                roam: false,
                itemStyle:{
                    normal:{
                        label:{show:true},
                    },
                    emphasis:{label:{show:true}}

                },
                data: data
            }
        ]
    };
    // 使用刚指定的配置项和数据显示图表。
    myChart.setOption(option);
}

//地图 --- 世界地图
function drawMapChartWorld(data,tradeNo,aspect_name,unite,maxValue,module_name,sql_date1,sql_date2,dateChoose_name,space_name){
    // echarts.registerMap('china', data.chinaJson);
    var myChart = echarts.init(document.getElementById('main4'));
    
        // 指定图表的配置项和数据
    option = {
        title : {
            text: module_name + '——' + aspect_name + '（' + space_name + '）',
            subtext: sql_date1 + '至' + sql_date2 + '内，以' + dateChoose_name + '为依据的' + space_name + '范围内' + aspect_name,
            x:'center',
            y:'top'
        },
       
        tooltip : {
            trigger: 'item',
            formatter : function (params) {
                //console.log(params);
                if (typeof params.value =='object'){
                    return aspect_name + '<br/>' + params.name + ' : 总销量为0，无法计算退货率！';
                }else{
                    return aspect_name + '<br/>' + params.name + ' : ' + params.value + unite;
                }
            }
        },
        toolbox: {
            show : true,
            orient : 'vertical',
            x: 'right',
            y: 'center',
            feature : {
                //mark : {show: true},
                dataView : {show: true, readOnly: false},
                //restore : {show: true},
                saveAsImage : {show: true}
            }
        },
        dataRange: {
            min: 0,
            max:  (maxValue + 1),
            text:['High','Low'],
            realtime: false,
            calculable : true,
            color: ['orangered','yellow','lightskyblue']
        },
        series : [
            {
                name: aspect_name,
                type: 'map',
                mapType: 'world',
                roam: true,
                mapLocation: {
                    y : 60
                },
                itemStyle:{
                    emphasis:{label:{show:true}}
                },
                data:data
            }
        ]
    };
                    
    // 使用刚指定的配置项和数据显示图表。
    myChart.setOption(option);
}



//地图----山东地图
function drawMapChartShandong(data,tradeNo,aspect_name,unite,maxValue,module_name,sql_date1,sql_date2,dateChoose_name,space_name){
    // echarts.registerMap('china', data.chinaJson);
    var myChart = echarts.init(document.getElementById('main4'));
    
        // 指定图表的配置项和数据
    option = {
        title : {
            text: module_name + '——' + aspect_name + '（' + space_name + '）',
            subtext: sql_date1 + '至' + sql_date2 + '内，以' + dateChoose_name + '为依据的' + space_name + '范围内' + aspect_name,
            x:'center'
        },
        legend: {
            orient: 'vertical',
            x:'left',
            data:[tradeNo]
        },
        tooltip : {
            trigger: 'item',
            formatter : function (params) {
                //console.log(params);
                if (typeof params.value =='object'){
                    return aspect_name + '<br/>' + params.name + ' : 总销量为0，无法计算退货率！';
                }else{
                    return aspect_name + '<br/>' + params.name + ' : ' + params.value + unite;
                }
            }
            // formatter: function(a){
            //   return a[2];
            // }
        },
        dataRange: {
            min: 0,
            max: (maxValue + 1),
            x: 'left',
            y: 'bottom',
            text:['高','低'],           // 文本，默认为数值文本
            calculable : true,
            color: ['orangered','yellow','lightskyblue']
        },
        series : [
            {
                name: tradeNo,
                type: 'map',
                mapType: '山东',
                selectedMode: 'single',
                itemStyle:{
                    normal:{label:{show:true}},
                    emphasis:{label:{show:true}}
                },
                data: data
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