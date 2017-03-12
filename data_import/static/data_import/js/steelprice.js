function history_query(){
    var history_begin =$("#history_begin").val();
    var history_end =$("#history_end").val();
    var params = {"history_begin":history_begin,"history_end":history_end}
    console.log(params);
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
        }
    })
    
}
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
$(function(){
    function price_history(){
        $.ajax({
            type: "post",
            url:  "/price_history",
            data: {},
            error: function() {
                console.log("404");
            },
            success: function(data) {
                console.log(data);
                drawHistoryPriceBrokenLineChart(data);
            }
        })
    }
})