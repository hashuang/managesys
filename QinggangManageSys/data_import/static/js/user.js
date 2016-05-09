/**
 * Created with JetBrains WebStorm.
 * User: SisiLiu
 * Date: 15-9-4
 * Time: 下午9:03
 * To change this template use File | Settings | File Templates.
 */

$(function(){

    $(".navbar-nav>li:eq(2)").addClass("active");

    //新建用户弹窗
    $("#newUser").on("click",function(){
        popShow("#newUserPop");
    });
    $("#newUserPop .cancel-btn").on("click",function(){
        popHide("#newUserPop");
    });
    $("#newUserPop .addConfirm").on("click",function(){
        addNewUser();
    });

    //删除用户弹窗
    $("#comfirmDelPop .cancel-btn").on("click",function(){
        $("#username").val("");
        $("#password").val("");
        popHide("#comfirmDelPop");
    });
    $("#comfirmDelPop .delConfirm").on("click",function(){
        popHide("#comfirmDelPop");
        delUser();
    });

    //用户列表删除
    $("#userList tbody").on("click",".delUser",function(){

        delUserid = $(this).attr("value");
        popShow("#comfirmDelPop");

    });

    searchUserList();

});

var delUserid = null;

//查询用户列表
function searchUserList(){

    $.ajax({
        type: "get",
        dataType: 'jsonp',
        url: domain+"/user/getall",
        data: {
            "token":  token
        },
        error: function(data) {
            alert("404");
        },
        success: function(data) {
            if(data.success==0){
                alert(data.error.message);
            }
            if(data.success==1){
                renderUserList(data.data.users);
            }
        }
    })

}

function renderUserList(list){

    var $container = $("#userList tbody");
    var tableHtml = "";
    $.each(list,function(n,value) {

        if(n%2==1){
            var trHtml = '<tr>';
        }else{
            var trHtml = '<tr class="active">';
        }
        trHtml +=    '<td>'+value.uid +'</td>'
                    +'<td>'+value.username +'</td>'
                    +'<td>'+userGroup[value.ugroup] +'</td>'
                    +'<td>'+value.regist_time +'</td>'
                    +'<td>'+value.login_time +'</td>'
                    +'<td><a href="#" class="delUser" value="'+value.uid+'">删除</a></td>'
                    +'</tr>';
        tableHtml += trHtml;
    });
    $container.html(tableHtml);

}

//删除用户
function delUser(){

    $.ajax({
        type: "get",
        dataType: 'jsonp',
        url: domain+"/user/delete",
        data: {
            "uid": delUserid,
            "token":  token
        },
        error: function(data) {
            alert("404");
        },
        success: function(data) {
            if(data.success==0){
                alert(data.error.message);
            }
            if(data.success==1){
                alert("删除用户成功！");
                delUserid = null;
                searchUserList();
            }
        }
    })

}

function addNewUser(){

    var username = $("#username").val();
    var password = $("#password").val();

    $.ajax({
        type: "get",
        dataType: 'jsonp',
        url: domain+"/user/add",
        data: {
            "username":username,
            "password":password,
            "token":  token,
            "ugroup":2
        },
        error: function(data) {
            alert("404");
        },
        success: function(data) {
            if(data.success==0){
                alert(data.error.message);
            }
            if(data.success==1){
                popHide("#newUserPop");
                alert("添加用户成功！");
                searchUserList();
                $("#username").val("");
                $("#password").val("");
            }
        }
    })

}
