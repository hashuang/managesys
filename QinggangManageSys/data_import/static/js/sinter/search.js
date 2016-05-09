function drawPage(pageCount, pageIndex, domId){
    var pageStart = pageIndex - 5;
    if (pageStart < 1){
        pageStart = 1;
    }

    var pageEnd = pageIndex + 5;
    if (pageEnd > pageCount){
        pageEnd = pageCount;
    }

    html = '';
    if( pageStart != 1){
        html += ('<li><a class="pageIndex" pageIndex="1">1</a></li> <li><a>...</a></li>');
    }
    for( var i = pageStart; i < pageEnd+1; i++){
        if( i == pageIndex ){
            html += ('<li class="active" ><a class="pageIndex" pageIndex="'+i+'">'+i+'</a></li>');
        } else {
           html += ('<li><a class="pageIndex" pageIndex="'+i+'">'+i+'</a></li>'); 
        }
    }
     if( pageEnd != pageCount){
        html += (' <li><a>...</a></li><li><a class="pageIndex" pageIndex="'+pageCount+'">'+pageCount+'</a></li>');
    }

    $("#"+domId).html( html );
}

function drawSearchResult(sinters,  domId){
    $("#oreList").hide();
    html = '<table class="table" id="advanced">'
    if( sinters.length < 1 ){
        html += '<tr><td>没有符合检索条件的烧结矿</td></tr>';
    } else {
        html += '<tr><td>烧结矿名称</td> <td>利用系数</td> <td>燃耗</td> <td>成品率</td> <td>转鼓指数</td> <td>还原度</td> <td>软化区间</td> <td>开始软化<br>温度</td> <td>低温粉化<br>指数</td> <td>添加时间</td> <td>评分</td> <td>成本</td> <td>组成</td> <td>操作</td> </tr>';
        for(var i = 0; i < sinters.length; i++ ){
            s = sinters[i];
            if(i%2==1){
                html+='<tr  class="active" id="sinter_' + s.id + '">'
            }else{
                html+='<tr id="sinter_'+s.id+'">'
            }
            html+=('<td>'+s.name+'</td>'
                +'<td>'+s.usage_factor+'</td>'
                +'<td>'+s.fuel_consumption+'</td>'
                +'<td>'+s.rate_of_ok+'</td>'
                +'<td>'+s.drum_index+'</td>'
                +'<td>'+s.reduction_degree+'</td>'
                +'<td>'+s.softening_region+'</td>'
                +'<td>'+s.softening_index+'</td>'
                +'<td>'+s.low_temperature+'</td>'
                +'<td>'+s.addtime.substring(0,10)+'</td>'
                +'<td>'+s.score.toFixed(2)+'</td>'
                +'<td>'+s.cost.toFixed(2)+'</td>'
                +'<td ><a class="material" sinterid="'+s.id+'" id="popup_'+s.id+'">查看</td>'
                +'<td><button type="submit" class="btn btn-danger" style="padding: 0 2px; font-size:12px;" onclick="deleteSinter('+s.id+')" >删除</button></td> </tr>' );
        }
    }
    html += "</table>";
    $("#"+domId).html( html );

    // 材料组成
    $(".material").mouseover( function() {
        sinterid=$(this).attr('sinterid');
        sinter = {};
        for(var i = 0; i < g_sinters.length; i++ ){
            if( sinterid == g_sinters[i].id ){
                sinter = g_sinters[i];
                break;
            }
        }

        char_text = (sinter.name || '');
        chart_subtext = (sinter.username || '') + "于" + sinter.addtime;
        chart_subtext = "";
        sinter.material = sinter.material || [];
        x = [];
        y = [];
        for( var i = 0; i < sinter.material.length; i++){
            m = sinter.material[i];
            x.push( m.ore_name + ':  ' + (m.ore_rate*100).toFixed(2)+'%');
            y.push( {value:m.ore_rate, name:m.ore_name + ':  ' + (m.ore_rate*100).toFixed(2)+'%'} );
        }


        // 基于准备好的dom，初始化echarts图表
        var myChart = echarts.init(document.getElementById('pic')); 
        
        option = {
            title : {
                text: char_text,
                subtext: chart_subtext,
                x:'right'
            },
            tooltip : {
                trigger: 'item',
                formatter: "{a} <br/>{b} : {c} ({d}%)"
            },
            legend: {
                orient : 'vertical',
                x : 'left',
                data:x
            },
            toolbox: {
                show : false
            },
            calculable : true,
            series : [
                {
                    name:'组成成分',
                    type:'pie',
                    radius : '25%',
                    center: ['50%', '60%'],
                    data:y
                }
            ]
        };

        // 为echarts对象加载数据 
        myChart.setOption(option); 

        easyDialog.open({
          container : 'material_popup',
          autoClose : 200000,
          fixed : false,
          overlay : false,
          follow : 'popup_'+sinterid,
          followX : -300,
          followY : -150
        });
    });

    $(".material").mouseout( function() {
        easyDialog.close();
    });        
}


function deleteSinter( sinterid ){
    $.ajax({
        type: "get",
        dataType: 'jsonp',
        url: domain+"/sinter/delete",
        data: {'id':sinterid, 'token':token},
        error: function(data) {
            alert("删除出错，请重试");
        },
        success: function(data) {
            if(data.success==0){
                alert(data.error.message);
            }
            if(data.success==1){
                $("#sinter_"+sinterid).hide();
                alert("删除成功")
            }
        }
    });
}

