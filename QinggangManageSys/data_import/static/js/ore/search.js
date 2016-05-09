/**
 * Created with JetBrains WebStorm.
 * User: SisiLiu
 * Date: 15-9-5
 * Time: 下午8:59
 * To change this template use File | Settings | File Templates.
 */

$(function(){

    $(".navbar-nav>li:eq(0)").addClass("active");

    searchOreList();
    //高级搜索
    $("#accuSearch").on("click",function(){
        $("#hiddenAccu").toggle();
    });
    //选择搜索内容
    $("#searchStyle li a").on("click",function(){
        var $container = $("#searchStyle button label");
        $container.html(searchStyle[$(this).attr("value")]);
        $container.attr("value",$(this).attr("value"));
    });
    //搜索按钮
    $("#searchBtn").on("click",function(){
        createCondition();
        reqData.page_index=1;
        reqData.order = "addtime";
        searchOreList();
    });
    //分页
    $(".pagination").on("click",".page-number",function(){
        var index = $(this).attr("value");
        reqData.page_index = index;
        searchOreList();
    });
    $(".pagination").on("click",".page-previous",function(){
        if(reqData.page_index>1){
            reqData.page_index--;
            searchOreList();
        }
    });
    $(".pagination").on("click",".page-next",function(){
        if(reqData.page_index<totalIndex){
            reqData.page_index++;
            searchOreList();
        }
    });
    //表头的排序
    $("#oreList").on("click","th[type=th]",function(){
        var orderName = $(this).attr("value");
        reqData.page_index =1;
        reqData.order = orderName;
        searchOreList();
    });
});

var searchStyle = {
    name:"铁矿粉名称",
    username:"添加者",
    addtime:"添加时间"
};

var reqData = {
    token:token,
    page_size:10,
    page_index:1,
    order:"addtime"
};

var totalIndex = 0;

//生成搜索condition
function createCondition(){

    var conditionStr = "";
    //如果搜索条件不为空
    if($("#kw").val()!=""){
        var ss = $("#searchStyle li a").attr("value");
        conditionStr += (ss+"\r" + $("#kw").val() + "\r\n");
    }

    //如果显示高级搜索
    if($("#hiddenAccu").css("display")=="block"){
        var $inputList = $("#hiddenAccu input.val");
        $.each($inputList,function(n,i){
            //if 最小值  else 最大值
            if(n%2==0){
                conditionStr += $(i).attr("name")+'\r';
                conditionStr += $(i).val() + '\r';
            }else{
                conditionStr += $(i).val() + '\n';
            }
        });
    }

    reqData.condition = conditionStr;

}

//搜索铁矿粉列表
function searchOreList(){

    $.ajax({
        type: "get",
        dataType: 'jsonp',
        url: domain + "/ore/search",
        data: reqData,
        error: function() {
            alert("404");
        },
        success: function(data) {
            if(data.success==0){
                alert(data.error.message);
            }
            if(data.success==1){
                renderOreList(data.data.ores);
                totalIndex = data.data.page_count;
                renderOrePagination(totalIndex);
            }
        }
    });
}

//渲染铁矿粉列表
function renderOreList(list){

    var $container = $("#oreList tbody");

    var tableHtml = "";

    $.each(list,function(n,value) {

        if(n%2==1){
            var trHtml = '<tr>';
        }else{
            var trHtml = '<tr class="active">';
        }
        trHtml +=
            '<td>'+value.name +'</td>'
            +'<td>'+value.al2o3 +'</td>'
            +'<td>'+value.cao +'</td>'
            +'<td>'+value.feo +'</td>'
            +'<td>'+value.mgo +'</td>'
            +'<td>'+value.sio2 +'</td>'
            +'<td>'+value.tfe +'</td>'
            +'<td>'+value.assimilability +'</td>'
            +'<td>'+value.bond_strength +'</td>'
            +'<td>'+value.burning_loss +'</td>'
            +'<td>'+value.crystal_strength +'</td>'
            +'<td>'+value.fluxility +'</td>'
            +'<td>'+value.score.toFixed(2) +'</td>'
            +'<td>'+value.cost.toFixed(2) +'</td>'
            +'<td>'+value.username +'</td>'
            +'<td>'+value.addtime.substring(0,10) +'</td>'
            +'<td><button type="submit" class="btn btn-info" style="padding: 0 2px; font-size:12px;" onclick="updateCost('+value.id+')">修改</button></td>'
            +'<td><button type="submit" class="btn btn-info" style="padding: 0 2px; font-size:12px;" onclick="deleteOre('+value.id+')">删除</button></td>'
            +'</tr>';
        tableHtml += trHtml;
    });

    $container.html(tableHtml);

}

function renderOrePagination(pages){
    $(".page-number").detach();
    var $container = $(".pagination li:eq(0)");
    var html = "";
    for(var i=1;i<=pages;i++){
        html +='<li><a class="page-number" href="#" value="'+i+'">'+i+'</a></li>';
    }
    $container.after(html);
}



function updateCost( oreid ) {
   popShow("#updateCostDiv"); 
   $("#oreId").val(oreid);
   
}

function quitCostDiv() {
    popHide("#updateCostDiv");
}
// 更新铁矿粉价格
function updatCostToServer(){

    reqData = {'cost': $("#currentCost").val() ,'token':token,'id':$("#oreId").val()}
    $.ajax({
        type: "get",
        dataType: 'jsonp',
        url: domain + "/ore/updatecost",
        data: reqData,
        error: function() {
            alert("404");
            popHide("#updateCostDiv");
        },
        success: function(data) {
            if(data.success==0){
                alert(data.error.message);
            }
            if(data.success==1){
            }
            popHide("#updateCostDiv");
            searchOreList();
        }
    });
    
}

function deleteOre(oreid){

    reqData = {'oreid':parseInt(oreid),'token':token};
    $.ajax({
        type: "get",
        dataType: 'jsonp',
        url: domain + "/ore/delete",
        data: reqData,
        error: function() {
            alert("404");
        },
        success: function(data) {
            if(data.success==0){
                alert(data.error.message);
            }
            if(data.success==1){
            }
            searchOreList();
        }
    });
}
