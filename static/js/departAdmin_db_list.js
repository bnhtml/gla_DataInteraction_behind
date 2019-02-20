var depart;
var interface_Depart;
var interface_Parent;
var interface_Num;

$(function () {

    //传入后端的部门名称
    var nowPath = $(".path");
    var menu_lock = true;
    var reg = /^[\u4e00-\u9fa5]+$/;
    var allData = $(".nav_right_content").html();
    var navRightHead = $(".nav_right_head_txt");
    var navRightInter = $(".nav_right_head_inter");
    var navRightContent = $(".nav_right_content");
    var dataStr = "";
    // 当前路径
    var classA = $(".classA"),
        classB = $(".classB"),
        classC = $(".classC"),
        classD = $(".classD"),
        classAIcon = $(".classAIcon"),
        classBIcon = $(".classBIcon"),
        classCIcon = $(".classCIcon");
    $("#left_menu").click(function () {
        if (menu_lock) {
            menu_lock = false;
            $(".leftnav").stop().animate({ "margin-left": "-309px" }, 400);
            $(this).addClass("menuActive");
        } else {
            menu_lock = true;
            $(".leftnav").stop().animate({ "margin-left": "0px" }, 400);
            $(this).removeClass("menuActive");
        }
    });
    $(".header_nav").on("click","ul>li>div",function(){
        console.log(1);
        var othis = $(this);
        // othis.addClass("clickDiv");
        othis.css({"border-color":"#58cafd","font-weight":"700"}).parent().siblings().find("div").css({"border-color":"transparent","font-weight":"normal"});
        // othis.addClass("clickDiv").parent().siblings().find(".clickDiv").removeClass("clickDiv");
        if($(othis).attr("class") == "dataAreaManage") {
            $.post("/loginEsgyn/",function (data) {                
                window.open("https://59.215.191.26:4206/#/login?" + data.result);
            });
        } else if ($(othis).attr("class") == "dataPrep") {
            $("#dataIntegrate").click();
        } else if ($(othis).attr("class") == "systemStatus") {
            if($("#auditAnalysis").length) {
                $("#auditAnalysis").click();
            } else {
                $("#journal").click();
            }
            
        }
    });
    // $(".leftnav").on("click",">div",function(){
    //     var othis = $(this);
    //     othis.next("ul").slideToggle(400);
    //     othis.find(".icon-angle-down").toggleClass("rotatez");
    // });
    $(".nav_left_title").click(function (e) {
        e.stopPropagation();
    });
    $(".leftnav .nav_left").on("click", ">ul li", function (e) {
        console.log(2);
        e.stopPropagation();
        var othis = $(this);
        classA.text(othis.attr("value")).nextAll().css("display", "none");
        if (!$(othis).attr("class")) {
            if ($(othis).parent("a").length) {
                $(othis).addClass("navClick").parent("a").siblings().removeClass("navClick");
            } else {
                $(othis).toggleClass("navClick").siblings().removeClass("navClick");
                $(othis).siblings("a").find("li").removeClass("navClick");
            }
        }
        navLeftBindData(othis);
    });
    //点击一级目录
    $(".nav_right_content").on("click", ">ul li.firstDier", function () {
        var othis = $(this);
        depart = $(othis).find(".nav_right_firstName").text().trim();
        interface_Depart = othis.find(".interNum");
        pathNone();
        othis.next("ul").siblings("ul").slideUp(200).find("ul").slideUp(200).end().find(".rotatez").removeClass("rotatez");
        othis.next("ul").siblings("ul").find(".thirdClick").removeClass("thirdClick");
        $(classAIcon).css("display", "inline-block");
        $(classB).text($(othis).find(".nav_right_firstName").text().trim()).css("display", "inline-block");
        $(classB).nextAll().css("display", "none");
        if (othis.next("ul").length) {
            othis.next("ul").slideToggle(200);
            othis.find(">div.icon").find("span.icon-angle-down").toggleClass("rotatez");
        }
        $.post('/admin_db/', { "depart": depart });
    });
    //点击二级目录
    $(".nav_right_content").on("click", ">ul>ul li.secondDier", function () {
        var othis = $(this);
        interface_Parent = othis.find(".interNum");
        $(classAIcon).css("display", "inline-block");
        $(classB).text($($(this).parents("ul")[0]).prev().find(".nav_right_firstName").text().trim()).css("display", "inline-block");
        $(classBIcon).css("display", "inline-block");
        $(classC).text($(othis).find(".nav_right_secondName").text().trim()).css("display", "inline-block");
        $(classC).nextAll().css("display", "none");
        if (othis.next("ul").length) {
            othis.next("ul").slideToggle(200);
            othis.find(">div.icon").find("span.icon-angle-down").toggleClass("rotatez");
        }
    });
    //点击三级目录
    $(".nav_right_content").on("click", ">ul>ul>ul li.thirdDier", function () {
        var othis = $(this);
        interface_Parent = $(othis.parents("ul")[0]).prev().find(".interNum");
        interface_Num = othis.find(".interNum");
        $(classAIcon).css("display", "inline-block");
        $(classB).text($($(othis).parents("ul")[0]).parent().prev().find(".nav_right_firstName").text().trim()).css("display", "inline-block");
        $(classBIcon).css("display", "inline-block");
        $(classC).text($($(othis).parents("ul")[0]).prev().find(".nav_right_secondName").text().trim()).css("display", "inline-block");
        $(classCIcon).css("display", "inline-block");
        $(classD).text($(othis).find(".nav_right_thirdName").text().trim()).css("display", "inline-block");
        //没写完的功能
        if (!$(othis).hasClass("thirdClick")) {
            $(othis).addClass("thirdClick").parent().siblings().find("li").removeClass("thirdClick");
            $($(othis).parents("ul")[0]).siblings("ul").find(".thirdClick").removeClass("thirdClick");
        }
        if (othis.next("ul").length) {
            othis.next("ul").slideToggle(200);
        }
    });

    $(".nav_right_content").on("click","#esg",function(){
        $.post("/loginEsgyn/",function (data) {                
            window.open("https://59.215.191.26:4206/#/login?" + data.result);
        });
    });


    $("#addDepartment").click(function (e) {
        e.stopPropagation();
        kg = true;
        layer.open({
            area: ["400px", "180px"],
            title: "添加部门",
            content: $(".add_depart"),
            type: 1,
            btn: ["添加", "取消"],
            yes: function (index) {
                layer.confirm('确认添加吗？', {
                    title: "提示",
                    btn: ["确定", "取消"],
                    yes: function (index) {
                        layer.close(index - 1);
                        var value = $("#depart_sel option:selected").text().trim();
                        if (reg.test(value.replace(/\s/g, ''))) {
                            var str = '';
                            var fk;
                            if (value != '') {
                                layer.open({
                                    area: ['500px', '100px'],
                                    title: "正在添加，请稍后...",
                                    content: $('.progressBar'),
                                    type: 1,
                                    closeBtn: 0
                                });
                                var num = 0;
                                var speed = 3;
                                params = { "depart": value };
                                $.post("/add_aepart/", params, function (data) {
                                    fk = data.result;
                                    speed = 80;
                                });

                                var timer = setInterval(function () {
                                    num += speed;
                                    $("#pbcontent").css("width", num + 'px');
                                    if (num >= 400) {
                                        $("#pbcontent").css("width", '400px');
                                        clearInterval(timer);
                                        if (fk == 1) {
                                            layer.alert('添加成功', function () {
                                                location.reload();
                                            });
                                        } else {
                                            layer.alert('添加失败，该部门已存在', function () {
                                                location.reload();
                                            });
                                        }
                                    }
                                }, 200);
                            }
                        } else {
                            layer.alert('部门名必须全部为汉字');
                            setTimeout(function () {
                                $(".addTwoLevel input[type='text']").focus();
                            }, 50);
                        }
                    },
                    btn2: function (index) {
                        $(".addTwoLevel").html("+&nbsp;添加");
                        $(".addTwoLevel").removeClass('on');
                        layer.close(index);
                    }
                });
            },
            btn2: function (index) {
                layer.close(index);
            }
        });
    });





    function pathNone() {
        // $(classA).css("display","none");
        $(classB).css("display", "none");
        $(classC).css("display", "none");
        $(classD).css("display", "none");
        $(classAIcon).css("display", "none");
        $(classBIcon).css("display", "none");
        $(classCIcon).css("display", "none");

    }

    function navLeftBindData(choice) {
        var choiceId = $(choice).attr("id");
        var choiceValue = $(choice).attr("value");
        var params = {
            "type": 0
        }
        if (choiceValue == "首页") {
            $(navRightHead).attr("title", choiceValue);
            $(navRightHead).text(choiceValue);
            $(navRightInter).text("");
            $(navRightContent).html("");
        }
        if (choiceValue != "首页") {
            $(navRightHead).attr("title", choiceValue);
            $(navRightHead).text(choiceValue);
        }
        if (choiceId) {
            switch (choiceId) {
                case "allData":
                    $(navRightInter).text("接口数量");
                    $(navRightContent).html(allData);
                    break;
                case "countryData":
                    params.type = 1;
                    $(navRightInter).text("接口数量");
                    postDatas(params);
                    break;
                case "directlySubData":
                    params.type = 2;
                    $(navRightInter).text("接口数量");
                    postDatas(params);
                    break;
                case "prefecturesData":
                    params.type = 3;
                    $(navRightInter).text("接口数量");
                    postDatas(params);
                    break;
                case "outsideProvinceData":
                    params.type = 4;
                    $(navRightInter).text("接口数量");
                    postDatas(params);
                    break;
                case "dataIntegrate":
                    $(navRightInter).text("");
                    postDatas(4);
                    break;
                case "databaseManagement":
                    $(navRightInter).text("");
                    postDatas(5);
                    break;
                case "auditAnalysis":
                    $(navRightInter).text("");
                    postDatas(6);
                    break;
                case "journal":
                    $(navRightInter).text("");
                    postDatas(7);
            }
            
        }
    }

    function postDatas(params) {
        if(typeof params == "object"){
            $.post("/jump_dpeartDetail/",params,function(data){
                console.log(data.result);
                var results = data.result;
                dataStr = "";
                for(var i = 0 ; i < results.length; i ++){
                    dataStr += '<ul>';
                    // 一级部门
                    dataStr += '<li class="firstDier">';
                    dataStr += '<div class="nav_right_firstName" title=' + results[i].departname + '>' + results[i].departname + '</div>';
                    dataStr += '<div class="icon"><span class="interNum">(' + results[i].total_num + ')</span><span class="icon-angle-down"></span></div>';
                    dataStr += '</li>';
                    // 二级菜单
                    dataStr += '<ul>';
                    // 二级用户目录
                    dataStr += '<li class="secondDier">';
                    dataStr += '<div class="nav_right_secondName" title="用户目录">用户目录</div>';
                    dataStr += '<div class="icon">';
                    dataStr += '<span class="interNum">(' + results[i].user_num + ')</span>';
                    dataStr += '<span class="icon-angle-down"></span>';
                    dataStr += '</div>';
                    dataStr += '</li>';
                    // 三级目录用户列表
                    dataStr += '<ul>';
                    dataStr += '<a href="/user_list/" target="body_iframe">';
                    dataStr += '<li class="thirdDier">';
                    dataStr += '◆&nbsp;<div class="nav_right_thirdName" title="用户列表">用户列表</div>';
                    dataStr += '<div class="icon"><span class="interNum">(' + results[i].user_num + ')</span></div>';
                    dataStr += '</li>';
                    dataStr += '</a>';
                    dataStr += '</ul>';
                    // 二级服务目录
                    dataStr += '<li class="secondDier">';
                    dataStr += '<div class="nav_right_secondName" title="用户目录">服务目录</div>';
                    dataStr += '<div class="icon"><span class="icon-angle-down"></span></div>';
                    dataStr += '</li>';
                    // 三级目录映射域名
                    dataStr += '<ul>';
                    dataStr += '<a href="/admin_mapping/" target="body_iframe">';
                    dataStr += '<li class="thirdDier">';
                    dataStr += '◆&nbsp;<div class="nav_right_thirdName">映射域名</div>';
                    dataStr += '</li>';
                    dataStr += '</a>';
                    // 三级映射目录
                    dataStr += '<a href="/admin_catalog/" target="body_iframe">';
                    dataStr += '<li class="thirdDier">';
                    dataStr += '◆&nbsp;<div class="nav_right_thirdName">映射目录</div>';
                    dataStr += '</li>';
                    dataStr += '</a>';
                    dataStr += '</ul>';
                    // 二级数据目录
                    dataStr += '<li class="secondDier">';
                    dataStr += '<div class="nav_right_secondName" title="用户目录">数据目录</div>';
                    dataStr += '<div class="icon">';
                    dataStr += '<span class="interNum">(' + results[i].service_num + ')</span>';
                    dataStr += '<span class="icon-angle-down"></span>';
                    dataStr += '</div>';
                    dataStr += '</li>';
                    // 三级数据目录
                    dataStr += '<ul>';
                    dataStr += '<a href="/service_list/" target="body_iframe">';
                    dataStr += '<li class="thirdDier">';
                    dataStr += '◆&nbsp;<div class="nav_right_thirdName" title="用户列表">数据目录</div>';
                    dataStr += '<div class="icon">';
                    dataStr += '<span class="interNum">(' + results[i].service_num + ')</span>';
                    dataStr += '</div>';
                    dataStr += '</li>';
                    dataStr += '</a>';
                    dataStr += '</ul>';
                    // 二级安全目录
                    dataStr += '<li class="secondDier">';
                    dataStr += '<div class="nav_right_secondName" title="用户目录">安全目录</div>';
                    dataStr += '<div class="icon">';
                    dataStr += '<span class="interNum">(' + results[i].safe_num + ')</span>';
                    dataStr += '<span class="icon-angle-down"></span>';
                    dataStr += '</div>';
                    dataStr += '</li>';
                    // 三级访问控制
                    dataStr += '<ul>';
                    dataStr += '<a href="/acl_list/" target="body_iframe">';
                    dataStr += '<li class="thirdDier">';
                    dataStr += '◆&nbsp;<div class="nav_right_thirdName">访问控制</div>';
                    dataStr += '<div class="icon">';
                    dataStr += '<span class="interNum">(' + results[i].acl_num + ')</span>';
                    dataStr += '</div>';
                    dataStr += '</li>';
                    dataStr += '</a>';
                    // 三级流量控制
                    dataStr += '<a href="/control_list/" target="body_iframe">';
                    dataStr += '<li class="thirdDier">';
                    dataStr += '◆&nbsp;<div class="nav_right_thirdName">流量控制</div>';
                    dataStr += '<div class="icon">';
                    dataStr += '<span class="interNum">(' + results[i].controls_num + ')</span>';
                    dataStr += '</div>';
                    dataStr += '</li>';
                    dataStr += '</a>';
                    dataStr += '</ul>';
                    // 二级元目录
                    dataStr += '<li class="secondDier">';
                    dataStr += '<div class="nav_right_secondName" title="用户目录">元目录</div>';
                    dataStr += '<div class="icon">';
                    dataStr += '<span class="icon-angle-down"></span>';
                    dataStr += '</div>';
                    dataStr += '</li>';
                    // 三级数据源录入
                    dataStr += '<ul>';
                    dataStr += '<a href="/db_list/" target="body_iframe">';
                    dataStr += '<li class="thirdDier">';
                    dataStr += '◆&nbsp;<div class="nav_right_thirdName">数据源录入</div>';
                    dataStr += '</li>';
                    dataStr += '</a>';
                    // 三级文件源录入
                    dataStr += '<a href="/file_list/" target="body_iframe">';
                    dataStr += '<li class="thirdDier">';
                    dataStr += '◆&nbsp;<div class="nav_right_thirdName">文件源录入</div>';
                    dataStr += '</li>';
                    dataStr += '</a>';
                    // 三级接口源录入
                    dataStr += '<a href="/interface_list/" target="body_iframe">';
                    dataStr += '<li class="thirdDier">';
                    dataStr += '◆&nbsp;<div class="nav_right_thirdName">接口源录入</div>';
                    dataStr += '</li>';
                    dataStr += '</a>';
                    // 三级消息源录入
                    dataStr += '<a href="/message_list/" target="body_iframe">';
                    dataStr += '<li class="thirdDier">';
                    dataStr += '◆&nbsp;<div class="nav_right_thirdName">消息源录入</div>';
                    dataStr += '</li>';
                    dataStr += '</a>';
                    dataStr += '</ul>';
                    // 二级数据桥接
                    dataStr += '<li class="secondDier">';
                    dataStr += '<div class="nav_right_secondName" title="用户目录">数据桥接</div>';
                    dataStr += '<div class="icon">';
                    dataStr += '<span class="interNum">(' + results[i].data_num + ')</span>';
                    dataStr += '<span class="icon-angle-down"></span>';
                    dataStr += '</div>';
                    dataStr += '</li>';
                    // 三级数据库桥接
                    dataStr += '<ul>';
                    dataStr += '<a href="/sql_admin/" target="body_iframe">';
                    dataStr += '<li class="thirdDier">';
                    dataStr += '◆&nbsp;<div class="nav_right_thirdName">数据库桥接</div>';
                    dataStr += '<div class="icon">';
                    dataStr += '<span class="interNum">(' + results[i].dbList_num + ')</span>';
                    dataStr += '</div>';
                    dataStr += '</li>';
                    dataStr += '</a>';
                    // 三级文件
                    dataStr += '<a href="/admin_file/" target="body_iframe">';
                    dataStr += '<li class="thirdDier">';
                    dataStr += '◆&nbsp;<div class="nav_right_thirdName">文件</div>';
                    dataStr += '<div class="icon">';
                    dataStr += '<span class="interNum">(' + results[i].fileList_num + ')</span>';
                    dataStr += '</div>';
                    dataStr += '</li>';
                    dataStr += '</a>';
                    // 三级接口
                    dataStr += '<a href="/admin_interface/" target="body_iframe">';
                    dataStr += '<li class="thirdDier">';
                    dataStr += '◆&nbsp;<div class="nav_right_thirdName">接口</div>';
                    dataStr += '<div class="icon">';
                    dataStr += '<span class="interNum">(' + results[i].interfaceList_num + ')</span>';
                    dataStr += '</div>';
                    dataStr += '</li>';
                    dataStr += '</a>';
                    // 三级消息
                    dataStr += '<a href="/admin_ways/" target="body_iframe">';
                    dataStr += '<li class="thirdDier">';
                    dataStr += '◆&nbsp;<div class="nav_right_thirdName">消息</div>';
                    dataStr += '<div class="icon">';
                    dataStr += '<span class="interNum">(' + results[i].messageList_num + ')</span>';
                    dataStr += '</div>';
                    dataStr += '</li>';
                    dataStr += '</a>';
                    dataStr += '</ul></ul></ul>';
                }
                $(navRightContent).html(dataStr);
            });
        } else {
            dataStr = "";
            switch(params){
                case 4:
                    dataStr += '<ul>';
                    dataStr += '<a href="http://59.215.191.38" target="_blank">';
                    dataStr += '<li class="firstDier">';
                    dataStr += '<div class="nav_right_firstName">数据库集成</div>';
                    dataStr += '</li>';
                    dataStr += '</a>';
                    dataStr += '<a href="http://59.215.191.48" target="body_iframe">';
                    dataStr += '<li class="firstDier">';
                    dataStr += '<div class="nav_right_firstName">文件集成</div>';
                    dataStr += '</li>';
                    dataStr += '</a>';
                    dataStr += '</ul>';
                    break;
                case 5:
                    dataStr += '<ul>';
                    dataStr += '<li class="firstDier" id="esg">';
                    dataStr += '<div class="nav_right_firstName">易鲸捷数据区</div>';
                    dataStr += '</li>';
                    // dataStr += '<a href="https://59.215.191.45:1158/em/" target="_blank">';
                    // dataStr += '<li class="firstDier">';
                    // dataStr += '<div class="nav_right_firstName">oracle数据区</div>';
                    // dataStr += '</li>';
                    // dataStr += '</a>';
                    // dataStr += '<a href="http://59.215.191.97/mysqladmin/" target="_blank">';
                    // dataStr += '<li class="firstDier">';
                    // dataStr += '<div class="nav_right_firstName">mysql数据区</div>';
                    // dataStr += '</li>';
                    // dataStr += '</a>';
                    dataStr += '</ul>';
                    break;
                case 6:
                    dataStr += '<ul>';
                    dataStr += '<a href="/journal/" target="body_iframe">';
                    dataStr += '<li class="firstDier">';
                    dataStr += '<div class="nav_right_firstName">配置日志</div>';
                    dataStr += '</li>';
                    dataStr += '</a>';
                    dataStr += '<a href="/status_journal/" target="body_iframe">';
                    dataStr += '<li class="firstDier">';
                    dataStr += '<div class="nav_right_firstName">状态日志</div>';
                    dataStr += '</li>';
                    dataStr += '</a>';
                    dataStr += '<a href="/statistical_analysis/" target="body_iframe">';
                    dataStr += '<li class="firstDier">';
                    dataStr += '<div class="nav_right_firstName">统计分析</div>';
                    dataStr += '</li>';
                    dataStr += '</a>';
                    dataStr += '</ul>';
                    break;
                case 7:
                    dataStr += '<ul>';
                    dataStr += '<a href="/journal/" target="body_iframe">';
                    dataStr += '<li class="firstDier">';
                    dataStr += '<div class="nav_right_firstName">配置日志</div>';
                    dataStr += '</li>';
                    dataStr += '</a>';
                    dataStr += '</ul>';
                    break;
            }
            $(navRightContent).html(dataStr);
        }
    }

});
