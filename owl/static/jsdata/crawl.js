/**
 * Created by dengqiuhua on 15-7-18.
 */

function addCrawl(){
    var url = $.trim($("#inputUrl").val());
    if (url == "" || url == "http://") {
        alert("请输入url");
        return false
    }
    if(url.lastIndexOf("http://") > 0){
        url = url.substring(url.lastIndexOf("http://"),url.length);
        $("#inputUrl").val(url);
    }
    var html_url = "<div class=\"row\">";
    html_url += "<div class=\"col-md-8\">"+ url +"</div>";
    html_url += "<div class=\"col-md-2 status\">未开始</div>";
    html_url += "<div class=\"col-md-2\">";
    html_url += "<button class=\"btn btn-primary\" type=\"submit\" onclick=\"crawl('"+ url +"',this);\">爬 行</button>";
    html_url += "</div>";
    html_url += "</div>";
    $("#url_queue").html(html_url);
}

function crawl(url,_this){
    $(_this).parents(".row").find(".status").text("爬行中");
    $(_this).attr("disabled","disabled");//禁用
    $.post(urls.api_crawl,{url:url},function(msg){
        if(msg.result){
            $(_this).parents(".row").find(".status").text("已完成");
        }else{
            $(_this).parents(".row").find(".status").text("发生错误");
        }
        $(_this).attr("disabled","");
    })
}


//获取url列表
function getUrlList(){
    var data = new pageData({url:urls.api_crawl,callback:"getUrlList"},function(msg){
        fillUrlList(msg);
    });
    /*
    $.get(urls.api_crawl,{},function(msg){
        fillUrlList(msg.data);
    })*/
}

function fillUrlList(msg){
    var html = "";
    if(msg != null && msg != ""){
        html += "<table class=\"table table-hover table-striped\">";
        $.each(msg,function(i,n){
            html += "<tr class=\"row\">";
            html += "<td>"+ n.url +"</td>";
            html += "<td>"+ n.click_counts +"</td>";
            html += "<td></td>";
            html += "<td><button class=\"btn btn-primary\" type=\"submit\" onclick=\"crawl('"+ n.url +"',this);\">爬 行</button></td>";
            html += "</tr>";
        });
        html += "<table>";
    }
    $("#datalist").html(html);
}