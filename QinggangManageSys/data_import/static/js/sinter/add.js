/**
 * Created with JetBrains WebStorm.
 * User: SisiLiu
 * Date: 15-10-31
 * Time: 下午4:39
 * To change this template use File | Settings | File Templates.
 */

$(function(){

    $oreTarget = "";
    comTargetHtml = "";

    $(".navbar-nav>li:eq(1)").addClass("active");

    //搜索按钮
    $("#searchBtn").on("click",searchOreList);

    //添加操作
    $("#oreList").on("click",".btn-info",function(){
        popShow("#addWeight");
        $("#weight").val(0);
        $oreTarget = $(this);
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

    //添加权重弹窗
    $("#addWeight .cancel-btn").on("click",function (){
        popHide("#addWeight");
    });
    $("#addWeight .weightConfirm").on("click",function (){
        addOre();
    });

    //添加烧结矿
    $("#addSinterConfirm").on("click",function(){
        checkAllInput();
    });
    $("#comfirmAddPop .cancel-btn").on("click",function (){
        popHide("#comfirmAddPop");
    });
    $("#comfirmAddPop .comfirm-btn").on("click",function (){
        addSinter();
    });

});

//检查输入是否为空
function checkAllInput(){
    var inputList = $("#sinterContentBody .add-table input");

    var tag =1;
    $.each(inputList,function(n,i){
        if($(i).val()==""){
            alert("输入不能为空");
            tag = 0;
            return false;
        }
    });
    if(tag){
        if($("#ore-comps").children().length==0){
            alert("组成成分不能为空");
            return false;
        }else{
            popShow("#comfirmAddPop");
        }
    }
}

function clearAllInput(){
    var inputList = $("#sinterContentBody .add-table input");
    $.each(inputList,function(n,i){
        $(i).val("");
    });
    $("#ore-comps").html("");
    $("#oreList tbody").html("");
}

//添加烧结矿
function addSinter(){

    var $inputList = $("#sinterContentBody .add-table input");
    var data = {};
    var materialStr = createMaterials();
    $.each($inputList,function(n,i){
        data[$(i).attr("name")]=$(i).val();
    });
    data["token"]=token;
    data["materials"]=materialStr;

    $.ajax({
        type: "get",
        dataType: 'jsonp',
        url: window.domain + "/sinter/add",
        data: data,
        error: function() {
            alert("404");
            popHide("#comfirmAddPop");
        },
        success: function(data) {
            popHide("#comfirmAddPop");
            if(data.success==1){
                alert("添加烧结矿成功！");
                clearAllInput();
            }else{
                alert(data.error.message);
            }
        }
    });
}
function createMaterials(){
    var materialStr = "";
    var $comps = $("#ore-comps").children();
    $.each($comps,function(n,i){
        materialStr += $(i).attr("oid")+"\r"+$(i).attr("weight")+"\n";
    });
    return materialStr;
}

//添加矿粉
function addOre(){
    popHide("#addWeight");
    $oreTarget.removeClass("btn-info").addClass("btn-none");
    var $name = $($oreTarget.parent().parent().children()[0]);
    var weight = $("#weight").val();
    var $container = $("#ore-comps");
    var $compHtml='<div class="btn btn-xs btn-warning" oid="'+$name.attr("value")+'" weight="'+weight+'">'+$name.html()+"("+weight+")"+'</div>\n';
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

    var $container = $("#oreList tbody");
    var tableHtml = "";
    $.each(list,function(n,value) {

        if(n%2==1){
            var trHtml = '<tr>';
        }else{
            var trHtml = '<tr class="active">';
        }
        trHtml +=
                '<td value="'+value.id+'">'+value.name +'</td>'
                +'<td>'+value.username +'</td>'
                +'<td>'+value.addtime +'</td>'
                +'<td>'+value.score +'</td>'
                +'<td><div class="btn btn-xs btn-info">添加</div></td>'
            +'</tr>';
        tableHtml += trHtml;
    });

    $container.html(tableHtml);
}
