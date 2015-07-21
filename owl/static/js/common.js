/**
 * Created with PyCharm.
 * User: Administrator
 * Date: 14-8-5
 * Time: 下午4:28
 * To change this template use File | Settings | File Templates.
 */
/**
 * Created with PyCharm.
 * User: dengqiuhua
 * Date: 14-7-16
 * Time: 上午10:21
 * To change this template use File | Settings | File Templates.
 */
$(function () {
    //提示框
    setTimeout('$("*[data-toggle=tooltip]").tooltip();', 2000);

    //所有Ajax的post请求需要csrftoken，否则403
    var csrftoken = $.cookie('csrftoken');

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

});


//扩展数组属性[移除]
Array.prototype.remove = function (index) {
    if (isNaN(index) || index > this.length) {
        return false;
    }
    for (var i = 0, n = 0; i < this.length; i++) {
        if (this[i] != this[index]) {
            this[n++] = this[i];
        }
    }
    this.length -= 1;
    return true;
};

//扩展数组属性[插入]
Array.prototype.insert = function (index, item) {
    this.splice(index, 0, item);
    return true;
};


//sleep
function sleep(numberMillis) {
    var now = new Date();
    var exitTime = now.getTime() + numberMillis;
    while (true) {
        now = new Date();
        if (now.getTime() > exitTime)
            return;
    }
}

//获取文件扩展名
function getFileExt(str) {
    var d = /\.[^\.]+$/.exec(str);
    return d;
}

//获取文件的显示图标
function getFileIcon(ext) {
    ext = ext.toString();
    var ext_img = [".jpg", ".jpeg", ".gif", ".png", ".bmp"];
    var ext_package = [".rar", ".zip"];
    var ext_media = [".mp4", ".mp3", ".3gp", ".flv", ".wav"];
    if ($.inArray(ext, ext_img) > -1) {
        return "/static/img/icon/img.png";
    } else if ($.inArray(ext, ext_package) > -1) {
        return "/static/img/icon/zip.png";
    } else if ($.inArray(ext, ext_media) > -1) {
        return "/static/img/icon/media.png";
    } else {
        return "/static/img/icon/text.png";
    }
}

//提示消息
function alert2(msg, type) {
    var _type = ["alert-info", "alert-success", "alert-error"];
    type = type == null || type == "" ? 0 : type;
    var rd = Math.random().toString();
    var alert_id = "alert_" + rd.substring(2, rd.length - 2);
    var html_alert = "";
    html_alert += "<div id=\"" + alert_id + "\" class=\"alert " + _type[type] + " fade hide in myalert\">";
    html_alert += "<button data-dismiss=\"alert\" class=\"close\" type=\"button\">×</button>";
    html_alert += "<strong>" + msg + "</strong>";
    html_alert += "</div>";
    $(html_alert).appendTo("body").fadeIn(500);
    setTimeout('$("#' + alert_id + '.alert").fadeOut(1000);', 3000);
    setTimeout('$("#' + alert_id + '.alert").remove();', 4000);
}

//按回车，评论框的高度自动增加
function setCommentTextarea(_this) {
    var _h = $(_this).height();
    //if(event.keyCode ==13){
    $(_this).height(_h + 16);
    //}
}

