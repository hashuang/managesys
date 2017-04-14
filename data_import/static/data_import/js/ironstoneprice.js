function drawHistoryPriceBrokenLineChart(data){
        var myChart = echarts.init(document.getElementById('history_figure'));
        option = {
            title: {
                text: '影响因素走势折线图'
            },
            tooltip: {
                trigger: 'axis'
            },
            legend: {
                data:['历史走势',]
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
                    name:'波罗的海指数',
                    type:'line',
                    stack: '总量',
                    data: data.price
                },
            ]
        };
        // 使用刚指定的配置项和数据显示图表。
        myChart.setOption(option);
    }
function drawPredictBrokenLineChart(data){
    var myChart = echarts.init(document.getElementById('predict_figure'));
    option = {
        title: {
            text: '预测图'
        },
        tooltip: {
            trigger: 'axis'
        },
        legend: {
            data:['历史值','预测值']
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
            data:data.timeline
        },
        yAxis: {
            type: 'value'
        },
        series: [
            {
                name:'历史值',
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
    var yinsu_type =$("#yinsu_type").val();
    var params = {"history_begin":history_begin,"history_end":history_end,"yinsu_type":yinsu_type}
    console.log(JSON.stringify(params));
    $.ajax({
        type: "post",
        url:  "/stone_price_history",
        data: params,
        error: function() {
            console.log("404");
        },
        success: function(data) {
            // console.log('123');
            console.log(data);
            drawHistoryPriceBrokenLineChart(data);
        }
    })
}
function predict_query(){
    var steelType = $("#iron_type").val();
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
        url:  "/stone_price_predict",
        data: params,
        error: function() {
            console.log("404");
        },
        success: function(data) {
            console.log(data);
            drawPredictBrokenLineChart(data.result.zhi)
        }
    })
}
$(function(){

})