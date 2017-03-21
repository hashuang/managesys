function drawHistoryPriceBrokenLineChart(data){
        var myChart = echarts.init(document.getElementById('history_figure'));
        option = {
            title: {
                text: '钢材价格走势折线图'
            },
            tooltip: {
                trigger: 'axis'
            },
            legend: {
                data:['特钢价格历史走势',]
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
                data: data.timeline
            },
            yAxis: {
                type: 'value'
            },
            series: [
                {
                    name:'特钢价格历史走势',
                    type:'line',
                    stack: '总量',
                    data: data.price
                },
            ]
        };
        // 使用刚指定的配置项和数据显示图表。
        myChart.setOption(option);
    }
function drawPredictBrokenLineChart(data,figure_name){
    var myChart = echarts.init(document.getElementById(figure_name));
    if(figure_name == "predict_figure")figure_name="钢材";
    option = {
        title: {
            text: figure_name + '预测图'
        },
        tooltip: {
            trigger: 'axis'
        },
        legend: {
            data:['真实值','预测值','评分：'+data.score]
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
            data: data.timeline
        },
        yAxis: {
            type: 'value'
        },
        series: [
            {
                name:'真实值',
                type:'line',
                stack: '总量',
                data:data.true_value
            },
            {
                name:'预测值',
                type:'line',
                stack: '总量',
                data:data.predict_value
            },
        ]
    };
    // 使用刚指定的配置项和数据显示图表。
    myChart.setOption(option);
}
function history_query(){
    var history_begin =$("#history_begin").val();
    var history_end =$("#history_end").val();
    var params = {"history_begin":history_begin,"history_end":history_end}
    console.log(JSON.stringify(params));
    $.ajax({
        type: "post",
        url:  "/price_history",
        data: params,
        error: function() {
            console.log("404");
        },
        success: function(data) {
            console.log(data);
            drawHistoryPriceBrokenLineChart(data);
            var json1 = {1:'9',2:'3',3:'1'};
            $.each(json1,function(name,value) {
                alert(value);
            });
        }
    })
}
function predict_query(){
    var steelType = $("#steel_type").val();
    console.log(steelType);
    var timeScale = $("#time_scale").val();
    console.log(time_scale);
    var type_array=new Array();
    $('input[name="predict_method"]:checked').each(function(){
        type_array.push($(this).val());//向数组中添加元素
    });
    var typestr=type_array.join(',');//将数组元素连接起来以构建一个字符串
    console.log(typestr);
    var params = {"steelType":steelType,"typestr":typestr,"timeScale":timeScale}
    console.log(params);
    $.ajax({
        type: "post",
        url:  "/price_predict",
        data: params,
        error: function() {
            console.log("404");
        },
        success: function(data) {
            $("#figures").empty();
            console.log(data);
            var pridict_result_json = data.result
            var len = 0;
            for(var item in pridict_result_json)len++;
            alert(len);
            var num = 0;
            var figures = $("#figures")

            $.each(pridict_result_json,function(name,value) {
                if(num ==0){
                    figure_name = "predict_figure";
                    drawPredictBrokenLineChart(value,figure_name)
                }
                    
                figures.append("<div id='"+ name +"' style='width: 500px;height:400px;'></div>")
                drawPredictBrokenLineChart(value,name)
            });

        }
    })
}
$(function(){

})