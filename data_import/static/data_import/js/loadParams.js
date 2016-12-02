function loadOption(){
	$.ajax({
        type: "post",
        url:  "/load_procedure_name",
        data: {'greet':'hello'},
        error: function() {
            alert("404");
        },
        success: function(data) {
            console.log(data.procedure_names);
            pnames=data.procedure_names;
            for(var pname in pnames){
                console.log(pnames[pname])
                $(".procedurename").append("<option value='"+pname+"'>"+pnames[pname]+"</option>")
            }
            var filepath= 'http://127.0.0.1:8000'+data.filepath; 
            console.log("<a href='"+filepath+"'>")
            $("#filedownload").html("<a href='"+filepath+"'>下载文件</a>")
        }
    })
}
function loadOption_ha(){
    $.ajax({
        type: "post",
        url:  "/load_to",
        data: {'greet':'hello'},
        error: function() {
            alert("404");
        },
        success: function(data) {
            console.log(data.procedure_names);
            pnames=data.procedure_names;
            for(var pname in pnames){
                console.log(pnames[pname])
                $(".procedurename").append("<option value='"+pname+"'>"+pnames[pname]+"</option>")
            }
            var filepath= 'http://127.0.0.1:8000'+data.filepath; 
            console.log("<a href='"+filepath+"'>")
            $("#filedownload").html("<a href='"+filepath+"'>下载文件</a>")
        }
    })
}
function loadOption_hs(){
    $.ajax({
        type: "post",
        //url:  "/load_procedure_name",
        url:  "/lond_to",
        data: {'greet':'hello'},
        error: function() {
            alert("404");
        },
        success: function(data) {
            console.log(data.procedure_names);
            pnames=data.procedure_names;
            for(var pname in pnames){
                console.log(pnames[pname])
                $(".procedurename").append("<option value='"+pname+"'>"+pnames[pname]+"</option>")
            }
            //var filepath= 'http://127.0.0.1:8000'+data.filepath; 
            //console.log("<a href='"+filepath+"'>")
            //$("#filedownload").html("<a href='"+filepath+"'>下载文件</a>")
        }
    })
}
function getFilepath(){
    var procedure=$("#procedure").find("option:selected").val();//获取值用text()
    $.ajax({
        type: "post",
        url:  "/ana_data_lack",
        data: {'procedure':procedure},
        error: function() {
            alert("404");
        },
        success: function(data) {
            console.log(data.filepath);
            console.log('<a href="/download_file?filepath='+data.filepath+'">下载文件</a>')
            // $("#filedownload").html('<a href="/download_file?filepath='+data.filepath+'">下载文件</a>')
        }
    })


}