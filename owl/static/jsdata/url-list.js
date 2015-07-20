/**
 * Created by dengqiuhua on 15-7-18.
 */

$(function(){
    getUrlList();
});

//获取url列表
function getUrlList(){
    $.get(urls.api_crawl,{},function(msg){
        fillUrlList(msg.data);
    })
}

function fillUrlList(msg){
    var html = "";
    if(msg != null && msg != ""){
        html += "<table class=\"table table-hover\">";
        $.each(msg,function(i,n){
            html += "<tr>";
            html += "<td>"+ n.url +"</td>";
            html += "<td>"+ n.click_counts +"</td>";
            html += "</tr>";
        });
        html += "<table>";
    }
    $("#datalist").html(html);
}