//获取两个时间差
function getDateDiff(strDateStart, strDateEnd, isHour) {
    isHour = isHour != null && isHour != "" ? isHour : false;
    var oDate1, oDate2;
    var iDays;
    var strDateS, strDateE;

    if (strDateStart == "" || strDateEnd == "")
        return "";

    if (isHour) {
        var time_start = strDateStart.split(' ');
        var time_end = strDateEnd.split(' ');
        oDate1 = time_start[0].split("-");
        oDate2 = time_end[0].split("-");
        strDateS = new Date(oDate1[0], oDate1[1] - 1, oDate1[2], time_start[1].split(':')[0], time_start[1].split(':')[1]);
        strDateE = new Date(oDate2[0], oDate2[1] - 1, oDate2[2], time_end[1].split(':')[0], time_end[1].split(':')[1]);
        iDays = parseInt((strDateS - strDateE) / 1000 / 60 / 60);//把相差的毫秒数转换为小时数
    } else {
        oDate1 = strDateStart.split("-");
        oDate2 = strDateEnd.split("-");
        strDateS = new Date(oDate1[0], oDate1[1] - 1, oDate1[2]);
        strDateE = new Date(oDate2[0], oDate2[1] - 1, oDate2[2]);
        iDays = parseInt((strDateS - strDateE) / 1000 / 60 / 60 / 24);//把相差的毫秒数转换为天数
    }
    return iDays;
}

//获取分页数据
var pageData = function (option, callback) {
    var op = {
        pageindex: 1,
        pagesize: 10,
        ispage: true,
        pagecontainer: $(".pagination"),
        pagecounts: 10,
        url: "",
        type: "get",
        callback: "",
        islogin: true,
        data: {}
    };
    $.extend(op, option);
    op.data['pageindex'] = op.pageindex;
    op.data['pagesize'] = op.pagesize;
    var _this = this;
    var ajax = null;
    //从URL地址获取页码
    setTimeout(function () {
        //从地址栏获取页码
        var hash_page = document.location.hash;
        if (hash_page != null && hash_page != "" && hash_page.indexOf("#page=") > -1) {
            var regx = /#page=\d+/;
            var page_hash = regx.exec(hash_page);
            page_hash = page_hash.toString().replace("#page=", "");
            if (page_hash != null && page_hash != "" && !isNaN(page_hash)) {
                op.data['pageindex'] = op.pageindex = parseInt(page_hash);
            }
        }
        //Ajax请求参数
        var param = {
            url: op.url,
            data: op.data,
            type: op.type,
            dataType: "json",
            contentType: "application/x-www-form-urlencoded; charset=utf-8",
            success: function (msg) {
                if (msg != null && msg != "") {
                    if (msg.code == -1 && op.islogin) {
                        showLogin();
                        return false;
                    }
                    //分页
                    var html_page = "";
                    if (msg.counts > op.pagesize)
                        html_page = _this.getPage(op, msg.counts);
                    if (op.pagecontainer != null && op.ispage && op.pagecontainer.length > 0) {
                        op.pagecontainer.html(html_page);
                    }
                    return callback(msg.data, msg.counts, html_page);
                } else {
                    return callback(msg, 0, "");
                }
            }
        };
        ajax = $.ajax(param);
    }, 300);

    //取消请求
    this.abort = function () {
        if (ajax != null) {
            ajax.abort();
        }
    }
};

