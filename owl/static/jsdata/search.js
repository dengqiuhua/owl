/**
 * Created by Administrator on 2015/7/21.
 */
$(function(){
    //搜索
    search();
});

function search(){
    var keywords = $.trim($("#inputKeywords").val());
    var data = new pageData({url:urls.url_api_search,data:{kw:keywords},callback:"search"},function(msg){
        fillSearchResult(msg);
    });
}

function fillSearchResult(msg){
    var html = "";
    if(msg != null && msg != "") {
        $.each(msg,function(i,n) {
            if(n.url != null) {
                html += "<div class=\"row\">";
                html += "<h4><a href=\"" + n.url + "\" target=\"_blank\">" + n.url + "</a></h4>";
                html += "<div>";
                html += "<p>"+ n.description +"</p>";
                html += "</div>";
                html += "<div>";
                html += "<span class=\"muted\">来源</span>";
                html += "</div>";
                html += "</div>";
            }
        });
    }else{
        html = "<div>没有结果</div>";
    }
    $("#datalist").html(html);
}