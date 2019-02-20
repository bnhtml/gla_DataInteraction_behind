// ------------------- 分页 --------------------------
//记录当前展示的页数的索引页，比如页数1 - 10，索引值是0 - 9
var index = 0;
//i记录一共生成了多少页，比如生成10页后，i最后会变成11，因为等于11的时候会结束for循环
var i;
//前或后显示的页码数量
var showPages = 0;
//一共显示的页码数量
var showAll = 0;
//拼接要显示的所有页码的jquery选择条件
var pageStr = '';
//循环页码数字
var page = 0;
//如果总页数小于等于5页时等于false，大于5页时等于true
var fewPages = true;
//匹配1~99的正整数
var reg_pagNum = /^\+?[1-9][0-9]*$/;
//数据库
var database;
//表名
var table_name;
//绑定位置
var bindPlace;
//操作页面
var handle;
//页码元素
var moveli;
//最新总页数
var newPageNum = 0;
//旧的总页数
var oldPageNum = 0;
//防止快速点击
var lock = true;
//部门
var depart;
//记录上一个页码
var report;
//每页显示多少页
var page_EachNum;
// 初始化绑定页码的锁
var pageCount_lock = true;
var qufen = 1;
// 搜索关键条件
var table_keys;
//paging函数设置总页数和显示的页码数量，第一个参数为总页数，第二个参数为显示的页码数量
//显示的页码不得大于总页数，当总页数大于5页时，显示的页码必须为单数(为了美观)
// paging(16,3);
//pageTotal总页数，displayPageNum显示的页码数量
function paging(pageTotal, displayPageNum) {
    //传入总页数生成页码pageTotal,传入要显示的页码总数displayPageNum
    if (reg_pagNum.test(pageTotal) && reg_pagNum.test(displayPageNum)) {
        //当总页数小于等于5页时
        if (pageTotal <= 5) {
            //不完全开启页码运动
            fewPages = false;
            //传入相同的总页数和一共显示的页码数量
            bindPageNum(pageTotal, pageTotal);
            //删除前后...
            $("#spanleft").remove();
            $("#spanright").remove();
            //要显示的页码小于等于总页数，并且要显示的页码为单数并大于等于3页(为了美观)
        } else if (displayPageNum <= pageTotal && (displayPageNum % 2) != 0 && displayPageNum >= 3) {
            //完全开启页码运动
            fewPages = true;
            bindPageNum(pageTotal, displayPageNum);
        }
    }
}

function set_PageData(database, table_name, bindPlace, page, moveli, each_num, depart,search_con,where_keys) {
    page_EachNum = each_num;
    var params = {
        "database": database,
        "table_name": table_name,
        "page": page,
        "each_num": each_num
    }
    if (depart) {
        params.depart = depart;
    }
    if (search_con && where_keys) {
        params.search = search_con;
        params.table_keys = where_keys;
    }
    // console.log(params);
    $.post("/commonUser/page_nation/", params, function (data) {
        // console.log(data);
        newPageNum = data.pageCount;
        //设置当前数据总条数
        $("#allpage").html("共&nbsp;" + newPageNum + "&nbsp;页&nbsp;" + data.allDataNum + "&nbsp;条");
        bindPageM();
        bindDatas(data.result, bindPlace);
        lock = true;
    });
}
function bindPageM() {
    if (qufen == 1) {
        // console.log(newPageNum);
        paging(newPageNum, 5);
    }
}