//获取分页
pageData.prototype.getPage = function (op, counts) {
    var pagesize = op.pagesize;
    var pageindex = op.pageindex;
    var callback = op.callback;
    var pagecount = 0;
    var hash_othors = "";//链接的其他标识
    if (document.location.hash != null && document.location.hash != "") {
        var regx = /#page=\d+/;
        var page_hash = regx.exec(document.location.hash);
        hash_othors = document.location.hash.toString().replace(page_hash, "");
    }

    //计算总页数
    if (counts % pagesize == 0) {
        pagecount = Math.floor(counts / pagesize);
        pagecount = pagecount == 0 ? 1 : pagecount;//至少一页
    } else {
        pagecount = Math.floor(counts / pagesize + 1);
    }
    var html = '<div>';
    html += '<ul class=\"pagination\">';
    //上一页
    if (pageindex > 1) {
        html += '<li><a href="#page=' + (pageindex - 1) + hash_othors + '" onclick="' + callback + '(' + (pageindex - 1) + ',\'' + op.url + '\')">上一页</a></li>';
    } else {
        html += '<li class="disabled"><a href="javascript:;">上一页</a></li>';
    }
    //页码
    if (pagecount < op.pagecounts) {
        for (var i = 1; i <= pagecount; i++) {
            html += '<li ' + (i == pageindex ? "class=\"active\"" : "") + '><a href="#page=' + i + hash_othors + '"  onclick="' + callback + '(' + i + ',\'' + op.url + '\')">' + i + '</a></li>';
        }
    } else {
        //断点页码
        var pagelist = [1, 2, 3, 4, 0, pagecount - 3, pagecount - 2, pagecount - 1, pagecount];
        if ($.inArray(pageindex, pagelist) < 0 || pageindex == 4 || pageindex == pagecount - 3) {
            if (pageindex == 4) {
                pagelist = [1, 2, pageindex - 1, pageindex, pageindex + 1, 0, pagecount - 1, pagecount];
            } else if (pageindex == pagecount - 3) {
                pagelist = [1, 2, 0, pageindex - 1, pageindex, pageindex + 1, pagecount - 1, pagecount];
            }
            else {
                pagelist = [1, 2, 0, pageindex - 1, pageindex, pageindex + 1, 0, pagecount - 1, pagecount];
            }
        }
        var pagelength = pagelist.length;
        for (var i = 0; i < pagelength; i++) {
            if (pagelist[i] == 0) {
                html += '<li><span>...</span></li>';
            } else {
                html += '<li ' + (pagelist[i] == pageindex ? "class=\"active\"" : "") + '><a href="#page=' + pagelist[i] + hash_othors + '"  onclick="' + callback + '(' + pagelist[i] + ',\'' + op.url + '\')">' + pagelist[i] + '</a></li>';
            }
        }
    }
    //下一页
    if (pageindex < pagecount) {
        html += '<li><a href="#page=' + (pageindex + 1) + hash_othors + '" onclick="' + callback + '(' + (pageindex + 1) + ',\'' + op.url + '\')">下一页</a></li>';
    } else {
        html += '<li class="disabled"><a href="javascript:;">下一页</a></li>';
    }
    html += '</ul>';
    html += '</div>';
    return html;
};

//搜索时，页码初始第一页
function initSearchPage() {
    if (document.location.hash != null && document.location.hash != "" && document.location.hash.indexOf("#page") > -1) {
        var regx = /#page=\d+/;
        var page_hash = regx.exec(document.location.hash);
        document.location.hash = document.location.hash.toString().replace(page_hash, "#page=1");
    }
}

//ajax请求数据,rest
var Ajax = function (url, option, callback) {
    var op = {
        url: url,
        type: "post",
        data: {},
        islogin: true
    };
    $.extend(op, option);
    //Ajax请求参数
    var param = {
        url: op.url,
        data: op.data,
        type: op.type,
        dataType: "json",
        contentType: "application/x-www-form-urlencoded; charset=utf-8",
        success: function (msg) {
            if (msg != null && msg != "") {
                if (msg.code == -1 && op.islogin) {
                    showLogin();
                    return false;
                }
                return callback(msg);
            } else {
                return callback(null);
            }
        }
    };
    $.ajax(param);
};

//获取网络请求结果
function getResult(msg, action) {
    if (msg != null && msg != "") {
        if (action == null)action = "操作";
        if (msg == -1) {
            showLogin();//登入
            return false;
        } else {
            msg = eval("(" + msg + ")");
            if (msg.result > 0) {
                alert2(action + "成功！", 1);
                return true;
            } else {
                alert2(action + "失败！" + getErrorMsg(msg.error_code), 2);
            }
        }
    } else {
        alert2('网络请求失败，请检查网络。')
    }
    return false;
}

