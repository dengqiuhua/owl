/**
 * Created by dengqiuhua on 15-7-18.
 */

function addCrawl(){
    var url = $.trim($("#inputUrl").val());
    if (url == "" || url == "http://") {
        alert("请输入url");
        return false
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
    $(_this).parents(".row").find(".status").text("爬行中").attr("disabled","disabled");
    $.post(urls.api_crawl,{url:url},function(msg){
        if(msg.result){
            $(_this).parents(".row").find(".status").text("已完成");
        }else{
            $(_this).parents(".row").find(".status").text("发生错误");
        }
    })
}