function bindDatas(data, bindPlace) {
    $(bindPlace).html('');
    var pag_Str = '';
    var i;
    var j;
    switch (handle) {
        case "commonUser_service_list":
            for (i = 0; i < data.length; i++) {
                pag_Str += "<div class='row break'>";
                // pag_Str += "<div class='col-xs-1 col-md-1'>";
                // pag_Str += "<input type='checkbox' name='item' id='server_name_id' value=''/>";
                // pag_Str += "</div>";
                pag_Str += "<div class='col-xs-1 col-md-1' id='id'>" + ((getPageNum() - 1) * page_EachNum + 1 + i) + "</div>";
                pag_Str += "<div class='col-xs-2 col-md-2' id='serviceName' title=" + data[i][1] + ">" + data[i][1] + "</div>";
                pag_Str += "<div class='col-xs-2 col-md-2' id='hosts' title=" + data[i][2] + ">" + data[i][2] + " </div>";
                pag_Str += "<div class='col-xs-3 col-md-3' id='uris' title=" + data[i][3] + ">" + data[i][3] + "</div>";
                pag_Str += "<div class='col-xs-2 col-md-2' id='upstream_url' title=" + data[i][5] + ">" + data[i][5] + "</div>";
                pag_Str += "<div class='col-xs-2 col-md-2'>";
                pag_Str += "<input type='button' name='' class='data_del' style='color: #409eff;' id='update_upd' value='修改'>";
                pag_Str += "<input style='margin-left:15px;' type='button' name='' class='data_del' value='删除' id='del_tr'/>";
                pag_Str += "</div></div>";
            }
            break;
        case "commonUser_acl_list":
            for (i = 0; i < data.length; i++) {
                pag_Str += "<div class='row break'>";
                // pag_Str += "<div class='col-xs-2 col-md-2'>";
                // pag_Str += "<input type='checkbox' name='item' id='server_name_id' value=''/>";
                // pag_Str += "</div>";
                pag_Str += "<div class='col-xs-2 col-md-2' id='id'>" + ((getPageNum() - 1) * page_EachNum + 1 + i) + "</div>";
                pag_Str += "<div class='col-xs-4 col-md-4' id='serviceName' title=" + data[i][1] + ">" + data[i][1] + "</div>";
                pag_Str += "<div class='col-xs-4 col-md-4' id='whitelist' title=" + data[i][3] + ">" + data[i][3] + "</div>";
                pag_Str += "<div class='col-xs-2 col-md-2'>";
                pag_Str += "<input type='button' name='' class='data_del' style='color: #409eff;' id='update_upd' value='修改'>";
                pag_Str += "<input style='margin-left:15px;' type='button' name='' class='data_del' value='删除' id='del_tr'/>";
                pag_Str += "</div></div>";
            }
            break;
        case "commonUser_control_list":
            for (i = 0; i < data.length; i++) {
                pag_Str += "<div class='row break'>";
                // pag_Str += "<div class='col-xs-1 col-md-1'>";
                // pag_Str += "<input type='checkbox' name='item' id='server_name_id' value=''/>";
                // pag_Str += "</div>";
                pag_Str += "<div class='col-xs-1 col-md-1' id='id'>" + ((getPageNum() - 1) * page_EachNum + 1 + i) + "</div>";
                pag_Str += "<div class='col-xs-2 col-md-2' id='name' title=" + data[i][1] + ">" + data[i][1] + "</div>";
                pag_Str += "<div class='col-xs-2 col-md-2' id='consumer_id' title=" + data[i][2] + ">" + data[i][2] + "</div>";
                pag_Str += "<div class='col-xs-3 col-md-3' id='serviceName' title=" + data[i][4] + ">" + data[i][4] + "</div>";
                pag_Str += "<div class='col-xs-2 col-md-2' id='day' title=" + data[i][5] + ">" + data[i][5] + "</div>";
                pag_Str += "<div class='col-xs-2 col-md-2'>";
                pag_Str += "<input type='button' name='' class='data_del' style='color: #409eff;' id='update_upd' value='修改'>";
                pag_Str += "<input style='margin-left:15px;' type='button' name='' class='data_del' value='删除' id='del_tr'/>";
                pag_Str += "</div></div>";
            }
            break;
        case "journal":
            for (i = 0; i < data.length; i++) {
                pag_Str += "<div class='row break'>";
                pag_Str += "<div class='col-xs-1 col-md-1'>" + ((getPageNum() - 1) * page_EachNum + 1 + i) + "</div>";
                pag_Str += "<div class='col-xs-2 col-md-2' title=" + data[i][1] + ">" + data[i][1] + "</div>";
                pag_Str += "<div class='col-xs-2 col-md-2' title=" + data[i][2] + ">" + data[i][2] + "</div>";
                pag_Str += "<div class='col-xs-2 col-md-2' title=" + data[i][3] + ">" + data[i][3] + "</div>";
                pag_Str += "<div class='col-xs-2 col-md-2' title=\"" + data[i][4] + "\">" + data[i][4] + "</div>";
                pag_Str += "<div class='col-xs-2 col-md-2' title=\"" + data[i][5] + "\">" + data[i][5] + "</div>";
                pag_Str += "<div class='col-xs-1 col-md-1'>" + data[i][6] + "</div>";
                pag_Str += "</div>";
            }
            break;
        case "departAdmin_sql_admin":
            for (i = 0; i < data.length; i++) {
                pag_Str += "<div class='row break'>";
                // pag_Str += "<div class='col-xs-1 col-md-1'>";
                // pag_Str += "<input type='checkbox' name='item' id='server_name_id' value=''/>";
                // pag_Str += "</div>";
                pag_Str += "<div class='col-xs-1 col-md-1 id'>" + ((getPageNum() - 1) * page_EachNum + 1 + i) + "</div>";
                pag_Str += "<div class='col-xs-2 col-md-2 dbName' title=" + data[i][1] + ">" + data[i][1] + "</div>";
                pag_Str += "<div class='col-xs-4 col-md-4 dbSql' title=\"" + data[i][2].replace(/["]+/g, "&quot;") + "\">" + data[i][2] + "</div>";
                pag_Str += "<div class='col-xs-3 col-md-3 dbIP' title=" + data[i][3] + ">" + data[i][3] + "</div>";
                pag_Str += "<div class='col-xs-2 col-md-2'>";
                pag_Str += "<input type='button' name='' class='data_del' style='color: #409eff;' id='update_upd' value='修改'>";
                // pag_Str += "<input type='button' name='' class='data_del' value='删除' id='del_tr'/>";
                pag_Str += "</div></div>";
            }
            break;
        case "departAdmin_admin_file":
            for (i = 0; i < data.length; i++) {
                pag_Str += "<div class='row break'>";
                // pag_Str += "<div class='col-xs-2 col-md-2'>";
                // pag_Str += "<input type='checkbox' name='item' id='server_name_id' value=''/>";
                // pag_Str += "</div>";
                pag_Str += "<div class='col-xs-2 col-md-2' id='id'>" + ((getPageNum() - 1) * page_EachNum + 1 + i) + "</div>";
                pag_Str += "<div class='col-xs-4 col-md-4' id='name' title=" + data[i][1] + ">" + data[i][1] + "</div>";
                pag_Str += "<div class='col-xs-4 col-md-4' id='ip' title=" + data[i][2] + ">" + data[i][2] + "</div>";
                pag_Str += "<div class='col-xs-2 col-md-2'>";
                pag_Str += "<input type='button' name='' class='data_del' style='color: #409eff;' id='update_upd' value='修改'>";
                pag_Str += "<input style='margin-left:15px;' type='button' name='' class='data_del' value='删除' id='del_tr'/>";
                pag_Str += "</div></div>";
            }
            break;
        case "departAdmin_admin_interface":
            for (i = 0; i < data.length; i++) {
                pag_Str += "<div class='row break'>";
                // pag_Str += "<div class='col-xs-2 col-md-2'>";
                // pag_Str += "<input type='checkbox' name='item' id='server_name_id' value=''/>";
                // pag_Str += "</div>";
                pag_Str += "<div class='col-xs-2 col-md-2' id='id'>" + ((getPageNum() - 1) * page_EachNum + 1 + i) + "</div>";
                pag_Str += "<div class='col-xs-4 col-md-4' id='name' title=" + data[i][1] + ">" + data[i][1] + "</div>";
                pag_Str += "<div class='col-xs-4 col-md-4' id='ip' title=" + data[i][2] + ">" + data[i][2] + "</div>";
                pag_Str += "<div class='col-xs-2 col-md-2'>";
                pag_Str += "<input type='button' name='' class='data_del' style='color: #409eff;' id='update_upd' value='修改'>";
                pag_Str += "<input style='margin-left:15px;' type='button' name='' class='data_del' value='删除' id='del_tr'/>";
                pag_Str += "</div></div>";
            }
            break;
        case "departAdmin_admin_ways":
            for (i = 0; i < data.length; i++) {
                pag_Str += "<div class='row break'>";
                // pag_Str += "<div class='col-xs-2 col-md-2'>";
                // pag_Str += "<input type='checkbox' name='item' id='server_name_id' value=''/>";
                // pag_Str += "</div>";
                pag_Str += "<div class='col-xs-2 col-md-2' id='id'>" + ((getPageNum() - 1) * page_EachNum + 1 + i) + "</div>";
                pag_Str += "<div class='col-xs-4 col-md-4' id='name' title=" + data[i][1] + ">" + data[i][1] + "</div>";
                pag_Str += "<div class='col-xs-4 col-md-4' id='ip' title=" + data[i][2] + ">" + data[i][2] + "</div>";
                pag_Str += "<div class='col-xs-2 col-md-2'>";
                pag_Str += "<input type='button' name='' class='data_del' style='color: #409eff;' id='update_upd' value='修改'>";
                pag_Str += "<input style='margin-left:15px;' type='button' name='' class='data_del' value='删除' id='del_tr'/>";
                pag_Str += "</div></div>";
            }
            break;
        case "superAdmin_user_list":
            for (i = 0; i < data.length; i++) {
                pag_Str += "<div class='row break'>";
                // pag_Str += "<div class='col-xs-2 col-md-2'>";
                // pag_Str += "<input type='checkbox' name='item' id='server_name_id' value=''/>";
                // pag_Str += "</div>";
                pag_Str += "<div class='col-xs-2 col-md-2' id='id'>" + ((getPageNum() - 1) * page_EachNum + 1 + i) + "</div>";
                pag_Str += "<div class='col-xs-5 col-md-5' id='name' title=" + data[i][1] + ">" + data[i][1] + "</div>";
                pag_Str += "<div class='col-xs-5 col-md-5' id='apikey' title=" + data[i][2] + ">" + data[i][2] + "</div>";
                // pag_Str += "<div class='col-xs-2 col-md-2'>";
                // pag_Str += "<input type='button' name='' class='data_del' style='color: #00cd00;' id='update_upd' value='修改'>";
                // pag_Str += "<input type='button' name='' class='data_del' value='删除' id='del_tr'/>";
                pag_Str += "</div>";
            }
            break;
        case "superAdmin_service_list":
            for (i = 0; i < data.length; i++) {
                pag_Str += "<div class='row break'>";
                // pag_Str += "<div class='col-xs-1 col-md-1'>";
                // pag_Str += "<input type='checkbox' name='item' id='server_name_id' value=''/>";
                // pag_Str += "</div>";
                pag_Str += "<div class='col-xs-1 col-md-1' id='id'>" + ((getPageNum() - 1) * page_EachNum + 1 + i) + "</div>";
                pag_Str += "<div class='col-xs-2 col-md-2' id='serviceName' title=" + data[i][1] + ">" + data[i][1] + "</div>";
                pag_Str += "<div class='col-xs-2 col-md-2' id='hosts' title=" + data[i][2] + ">" + data[i][2] + "</div>";
                pag_Str += "<div class='col-xs-3 col-md-3' id='uris' title=" + data[i][3] + ">" + data[i][3] + "</div>";
                pag_Str += "<div class='col-xs-2 col-md-2' id='upstream_url' title=" + data[i][5] + ">" + data[i][5] + "</div>";
                pag_Str += "<div class='col-xs-2 col-md-2'>";
                pag_Str += "<input type='button' name='' class='data_del' style='color: #409eff;' id='update_upd' value='修改'>";
                pag_Str += "<input style='margin-left:15px;' type='button' name='' class='data_del' value='删除' id='del_tr'/>";
                pag_Str += "</div></div>";
            }
            break;
        case "status_journal":
            for (i = 0; i < data.length; i++) {
                pag_Str += "<div class='row break'>";
                pag_Str += "<div class='col-xs-1 col-md-1'>" + ((getPageNum() - 1) * page_EachNum + 1 + i) + "</div>";
                pag_Str += "<div class='col-xs-1 col-md-1' title=" + data[i][1] + ">" + data[i][1] + "</div>";
                pag_Str += "<div class='col-xs-2 col-md-2' title=\"" + data[i][2].replace(/T/, " ") + "\">" + data[i][2].replace(/T/, " ") + "</div>";
                pag_Str += "<div class='col-xs-1 col-md-1' title=" + data[i][3] + ">" + data[i][3] + "</div>";
                pag_Str += "<div class='col-xs-1 col-md-1' title=" + data[i][4] + ">" + data[i][4] + "</div>";
                pag_Str += "<div class='col-xs-2 col-md-2' title=" + data[i][5] + ">" + data[i][5] + "</div>";
                pag_Str += "<div class='col-xs-1 col-md-1' title=" + data[i][6] + ">" + data[i][6] + "</div>";
                pag_Str += "<div class='col-xs-1 col-md-1' title=" + data[i][7] + ">" + data[i][7] + "</div>";
                pag_Str += "<div class='col-xs-1 col-md-1' title=" + data[i][8] + ">" + data[i][8] + "</div>";
                pag_Str += "<div class='col-xs-1 col-md-1' title=" + data[i][9] + ">" + data[i][9] + "</div>";
                pag_Str += "</div>";
            }
            break;
    }
    $(bindPlace).append(pag_Str);
}


//此方法返回当前显示页数的索引值，+1表示正常的页数1 - 10
function getPageNum() {
    return index + 1;
}
//要显示的所有页码，从最左边的页码开始拼接jquery选择器语句
function moveCenter() {
    for (page = (index - showPages); page <= (index + showPages); page++) {
        if (page == (index - showPages)) {
            pageStr += '.moveLi:eq(' + page + ')';
        } else {
            pageStr += ',.moveLi:eq(' + page + ')';
        }
    }
}
//要显示的所有页码，从索引0的页开始拼接jquery选择器语句
function moveLeft() {
    pageStr = '';
    for (page = 0; page < showAll; page++) {
        if (page == 0) {
            pageStr += '.moveLi:eq(' + page + ')';
        } else {
            pageStr += ',.moveLi:eq(' + page + ')';
        }
    }
    $(pageStr).css("display", "inline-block");
}
//要显示的所有页码，从倒数第showAll位开始拼接jquery选择器语句
function moveRight() {
    pageStr = '';
    for (page = (i - 1 - showAll); page < (i - 1); page++) {
        if (page == (i - 1 - showAll)) {
            pageStr += '.moveLi:eq(' + page + ')';
        } else {
            pageStr += ',.moveLi:eq(' + page + ')';
        }
    }
    $(pageStr).css("display", "inline-block");
}
//页码运动
function moveContent() {
    //隐藏所有页码
    $("li.moveLi").css("display", "none");
    //jquery选择器语句清空
    pageStr = '';
    //当前要显示的页，大于等于左边可以显示的页码数量，小于等于右边可以显示的页码数量
    if (index >= showPages && index < (i - 1 - showPages)) {
        moveCenter();
        //当右边可以显示的页码数量不足时
    } else if (index > (i - 2 - showPages)) {
        moveRight();
        //当左边可以显示的页码数量不足时
    } else if (index < showPages) {
        moveLeft();
    }
    //将要显示的所有页码显示
    $(pageStr).css("display", "inline-block");
}
//修改前后...和首页尾页按钮
function updateSpanAndButton() {
    //当总页数小于等于5页时，会删除前后的... 此处判断...是否存在
    if ($("#spanleft")) {
        index > showPages ? $("#spanleft").css("display", "inline-block") : $("#spanleft").css("display", "none");
    }
    //当总页数小于等于5页时，会删除前后的... 此处判断...是否存在
    if ($("#spanright")) {
        index >= (i - 2 - showPages) ? $("#spanright").css("display", "none") : $("#spanright").css("display", "inline-block");
    }
    //当前页为第一页时，首页按钮禁止使用，否则可以使用
    index == 0 ? $("#shouye").attr("disabled", "disabled") : $("#shouye").removeAttr("disabled");
    //当前页为最后一页时，尾页按钮禁止使用，否则可以使用
    index == (i - 2) ? $("#weiye").attr("disabled", "disabled") : $("#weiye").removeAttr("disabled");
}
//页码初始化
function bindPageNum(pageTotal, displayPageNum) {
    $(".moveLi").remove();
    i = 1;
    //计算左右要显示的页码数量，减去最中间的一页，再除以2得到左右翼页码数量
    showPages = (displayPageNum - 1) / 2;
    //记录一共要显示的页码数量
    showAll = displayPageNum;
    //隐藏的页数部分由...显示
    // $("#xiayiye").before("<span id='spanleft' style='display: none;'>...</span>");
    for (i; i <= pageTotal; i++) {
        if (i == 1) {
            //第一页页码默认添加正在显示的样式move
            $("#xiayiye").before("<li class='active moveLi'>" + i + "</li>");
        } else if (i > displayPageNum) {
            //大于5页的页码隐藏
            $("#xiayiye").before("<li class='moveLi' style='display:none'>" + i + "</li>");
        } else {
            //添加正常显示的页码2~4页
            $("#xiayiye").before("<li class='moveLi'>" + i + "</li>");
        }
    }
    if(pageTotal == 1){
        $("#xiayiye").addClass("disabled");
    } else {
        $("#xiayiye").removeClass("disabled");
    }
    //隐藏的页数部分由...显示
    // $("#xiayiye").before("<span id='spanright'>...</span>");
}

$(document).ready(function () {
    // 点击每页N行
    $("#eachPage").click(function () {
        $(".eachPage_box").stop().slideToggle(200);
        $(this).toggleClass("selectedEach");
    });
    // 点击具体每页几行
    $(".eachPage_con ul").on("click", "li", function () {
        var othis = $(this);
        page_EachNum = parseInt($(othis).text());
        $("#eachPage>i").text($(othis).text().trim());
        if (!othis.hasClass("eachPage_selected")) {
            othis.addClass("eachPage_selected").siblings().removeClass("eachPage_selected");
            index = 0;
            qufen = 1;
            set_PageData(database, table_name, bindPlace, 1, moveli, page_EachNum, depart);
            // bindPageM(222);
        }
    });
    //给所有页码设置单击事件
    $(".padlr_right").on('click', 'li.moveLi', function () {
        if (index != parseInt($(this).text().trim()) - 1) {
            lock = true;
        } else {
            lock = false;
        }
        // report = $(this).text().trim();
        //点击除了正在显示的页码
        if (lock) {
            lock = false;
            if (index !== Number($(this).text()) - 1) {
                //点击当前页码，如果没有move样式则添加，否则删除move样式，并且其他兄弟页码全部删除move样式
                $(this).toggleClass("active").siblings().removeClass("active");
                //修改当前显示的页码
                index = Number($(this).text() - 1);
                if(index + 1 == 1 && index + 2 < i){
                    $("#shangyiye").addClass("disabled");
                    $("#xiayiye").removeClass("disabled");
                } else if (index == (i - 2) && index > 0) {
                    $("#xiayiye").addClass("disabled");
                    $("#shangyiye").removeClass("disabled");
                } else {
                    $("#shangyiye").removeClass("disabled");
                    $("#xiayiye").removeClass("disabled");
                }
                //修改当前显示的页数
                // $("#allpage").html("共&nbsp;" + (i - 1) + "&nbsp;条");
                if (fewPages) {
                    moveContent();
                }
                updateSpanAndButton();
                moveli = $(".moveLi");
                qufen = 2;
                set_PageData(database, table_name, bindPlace, getPageNum(), moveli, page_EachNum, depart);
            }
        }
    });
    //点击下一页时
    $(".padlr_right").on('click', '#xiayiye', function () {

        // lock = false;
        if (index + 2 != i) {
            $(this).removeClass("disabled");
            if(index + 3 == i){
                console.log("ok");
                $(this).addClass("disabled");
            }
            $("#shangyiye").removeClass("disabled");
            //点击下一页之前的页码删除展示样式
            $("li.moveLi:eq(" + index + ")").removeClass("active");
            index += 1;
            //点击下一页后要展示的页码添加展示样式
            $("li.moveLi:eq(" + index + ")").addClass("active");
            if (fewPages) {
                moveContent();
            }
            updateSpanAndButton();
            moveli = $(".moveLi");
            qufen = 2;
            set_PageData(database, table_name, bindPlace, getPageNum(), moveli, page_EachNum, depart);
        }

    });
    //点击上一页时
    $(".padlr_right").on('click', '#shangyiye', function () {

        if (index != 0) {
            $(this).removeClass("disabled");
            if(index == 1){
                $(this).addClass("disabled");
            }
            $("#xiayiye").removeClass("disabled");
            //之前展示的页码删除展示样式
            $("li.moveLi:eq(" + index + ")").removeClass("active");
            //索引值减1，代表跳转到上一页
            index -= 1;
            //上一页的页码添加展示样式
            $("li.moveLi:eq(" + index + ")").addClass("active");
            if (fewPages) {
                moveContent();
            }
            updateSpanAndButton();
            moveli = $(".moveLi");
            qufen = 2;
            set_PageData(database, table_name, bindPlace, getPageNum(), moveli, page_EachNum, depart);
        }

    });
    //点击首页
    // $(".padlr_right").on('click','#shouye',function () {
    //     // if(report == 0){
    //     //     lock = false;
    //     // } else {
    //     //     lock = true;
    //     // }
    //     // if(lock) {
    //         lock = false;
    //         //正在展示的页数不为首页时
    //         if (index != 0) {
    //             //之前的页码删除展示样式
    //             $("li.moveLi:eq(" + index + ")").removeClass("active");
    //             //首页页码添加展示样式
    //             $("li.moveLi:eq(0)").addClass("active");
    //             //修改当前页的索引值
    //             index = 0;
    //             //所有页码隐藏
    //             $("li.moveLi").css("display", "none");
    //             moveLeft();
    //             updateSpanAndButton();
    //             moveli = $(".moveLi");
    //             set_PageData(database,table_name,bindPlace,getPageNum(),moveli,depart);
    //         }
    //     // }
    // });
    //点击尾页
    // $(".padlr_right").on('click','#weiye',function () {
    //     // if(report != (i - 2)){
    //     //     lock = true;
    //     // } else {
    //     //     lock = false;
    //     // }
    //     // if(lock) {
    //     //     lock = false;
    //         //当前索引页不为最后一页时
    //         if (index != (i - 2)) {
    //             //之前展示的页码删除展示样式
    //             $("li.moveLi:eq(" + index + ")").removeClass("active");
    //             //最后一页页码添加展示样式
    //             $("li.moveLi:eq(" + (i - 2) + ")").addClass("active");
    //             //修改当前正在展示的索引值
    //             index = i - 2;
    //             //所有页码隐藏
    //             $("li.moveLi").css("display", "none");
    //             //最后五页显示
    //             moveRight();
    //             updateSpanAndButton();
    //             moveli = $(".moveLi");
    //             set_PageData(database,table_name,bindPlace,getPageNum(),moveli,depart);
    //         }
    //     // }
    // });
    //点击跳转按钮
    $(".padlr_right").on('click', '#jump', function () {
        //得到输入框里的值
        var num = Number($("#tiaozhuannum").val().replace(/\s/g, ''));
        if (num != (index + 1)) {
            //如果有值，并且是有效的页数数字
            if (reg_pagNum.test(num) && num <= (i - 1)) {
                //之前展示的页码删除展示样式
                $("li.moveLi:eq(" + index + ")").removeClass("active");
                //修改当前展示的页数的索引值
                index = num - 1;
                //按照输入框的数字-1得到相应页码的索引值，并且添加展示样式
                $("li.moveLi:eq(" + index + ")").addClass("active");
                if (fewPages) {
                    moveContent();
                }
                updateSpanAndButton();
                // $("#allpage").text((index + 1) + "/共" + (i - 1) + "页");
                moveli = $(".moveLi");
                qufen = 2;
                set_PageData(database, table_name, bindPlace, getPageNum(), moveli, page_EachNum, depart);
            } else if (reg_pagNum.test(num) && num > (i - 1)) {
                layer.alert("请输入存在的页数：");
            } else {
                layer.alert("请输入正确的页数：");
            }
        }
        if(i - 1 == 1) {
            $("#shangyiye").addClass("disabled");
            $("#xiayiye").addClass("disabled");
        } else if(num == (i - 1)) {
            $("#xiayiye").addClass("disabled");
            $("#shangyiye").removeClass("disabled");
        } else if(num == 1) {
            $("#shangyiye").addClass("disabled");
            $("#xiayiye").removeClass("disabled");
        }
        // if(num == 1){
        //     $("#shangyiye").addClass("disabled");
        // }
        // if(num == (i - 1)){
        //     $("#xiayiye").addClass("disabled");
        // }
    });
    $("#search_btnOK").click(function(){
        var serach_data = $("#search_input").val();
        set_PageData(database, table_name, bindPlace, 1, moveli,10, depart,serach_data,table_keys);
    });
    $("#search_input").bind('keypress',function(event){
        if(event.keyCode == "13"){
            $("#search_btnOK").click();
        }
    });

    $("#tiaozhuannum").bind('keypress',function(event){
        if(event.keyCode == "13"){
            $("#jump").click();
        }
    });
});


