/**
 * Created with JetBrains WebStorm.
 * User: SisiLiu
 * Date: 15-9-5
 * Time: 上午11:57
 * To change this template use File | Settings | File Templates.
 */

$(function (){

    $("#userPsw").on("click",function(){
        popShow("#changePwdPop");
    });

    $("#checkOut").on("click",function(){
        window.location.href = window.rootURL + "/logout.jsp";
    });

    //遮罩
    $(".blackmask").css("width",$(window).width());
    $(".blackmask").css("height",$(window).height());

    //修改密码弹窗
    $("#changePwdPop .tabcon h3").html("修改"+userInfo+"的密码")

    $("#changePwdPop .cancel-btn").on("click",function(){
        $("#oldPwd").val("");
        $("#newPwd1").val("");
        $("#newPwd2").val("");
        popHide("#changePwdPop");
    });

    $("#changePwdPop .comfirm-btn").on("click",function(){
        changePassword();
    })
});

//修改密码弹窗事件
function changePassword(){

    $("#changePwdtip").css("display","none");
    var oldPwd = $("#oldPwd").val();
    var newPwd1 = $("#newPwd1").val();
    var newPwd2 = $("#newPwd2").val();

    if(newPwd1==""||newPwd2==""){
        $("#changePwdtip").html("请输入密码");
        $("#changePwdtip").css("display","block");
    }else if(newPwd1==newPwd2){

        $.ajax({
            type: "get",
            dataType: 'jsonp',
            url: window.domain+"/user/changepass",
            data: {
                "opassword":  oldPwd,
                "uid":uid,
                "npassword": newPwd1
            },
            error: function(data) {
                alert("404");
            },
            success: function(data) {
                if(data.success==0){
                    alert(data.error.message);
                }
                if(data.success==1){
                    popHide("#changePwdPop");
                    alert("修改密码成功");
                    $("#oldPwd").val("");
                    $("#newPwd1").val("");
                    $("#newPwd2").val("");
                }
            }
        });

    }else{
        $("#changePwdtip").html("新密码输入不同");
        $("#changePwdtip").css("display","block");
    }

}

function popShow(popId){
    $(".blackmask").css("width",$(window).width());
    $(".blackmask").css("height",$(window).height());
    $(".blackmask").css("display","block");
    $(popId).css("display","block");

}

function popHide(popId){

    $(".blackmask").css("display","none");
    $(popId).css("display","none");

}

//判断是否为正数
function check(c)
{
    var r= /^[+]?[0-9]*\.?[0-9]*$/;
    return r.test(c);
}
