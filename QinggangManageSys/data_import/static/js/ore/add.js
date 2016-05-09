/**
 * Created with JetBrains WebStorm.
 * User: SisiLiu
 * Date: 15-9-5
 * Time: 下午2:41
 * To change this template use File | Settings | File Templates.
 */

$(function(){

    $(".navbar-nav>li:eq(0)").addClass("active");

    $("#addOreConfirm").on("click",function(){
        checkAllInput();
    });

    //确认弹窗
    $("#comfirmAddPop .cancel-btn").on("click",function(){
        popHide("#comfirmAddPop");
    });
    $("#comfirmAddPop .comfirm-btn").on("click",function(){
        popHide("#comfirmAddPop");
        addAllInput();
    });

});

function checkAllInput(){

    var inputList = $("#oreContentBody input.val");
    var tag =1;

    $.each(inputList,function(n,i){
        if(n==0&&($(i).val()=="")){
            alert("输入不能为空");
            tag = 0;
            return false;
        }else if(!check($(i).val())&&n!=0){
            alert("请输入数字");
            tag = 0;
            return false;
        }
    });

    if(tag){
        popShow("#comfirmAddPop");
    }

}

function addAllInput(){

    var inputList = $("#oreContentBody input.line");
    var urlData = {};

    $.each(inputList,function(n,i){

        var dataKey = $(i).attr("id");
        var dataValue = $(i).val();
        urlData[dataKey]=dataValue;

    });

    urlData["token"] = token;

    $.ajax({
        type: "get",
        dataType: 'jsonp',
        url: domain+"/ore/add",
        data: urlData,
        error: function(data) {
            alert("404");
        },
        success: function(data) {
            if(data.success==0){
                alert(data.error.message);
            }
            if(data.success==1){
                alert("添加铁矿粉成功");
                console.log(data.data.ore);
            }
        }
    });

    clearAllInput();

}

function clearAllInput(){

    var inputList = $("#oreContentBody .add-table input.val");

    $.each(inputList,function(n,i){

        $(i).val("0");

    });

    $("#oreContentBody .ore-name").val("");

}
