/**
 * Created with JetBrains WebStorm.
 * User: SisiLiu
 * Date: 15-10-31
 * Time: 下午9:25
 * To change this template use File | Settings | File Templates.
 */
/**
 * Created with JetBrains WebStorm.
 * User: SisiLiu
 * Date: 15-10-31
 * Time: 下午4:39
 * To change this template use File | Settings | File Templates.
 */

var pageSize  = 10;
var g_sinters = [];
$(function(){

    comTargetHtml = "";

    $(".navbar-nav>li:eq(1)").addClass("active");

    //搜索按钮
    $("#searchBtn").on("click",searchOreList);

    //添加操作
    $("#oreList").on("click",".btn-info",function(){
        addOre($(this));
    });

    //组成成分删除操作
    $("#ore-comps").on("mouseenter","div.btn",function(){
        comTargetHtml = $(this).html();
        $(this).removeClass("btn-warning").addClass("btn-danger");
        $(this).css("width",$(this).outerWidth());
        $(this).html("删除");
    });
    $("#ore-comps").on("mouseleave","div.btn",function(){
        $(this).removeClass("btn-danger").addClass("btn-warning");
        $(this).html(comTargetHtml);
    });
    $("#ore-comps").on("click","div.btn",function(){
        delOre($(this));
    });

    //筛选
    $("#filterSinterConfirm").on("click",function(){
        searchSinterList();
    });
});

function searchSinterList(){

    var materialStr = "";
    var $comps = $("#ore-comps").children();
    if($comps.length==0){
        alert("铁矿粉组成不能为空");
        return false;
    }
    $.each($comps,function(n,i){
        if(n==0){
            materialStr += $(i).attr("oid");
        }else{
            materialStr += ","+$(i).attr("oid");
        }
    });
    $.ajax({
        type: "get",
        dataType: 'jsonp',
        url: domain + "/sinter/find",
        data: {
            token:token,
            oreids:materialStr
        },
        error: function() {
            alert("404");
        },
        success: function(data) {
            g_sinters = data.data.sinters;
            drawSearchResult( g_sinters, "result");
            //drawPage(data.data.page_count, data.data.page_index, "pagination");
            //$(".pageIndex").click( function(){
            //    searchSinterList( $(this).attr('pageIndex'));
            //});
        }
    });

}

//添加矿粉
function addOre($oreTarget){
    $oreTarget.removeClass("btn-info").addClass("btn-none");
    var $name = $($oreTarget.parent().parent().children()[0]);
    var weight = $("#weight").val();
    var $container = $("#ore-comps");
    var $compHtml='<div class="btn btn-xs btn-warning" oid="'+$name.attr("value")+'">'+$name.html()+'</div>\n';
    $container.append($compHtml);
}

//删除矿粉
function delOre($target){
    var oid = $target.attr("oid");
    var $name = $($("#oreList tbody").find('td[value="'+oid+'"]'));
    $($name.parent().children()[4]).children().removeClass("btn-none").addClass("btn-info");
    $target.remove();
}

//搜索铁矿粉列表
function searchOreList(){

    var oreName = $("#kw").val();
    $("#searchBtn").off("click",searchOreList);
    $.ajax({
        type: "get",
        dataType: 'jsonp',
        url: window.domain + "/ore/search",
        data: {
            condition:"name\r"+oreName+"\r",
            token:token,
            page_size:1000
        },
        error: function() {
            alert("404");
        },
        success: function(data) {
            if(data.success==0){
                alert(data.error.message);
                $("#searchBtn").on("click",searchOreList);
            }
            if(data.success==1){
                renderOreList(data.data.ores);
                $("#searchBtn").on("click",searchOreList);
            }
        }
    });
}

//渲染铁矿粉列表
function renderOreList(list){
    // 
    var exists = [];
    var $comps = $("#ore-comps").children();
    $.each($comps,function(n,i){
        exists.push(  $(i).attr("oid") )
    });


    $("#oreList").show();
    var $container = $("#oreList tbody");
    var tableHtml = "";
    $.each(list,function(n,value) {

        if(n%2==1){
            var trHtml = '<tr>';
        }else{
            var trHtml = '<tr class="active">';
        }

        var btnNone = "btn-info";
        for( var i = 0; i < exists.length; i++ ){
            if( value.id == exists[i] ){
                btnNone = "btn-none";
            }
        }
        trHtml +=
            '<td value="'+value.id+'">'+value.name +'</td>'
                +'<td>'+value.username +'</td>'
                +'<td>'+value.addtime +'</td>'
                +'<td>'+value.score.toFixed(2) +'</td>'
                +'<td><div class="btn btn-xs '+btnNone+'">添加</div></td>'
                +'</tr>';
        tableHtml += trHtml;
    });

    $container.html(tableHtml);
}