//指定日期转换时间戳
function js_strto_time(str_time) {
    var new_str = str_time.replace(/:/g, '-');
    new_str = new_str.replace(/\//g, '-');
    new_str = new_str.replace(/ /g, '-');
    var arr = new_str.split("-");
    if (arr.length < 4) {
        arr[3] = arr[4] = arr[5] = "00";
    } else if (arr.length == 4) {
        arr[5] = "00";
    }
    var datum = new Date(Date.UTC(arr[0], arr[1] - 1, arr[2], arr[3] - 8, arr[4], arr[5]));
    return datum.getTime() / 1000;
}

//时间戳转换日期
function getLocalTime(timestamp) {
    if (timestamp != null && timestamp != "") {
        return new Date(parseInt(timestamp) * 1000).toLocaleString().replace(/:\d{1,2}$/, ' ');
    }
    return "";
}

//时间戳转换标准日期
function formateTime(timestamp, isShhort) {
    if (timestamp != null && timestamp != "") {
        var date = new Date(parseInt(timestamp) * 1000);
        if (typeof isShhort != "undefined" && isShhort != "" && isShhort) {
            return date.toLocaleDateString();
        } else {
            var time = "";
            if (date.getHours() > 0) {
                var hours = date.getHours(),
                    minutes = date.getMinutes(),
                    seconds = date.getSeconds();
                hours = hours > 9 ? hours : "0" + hours;
                minutes = minutes > 9 ? minutes : "0" + minutes;
                seconds = seconds > 9 ? seconds : "0" + seconds;
                time = hours + ":" + minutes + ":" + seconds;
            }
            return date.toLocaleDateString() + " " + time;
        }
    }
    return "";
}

//社交时间
function getGamTime(timestamp) {
    var myDate = new Date();
    var now = myDate.getTime();//当前时间戳
    var today = new Date(myDate.toLocaleDateString()).getTime();//今天的时间戳
    //var today = js_strto_time("2015/03/18 01:00:00");
    var yesterday = today - 3600 * 24 * 1000;
    var timestampJS = new Date(parseInt(timestamp) * 1000).getTime();
    //alert(timestamp);
    //var thisYear
    var date = new Date(parseInt(timestamp) * 1000);
    var day = date.getDate(),
        hours = date.getHours(),
        minutes = date.getMinutes();
    if (hours < 10) {
        hours = "0" + hours;
    }
    if (minutes < 10) {
        minutes = "0" + minutes;
    }
    if (timestampJS >= today) {
        //今天
        return "今天" + hours + ":" + minutes;
    } else if (timestampJS >= yesterday) {
        //昨天
        return "昨天" + hours + ":" + minutes;
    } else {
        //今年
        return (date.getMonth() + 1) + "月" + day + "日\t" + hours + ":" + minutes;
    }
}

//文件大小格式化
function formatFileSize(fileseze) {
    if (!isNaN(fileseze)) {
        if (fileseze >= 1024 * 1024) {
            return toDecimal(fileseze / (1024 * 1024)) + "\tMB";
        }else if (fileseze >= 1024) {
            return toDecimal(fileseze / 1024) + "\tKB";
        }else {
            return fileseze + "\t字节";
        }
    }
    return "--";
}

//保留两位小数点
function toDecimal(x) {
    var f = parseFloat(x);
    if (isNaN(f)) {
        return;
    }
    f = Math.round(x*100)/100;
    return f;
}

//判断登入
function checkLogin(isopenLogin) {
    var islogin = false;
    $.ajax({
        url: "/api/user/checklogin/",
        async: false,
        success: function (msg) {
            if (msg != null && msg != "") {
                if (msg == "True") {
                    islogin = true;
                } else {
                    islogin = false;
                    if (isopenLogin != null && isopenLogin) {
                        //打开登入对话框
                        showLogin();
                    }
                }
            }
        }
    });
    return islogin;
}

//打开登入对话框
function showLogin() {
    if ($("#login_modal").length < 1) {
        var username = "";
        if ($.cookie("username") != null && $.cookie("username") != "")username = $.cookie("username");
        var html = "";
        html += "<div id=\"login_modal\" class=\"modal hide\" style=\"width:360px;z-index:1052;\">";
        html += '<div class="modal-header">';
        html += '<button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>';
        html += '<p style="margin: 0;">';
        html += "<h3>登入</h3>";
        html += '</p>';
        html += '</div>';
        html += "<div class=\"modal-body\" style=\"overflow-y: inherit;\">";
        html += "<form class=\"form-horizontal\">";
        html += "<div class=\"control-group\">";
        html += "<label for=\"inputEmail\" class=\"control-label\">用户名</label>";
        html += "<div class=\"controls\">";
        html += "<input type=\"text\" placeholder=\"用户名\" value=\"" + username + "\" id=\"inputEmail\" name=\"username\" style=\"ime-mode: disabled;\">";
        html += "</div>";
        html += "</div>";
        html += "<div class=\"control-group\">";
        html += "<label for=\"inputPassword\" class=\"control-label\">密码</label>";
        html += "<div class=\"controls\">";
        html += "<input type=\"password\" value=\"\" placeholder=\"密码\" id=\"inputPassword\" name=\"password\" onkeyup=\"if(event.keyCode ==13)login();\">";
        html += "</div>";
        html += "</div>";
        html += "</form>";
        html += "<div class=\"alert hide\" style=\"margin:2px;\"></div>";
        html += "</div>";
        html += "<div class=\"modal-footer\">";
        html += "<a href=\"javascript:;\" name=\"a_btn_submit\" class=\"btn btn-info\" onclick=\"login();\">登入</a>";
        html += "<a href=\"javascript:;\" class=\"btn a_close\" data-dismiss=\"modal\" aria-hidden=\"true\">取消</a>";
        html += "</div>";
        html += "</div>";
        //填充
        $("body").append(html);
    }
    $("#login_modal input[name=password]").val("");
    //显示弹框
    $("#login_modal").modal('show');
    //初始化弹框
    if ($("#login_modal input[name=username]").val() == "") {
        $("#login_modal input[name=username]").focus();
        return false;
    }
    if ($("#login_modal input[name=password]").val() == "") {
        $("#login_modal input[name=password]").focus();
        return false;
    }
    $("#login_modal div.alert").text("").addClass("hide").removeClass("alert-success");
    return false;
}

//登入
function login() {
    var username = $.trim($("#login_modal input[name=username]").val());
    var password = $.trim($("#login_modal input[name=password]").val());
    if (username == "") {
        $("#login_modal input[name=username]").focus();
        return false;
    }
    if (password == "") {
        $("#login_modal input[name=password]").focus();
        return false;
    }
    var csrftoken = $.cookie('csrftoken');
    //加密
    $.getScript("/static/js/md5.js", function () {
        password = hex_md5(password);
        //login
        $.post("/api/user/login/", {username: username, password: password, csrftoken: csrftoken}, function (msg) {
            if (msg != null && msg != "") {
                if (msg.result) {
                    $("#login_modal div.alert").text("登入成功。").removeClass("hide").addClass("alert-success");
                    setTimeout('close_login_dialog();', 720);
                    $("#login_modal div.alert").text("").addClass("hide").removeClass("alert-success");
                } else {
                    $("#login_modal div.alert").text("登入失败，请检查用户名或密码。").removeClass("hide");
                }
            }
        });
    })

}
//取消登入
function close_login_dialog() {
    $("#login_modal").modal('hide');
}


//检查能否播放HTML视频
function checkVideo() {
    if (!!document.createElement('video').canPlayType) {
        var vidTest = document.createElement("video");
        oggTest = vidTest.canPlayType('video/ogg; codecs="theora, vorbis"');
        if (!oggTest) {
            h264Test = vidTest.canPlayType('video/mp4; codecs="avc1.42E01E, mp4a.40.2"');
            if (!h264Test) {
                return false;
            } else {
                if (h264Test == "probably") {
                    return true;
                } else {
                    return true;
                }
            }
        } else {
            if (oggTest == "probably") {
                return true;
            } else {
                return true;
            }
        }
    }
    else {
        return false;
    }
    return false;
}
