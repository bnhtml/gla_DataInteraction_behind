var depart;
var interface_Depart;
var interface_Parent;
var interface_Num;
var system_lock = true;
var control_lock = false;
var tbDatasBL;
var tbDataIndex;
var tbDataLayer;
var spinner;
$(function () {
    tbDatasBL = tbDatas;
    spinner = $(".icon-spinner");
    // 记录数据接口封装第几步
    var StepCount = 0;
    // 记录选择的数据类型
    var saveDataType = 0;
    // 类型
    var dataType;
    // 记录数据接口控制第几步
    var StepCount_control = 0;
    if(differentPage == "Administrators") {
        StepCount = 1;
        StepCount_control = 1;
    } else if(differentPage == "technicalSupport"){
        StepCount = 2;
        StepCount_control = 2;
        $(".dataInter_secondStep").css("display","flex");
        $(".interControl_secondStep").css("display","flex");
        depart = departname;
    }
    $(".cli").click();
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
        var othis = $(this);
        // othis.addClass("clickDiv");
        othis.css({"border-color":"#58cafd","font-weight":"700"}).parent().siblings().find("div").css({"border-color":"transparent","font-weight":"normal"});
        // othis.addClass("clickDiv").parent().siblings().find(".clickDiv").removeClass("clickDiv");
        //点击横向菜单数据区管理
        if($(othis).attr("class") == "dataAreaManage") {
            resetDataInter();
            resetControl();
            $("#left_menu").css("display","block");
            $(".body").css("display","flex");
            $(".dataInterPack_content").css("display","none");
            $(".control_content").css("display","none");
            $("#databaseManagement").click();
            // $.post("/loginEsgyn/",function (data) {                
            //     window.open("https://59.215.191.26:4206/#/login?" + data.result);
            // });
        //点击横向菜单数据准备
        } else if ($(othis).attr("class") == "dataPrep") {
            resetDataInter();
            resetControl();
            $("#left_menu").css("display","block");
            $(".body").css("display","flex");
            $(".dataInterPack_content").css("display","none");
            $(".control_content").css("display","none");
            $("#dataIntegrate").click();
        //点击横向菜单系统状态
        } else if ($(othis).attr("class") == "systemStatus") {
            resetDataInter();
            resetControl();
            $("#left_menu").css("display","block");
            $(".body").css("display","flex");
            $(".dataInterPack_content").css("display","none");
            $(".control_content").css("display","none");
            if($("#auditAnalysis").length) {
                $("#auditAnalysis").click();
            } else {
                $("#journal").click();
            }
            $(".nav_right_content").find("a:first-child>li.firstDier").click();
        //点击横向菜单数据接口封装
        } else if ($(othis).attr("class") == "dataInterPack") {
            if(differentPage == "technicalSupport") {
                depart = departname;
            }
            resetControl();
            $("#left_menu").css("display","none");
            system_lock = false;
            $(".body").css("display","none");
            $(".preStep").css("display","none");
            $(".dataInterPack_content").css("display","flex");
            $(".control_content").css("display","none");
        //点击横向菜单数据接口控制
        } else if ($(this).attr("class") == "control_Data") {
            if(differentPage == "technicalSupport") {
                depart = departname;
            }
            resetDataInter();
            $(ifr_control).attr("src","/departAdmin/user_list/");
            $("#left_menu").css("display","none");
            control_lock = false;
            $(".body").css("display","none");
            $(".control_preStep").css("display","none");
            $(".dataInterPack_content").css("display","none");
            $(".control_content").css("display","flex");
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
        e.stopPropagation();
        var othis = $(this);
        classA.text(othis.attr("value")).nextAll().css("display", "none");
        if ($(othis).parent("a").length) {
            $(othis).addClass("navClick").parent("a").siblings().removeClass("navClick");
        } else {
            $(othis).toggleClass("navClick").siblings().removeClass("navClick");
            $(othis).siblings("a").find("li").removeClass("navClick");
        }
        navLeftBindData(othis);
    });
    //点击一级目录
    $(".nav_right_content").on("click", ">ul li.firstDier", function () {
        system_lock = true;
        control_lock = true;
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
    $(".nav_right_content").on("click",".checkRightCon",function(){
        var othis = $(this);
        $(othis).css("background-color","#4d92bc").parent().siblings().find(".firstDier").css("background-color","transparent");
    });
    // 点击左侧菜单
    function navLeftBindData(choice) {
        var choiceId = $(choice).attr("id");
        var choiceValue = $(choice).attr("value");
        var params = {
            "type": 0
        }
        $(".header_nav>ul>li>div").css({"border-color":"transparent","font-weight":"normal"});
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
                    $(".dataPrep").css({"border-color":"#58cafd","font-weight":"700"});
                    postDatas(4);
                    break;
                case "databaseManagement":
                    $(navRightInter).text("");
                    $(".dataAreaManage").css({"border-color":"#58cafd","font-weight":"700"});
                    postDatas(5);
                    break;
                case "auditAnalysis":
                    $(navRightInter).text("");
                    $(".systemStatus").css({"border-color":"#58cafd","font-weight":"700"});
                    postDatas(6);
                    break;
                case "journal":
                    $(navRightInter).text("");
                    $(".systemStatus").css({"border-color":"#58cafd","font-weight":"700"});
                    postDatas(7);
            }
            
        }
    }

    // 切换左侧菜单的内容
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
                    dataStr += '<div class="nav_right_secondName" title="服务目录">服务目录</div>';
                    dataStr += '<div class="icon"><span class="icon-angle-down"></span></div>';
                    dataStr += '</li>';
                    // 三级目录映射域名
                    dataStr += '<ul>';
                    dataStr += '<a href="/admin_mapping/" target="body_iframe">';
                    dataStr += '<li class="thirdDier">';
                    dataStr += '◆&nbsp;<div class="nav_right_thirdName" title="映射域名">映射域名</div>';
                    dataStr += '</li>';
                    dataStr += '</a>';
                    // 三级映射目录
                    dataStr += '<a href="/admin_catalog/" target="body_iframe">';
                    dataStr += '<li class="thirdDier">';
                    dataStr += '◆&nbsp;<div class="nav_right_thirdName" title="映射目录">映射目录</div>';
                    dataStr += '</li>';
                    dataStr += '</a>';
                    dataStr += '</ul>';
                    // 二级元数据
                    dataStr += '<li class="secondDier">';
                    dataStr += '<div class="nav_right_secondName" title="元数据">元数据</div>';
                    dataStr += '<div class="icon">';
                    dataStr += '<span class="icon-angle-down"></span>';
                    dataStr += '</div>';
                    dataStr += '</li>';
                    // 三级数据源录入
                    dataStr += '<ul>';
                    dataStr += '<a href="/db_list/" target="body_iframe">';
                    dataStr += '<li class="thirdDier">';
                    dataStr += '◆&nbsp;<div class="nav_right_thirdName" title="数据源录入">数据源录入</div>';
                    dataStr += '</li>';
                    dataStr += '</a>';
                    // 三级文件源录入
                    dataStr += '<a href="/file_list/" target="body_iframe">';
                    dataStr += '<li class="thirdDier">';
                    dataStr += '◆&nbsp;<div class="nav_right_thirdName" title="文件源录入">文件源录入</div>';
                    dataStr += '</li>';
                    dataStr += '</a>';
                    // 三级接口源录入
                    dataStr += '<a href="/interface_list/" target="body_iframe">';
                    dataStr += '<li class="thirdDier">';
                    dataStr += '◆&nbsp;<div class="nav_right_thirdName" title="接口源录入">接口源录入</div>';
                    dataStr += '</li>';
                    dataStr += '</a>';
                    // 三级消息源录入
                    dataStr += '<a href="/message_list/" target="body_iframe">';
                    dataStr += '<li class="thirdDier">';
                    dataStr += '◆&nbsp;<div class="nav_right_thirdName" title="消息源录入">消息源录入</div>';
                    dataStr += '</li>';
                    dataStr += '</a>';
                    dataStr += '</ul>';
                    // 二级数据桥接
                    dataStr += '<li class="secondDier">';
                    dataStr += '<div class="nav_right_secondName" title="数据桥接">数据桥接</div>';
                    dataStr += '<div class="icon">';
                    dataStr += '<span class="interNum">(' + results[i].data_num + ')</span>';
                    dataStr += '<span class="icon-angle-down"></span>';
                    dataStr += '</div>';
                    dataStr += '</li>';
                    // 三级数据库桥接
                    dataStr += '<ul>';
                    dataStr += '<a href="/sql_admin/" target="body_iframe">';
                    dataStr += '<li class="thirdDier">';
                    dataStr += '◆&nbsp;<div class="nav_right_thirdName" title="数据库桥接">数据库桥接</div>';
                    dataStr += '<div class="icon">';
                    dataStr += '<span class="interNum">(' + results[i].dbList_num + ')</span>';
                    dataStr += '</div>';
                    dataStr += '</li>';
                    dataStr += '</a>';
                    // 三级文件
                    dataStr += '<a href="/admin_file/" target="body_iframe">';
                    dataStr += '<li class="thirdDier">';
                    dataStr += '◆&nbsp;<div class="nav_right_thirdName" title="文件桥接">文件桥接</div>';
                    dataStr += '<div class="icon">';
                    dataStr += '<span class="interNum">(' + results[i].fileList_num + ')</span>';
                    dataStr += '</div>';
                    dataStr += '</li>';
                    dataStr += '</a>';
                    // 三级接口
                    dataStr += '<a href="/admin_interface/" target="body_iframe">';
                    dataStr += '<li class="thirdDier">';
                    dataStr += '◆&nbsp;<div class="nav_right_thirdName" title="接口桥接">接口桥接</div>';
                    dataStr += '<div class="icon">';
                    dataStr += '<span class="interNum">(' + results[i].interfaceList_num + ')</span>';
                    dataStr += '</div>';
                    dataStr += '</li>';
                    dataStr += '</a>';
                    // 三级消息
                    dataStr += '<a href="/admin_ways/" target="body_iframe">';
                    dataStr += '<li class="thirdDier">';
                    dataStr += '◆&nbsp;<div class="nav_right_thirdName" title="消息桥接">消息桥接</div>';
                    dataStr += '<div class="icon">';
                    dataStr += '<span class="interNum">(' + results[i].messageList_num + ')</span>';
                    dataStr += '</div>';
                    dataStr += '</li>';
                    dataStr += '</a></ul>';
                    // 二级数据接口封装
                    dataStr += '<li class="secondDier">';
                    dataStr += '<div class="nav_right_secondName" title="数据接口封装">数据接口封装</div>';
                    dataStr += '<div class="icon">';
                    dataStr += '<span class="interNum">(' + results[i].service_num + ')</span>';
                    dataStr += '<span class="icon-angle-down"></span>';
                    dataStr += '</div>';
                    dataStr += '</li>';
                    // 三级数据接口
                    dataStr += '<ul>';
                    dataStr += '<a href="/service_list/" target="body_iframe">';
                    dataStr += '<li class="thirdDier">';
                    dataStr += '◆&nbsp;<div class="nav_right_thirdName" title="数据接口封装">数据接口封装</div>';
                    dataStr += '<div class="icon">';
                    dataStr += '<span class="interNum">(' + results[i].service_num + ')</span>';
                    dataStr += '</div>';
                    dataStr += '</li>';
                    dataStr += '</a>';
                    dataStr += '</ul>';
                    // 二级数据接口控制
                    dataStr += '<li class="secondDier">';
                    dataStr += '<div class="nav_right_secondName" title="数据接口控制">数据接口控制</div>';
                    dataStr += '<div class="icon">';
                    dataStr += '<span class="interNum">(' + results[i].safe_num + ')</span>';
                    dataStr += '<span class="icon-angle-down"></span>';
                    dataStr += '</div>';
                    dataStr += '</li>';
                    // 三级访问控制
                    dataStr += '<ul>';
                    dataStr += '<a href="/acl_list/" target="body_iframe">';
                    dataStr += '<li class="thirdDier">';
                    dataStr += '◆&nbsp;<div class="nav_right_thirdName" title="访问控制">访问控制</div>';
                    dataStr += '<div class="icon">';
                    dataStr += '<span class="interNum">(' + results[i].acl_num + ')</span>';
                    dataStr += '</div>';
                    dataStr += '</li>';
                    dataStr += '</a>';
                    // 三级流量控制
                    dataStr += '<a href="/control_list/" target="body_iframe">';
                    dataStr += '<li class="thirdDier">';
                    dataStr += '◆&nbsp;<div class="nav_right_thirdName" title="流量控制">流量控制</div>';
                    dataStr += '<div class="icon">';
                    dataStr += '<span class="interNum">(' + results[i].controls_num + ')</span>';
                    dataStr += '</div>';
                    dataStr += '</li>';
                    dataStr += '</a>';
                    dataStr += '</ul>';
                    dataStr += '</ul></ul>';
                }
                $(navRightContent).html(dataStr);
            });
        } else {
            dataStr = "";
            switch(params){
                case 4:
                    dataStr += '<ul>';
                    dataStr += '<a href="http://59.215.191.38" target="body_iframe">';
                    dataStr += '<li class="firstDier checkRightCon">';
                    dataStr += '<div class="nav_right_firstName">数据库集成</div>';
                    dataStr += '</li>';
                    dataStr += '</a>';
                    dataStr += '<a href="http://59.215.191.48" target="body_iframe">';
                    dataStr += '<li class="firstDier checkRightCon">';
                    dataStr += '<div class="nav_right_firstName">文件集成</div>';
                    dataStr += '</li>';
                    dataStr += '</a>';
                    dataStr += '</ul>';
                    break;
                case 5:
                    dataStr += '<ul>';
                    dataStr += '<li class="firstDier checkRightCon" id="esg">';
                    dataStr += '<div class="nav_right_firstName">数据区</div>';
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
                    dataStr += '<li class="firstDier checkRightCon">';
                    dataStr += '<div class="nav_right_firstName">配置日志</div>';
                    dataStr += '</li>';
                    dataStr += '</a>';
                    dataStr += '<a href="/status_journal/" target="body_iframe">';
                    dataStr += '<li class="firstDier checkRightCon">';
                    dataStr += '<div class="nav_right_firstName">状态日志</div>';
                    dataStr += '</li>';
                    dataStr += '</a>';
                    // ***********  不可以删的内容，想删先问老郭。
                    // dataStr += '<a href="/statistical_analysis/" target="body_iframe">';
                    // dataStr += '<li class="firstDier">';
                    // dataStr += '<div class="nav_right_firstName">统计分析</div>';
                    // dataStr += '</li>';
                    // dataStr += '</a>';
                    // ********************************
                    dataStr += '</ul>';
                    break;
                case 7:
                    dataStr += '<ul>';
                    dataStr += '<a href="/journal/" target="body_iframe">';
                    dataStr += '<li class="firstDier checkRightCon">';
                    dataStr += '<div class="nav_right_firstName">配置日志</div>';
                    dataStr += '</li>';
                    dataStr += '</a>';
                    dataStr += '</ul>';
                    break;
            }
            $(navRightContent).html(dataStr);
        }
    }



    // 数据接口封装选择部门的js代码
    $(".dataInter_firstStep").on("click",".checkDepart_con>ul>li",function(){
        var othis = $(this);
        $("i#pleCheckDepart").text(othis.text().trim());
    });
    $(".dataInter_secondStep").on("click",".checkDepart_con>ul>li",function(){
        var othis = $(this);
        $("i#pleCheckDataType").text(othis.text().trim());
    });
    $(".checkDepart").click(function(){
        var othis = $(this);
        othis.find(".checkDepart_con").stop().slideToggle(200);
        othis.find(".icon-angle-down").toggleClass("rotatez");
    });

    // 数据接口控制选择部门的js代码
    $(".interControl_firstStep").on("click",".checkInterCont_con>ul>li",function(){
        var othis = $(this);
        $("i#pleCheckInterCont").text(othis.text().trim());
    });
    // $(".interControl_secondStep").on("click",".checkInterCont_con>ul>li",function(){
    //     var othis = $(this);
    //     $("i#pleCheckDataType").text(othis.text().trim());
    // });
    $(".checkInterCont").click(function(){
        var othis = $(this);
        othis.find(".checkInterCont_con").stop().slideToggle(200);
        othis.find(".icon-angle-down").toggleClass("rotatez");
    });


    var ifr = $("#check_iframe");
    var ifr_control = $("#interControl_iframe");
    //数据接口封装下一步
    $(".afterStep").click(function(){
        switch(StepCount){
            case 1:
                if($("i#pleCheckDepart").text().trim() == "请选择部门") {
                    layer.alert("请选择部门");   
                } else {
                    $(".preStep").css("display","block");
                    StepCount ++;
                    depart = $("i#pleCheckDepart").text().trim();

                    $.post('/admin_db/', { "depart": depart });
                    $("#two").parent().addClass("click_con");
                    $(".dataInter_firstStep").css("display","none");
                    $(".dataInter_secondStep").css("display","flex");
                }
                break;
            case 2:
                $(".preStep").css("display","block");
                dataType = $("#pleCheckDataType").text().trim();
                if(dataType == "请选择数据类型") {
                    layer.alert("请选择数据类型");   
                } else {
                    StepCount ++;
                    $.post('/admin_db/', { "depart": depart },function(){
                        switch(dataType){
                            case "数据库类":
                                saveDataType = 1;
                                if(differentPage == "Administrators") {
                                    $(ifr).attr("src","/db_list/");
                                } else if(differentPage == "technicalSupport"){
                                    $(ifr).attr("src","/departAdmin/db_list/");
                                }
                                break;
                            case "文件类":
                                saveDataType = 2;
                                if(differentPage == "Administrators") {
                                    $(ifr).attr("src","/file_list/");
                                } else if(differentPage == "technicalSupport"){
                                    $(ifr).attr("src","/departAdmin/file_list/");
                                }
                                break;
                            case "接口类":
                                saveDataType = 3;
                                if(differentPage == "Administrators") {
                                    $(ifr).attr("src","/interface_list/");
                                } else if(differentPage == "technicalSupport"){
                                    $(ifr).attr("src","/departAdmin/interface_list/");
                                }
                                break;
                            case "消息类":
                                saveDataType = 4;
                                if(differentPage == "Administrators") {
                                    $(ifr).attr("src","/message_list/");
                                } else if(differentPage == "technicalSupport"){
                                    $(ifr).attr("src","/departAdmin/message_list/");
                                }
                                break;
                        }
                    });
                    $("#three").parent().addClass("click_con");
                    $(".dataInter_secondStep").css("display","none");
                    $(".dataInter_thirdStep").css("display","flex");
                }
                break;
            case 3:
                switch(saveDataType) {
                    case 1:
                        if(differentPage == "Administrators") {
                            $(ifr).attr("src","/sql_admin/");
                        } else if(differentPage == "technicalSupport"){
                            $(ifr).attr("src","/departAdmin/sql_admin/");
                        }
                        break;
                    case 2:
                        if(differentPage == "Administrators") {
                            $(ifr).attr("src","/admin_file/");
                        } else if(differentPage == "technicalSupport"){
                            $(ifr).attr("src","/departAdmin/admin_file/");
                        }
                        break;
                    case 3:
                        if(differentPage == "Administrators") {
                            $(ifr).attr("src","/admin_interface/");
                        } else if(differentPage == "technicalSupport"){
                            $(ifr).attr("src","/departAdmin/admin_interface/");
                        }
                        break;
                    case 4:
                        if(differentPage == "Administrators") {
                            $(ifr).attr("src","/admin_ways/");
                        } else if(differentPage == "technicalSupport"){
                            $(ifr).attr("src","/departAdmin/admin_ways/");
                        }
                        break;
                }
                StepCount ++;
                $("#four").parent().addClass("click_con");
                break;
            case 4:
                if(differentPage == "Administrators") {
                    $(ifr).attr("src","/admin_catalog/");
                } else if(differentPage == "technicalSupport"){
                    $(ifr).attr("src","/departAdmin/admin_catalog/");
                }
                StepCount ++;
                $("#five").parent().addClass("click_con");
                break;
            case 5:
                $(".afterStep").text("完成");
                if(differentPage == "Administrators") {
                    $(ifr).attr("src","/service_list/");
                } else if(differentPage == "technicalSupport"){
                    $(ifr).attr("src","/departAdmin/service_list/");
                }
                StepCount ++;
                $("#six").parent().addClass("click_con");
                break;
            case 6:
                $(".preStep").css("display","none");
                $("#seven").parent().addClass("click_con");
                layer.alert("数据接口封装完成",function(){
                    window.location.reload();
                });
                // setTimeout(function(){
                //     window.location.reload();
                // },200);
                break;
        }
    });

    //数据接口封装上一步
    $(".preStep").click(function(){
        switch(StepCount){
            case 2:
                StepCount--;
                $(".preStep").css("display","none");
                $(".dataInter_firstStep").css("display","flex");
                $(".dataInter_secondStep").css("display","none");
                $("#two").parent().removeClass("click_con");
                break;
            case 3:
                if(differentPage == "technicalSupport") {
                    $(".preStep").css("display","none");
                }
                StepCount--;
                $(".dataInter_secondStep").css("display","flex");
                $(".dataInter_thirdStep").css("display","none");
                $("#three").parent().removeClass("click_con");
                break;
            case 4:
                switch(dataType){
                    case "数据库类":
                        saveDataType = 1;
                        if(differentPage == "Administrators") {
                            $(ifr).attr("src","/db_list/");
                        } else if(differentPage == "technicalSupport"){
                            $(ifr).attr("src","/departAdmin/db_list/");
                        }
                        break;
                    case "文件类":
                        saveDataType = 2;
                        if(differentPage == "Administrators") {
                            $(ifr).attr("src","/file_list/");
                        } else if(differentPage == "technicalSupport"){
                            $(ifr).attr("src","/departAdmin/file_list/");
                        }
                        break;
                    case "接口类":
                        saveDataType = 3;
                        if(differentPage == "Administrators") {
                            $(ifr).attr("src","/interface_list/");
                        } else if(differentPage == "technicalSupport"){
                            $(ifr).attr("src","/departAdmin/interface_list/");
                        }
                        break;
                    case "消息类":
                        saveDataType = 4;
                        if(differentPage == "Administrators") {
                            $(ifr).attr("src","/message_list/");
                        } else if(differentPage == "technicalSupport"){
                            $(ifr).attr("src","/departAdmin/message_list/");
                        }
                        break;
                }
                StepCount--;
                $("#four").parent().removeClass("click_con");
                break;
            case 5:
                switch(saveDataType) {
                    case 1:
                        if(differentPage == "Administrators") {
                            $(ifr).attr("src","/sql_admin/");
                        } else if(differentPage == "technicalSupport"){
                            $(ifr).attr("src","/departAdmin/sql_admin/");
                        }
                        break;
                    case 2:
                        if(differentPage == "Administrators") {
                            $(ifr).attr("src","/admin_file/");
                        } else if(differentPage == "technicalSupport"){
                            $(ifr).attr("src","/departAdmin/admin_file/");
                        }
                        break;
                    case 3:
                        if(differentPage == "Administrators") {
                            $(ifr).attr("src","/admin_interface/");
                        } else if(differentPage == "technicalSupport"){
                            $(ifr).attr("src","/departAdmin/admin_interface/");
                        }
                        break;
                    case 4:
                        if(differentPage == "Administrators") {
                            $(ifr).attr("src","/admin_ways/");
                        } else if(differentPage == "technicalSupport"){
                            $(ifr).attr("src","/departAdmin/admin_ways/");
                        }
                        break;
                }
                StepCount--;
                $("#five").parent().removeClass("click_con");
                break;
            case 6:
                StepCount--;
                $(".afterStep").text("下一步");
                if(differentPage == "Administrators") {
                    $(ifr).attr("src","/admin_catalog/");
                } else if(differentPage == "technicalSupport"){
                    $(ifr).attr("src","/departAdmin/admin_catalog/");
                }
                $("#six").parent().removeClass("click_con");
                break;
        }
    });

    // 数据接口控制下一步
    $(".control_afterStep").click(function(){
        switch(StepCount_control){
            case 1:
                if($("i#pleCheckInterCont").text().trim() == "请选择部门") {
                    layer.alert("请选择部门");   
                } else {
                    StepCount_control ++;
                    $(".control_preStep").css("display","block");
                    depart = $("i#pleCheckInterCont").text().trim();
                    $.post('/admin_db/', { "depart": depart },function(){
                        if(differentPage == "Administrators") {
                            $(ifr_control).attr("src","/user_list/");
                        } else if(differentPage == "technicalSupport"){
                            $(ifr_control).attr("src","/departAdmin/user_list/");
                        }
                    });
                    $("#two_cont").parent().addClass("click_con");
                    $(".interControl_firstStep").css("display","none");
                    $(".interControl_secondStep").css("display","flex");
                }
                break;
            case 2:
                $.post('/admin_db/', { "depart": depart },function(){
                    if(differentPage == "Administrators") {
                        $(ifr_control).attr("src","/acl_list/");
                    } else if(differentPage == "technicalSupport"){
                        $(ifr_control).attr("src","/departAdmin/acl_list/");
                    }
                });
                if(differentPage == "technicalSupport") {
                    $(".control_preStep").css("display","block");
                }
                StepCount_control ++;
                $("#three_cont").parent().addClass("click_con");
                
                break;
            case 3:
                StepCount_control ++;
                $(".control_afterStep").text("完成");
                $("#four_cont").parent().addClass("click_con");
                if(differentPage == "Administrators") {
                    $(ifr_control).attr("src","/control_list/");
                } else if(differentPage == "technicalSupport"){
                    $(ifr_control).attr("src","/departAdmin/control_list/");
                }
                
                break;
            case 4:
                StepCount_control ++;
                layer.alert("数据接口控制完成",function(){
                    window.location.reload();
                });
                $(".control_preStep").css("display","none");
                $("#five_cont").parent().addClass("click_con");
                // setTimeout(function(){
                   
                // },200);
                break;
        }
    });

    // 数据接口控制上一步
    $(".control_preStep").click(function(){
        switch(StepCount_control){
            case 2:
                $(".control_preStep").css("display","none");
                StepCount_control --;
                $(".interControl_firstStep").css("display","flex");
                $(".interControl_secondStep").css("display","none");
                $("#two_cont").parent().removeClass("click_con");
                break;
            case 3:
                if(differentPage == "technicalSupport") {
                    $(".control_preStep").css("display","none");
                }
                StepCount_control --;
                if(differentPage == "Administrators") {
                    $(ifr_control).attr("src","/user_list/");
                } else if(differentPage == "technicalSupport"){
                    $(ifr_control).attr("src","/departAdmin/user_list/");
                }
                $("#three_cont").parent().removeClass("click_con");
                break;
            case 4:
                StepCount_control --;
                if(differentPage == "Administrators") {
                    $(ifr_control).attr("src","/acl_list/");
                } else if(differentPage == "technicalSupport"){
                    $(ifr_control).attr("src","/departAdmin/acl_list/");
                }
                $(".control_afterStep").text("下一步");
                $("#four_cont").parent().removeClass("click_con");
                break;
        }
    });


    // 重置数据接口封装
    function resetDataInter(){
        $(".afterStep").text("下一步");
        if(differentPage == "Administrators") {
            StepCount = 1;
            $("#pleCheckDepart").text("请选择部门");
            $("#pleCheckDataType").text("请选择数据类型");
            $(".dataInter_firstStep").css("display","flex");
            $(".dataInter_secondStep").css("display","none");
            $(".dataInter_thirdStep").css("display","none");
            $("#two,#three,#four,#five,#six,#seven").parent().removeClass("click_con");
        } else if(differentPage == "technicalSupport"){
            StepCount = 2;
            $("#pleCheckDataType").text("请选择数据类型");
            $(".dataInter_secondStep").css("display","flex");
            $(".dataInter_thirdStep").css("display","none");
            $("#three,#four,#five,#six,#seven").parent().removeClass("click_con");
        }
        
    }
    // 重置数据接口控制
    function resetControl(){
        $(".control_afterStep").text("下一步");
        if(differentPage == "Administrators") {
            StepCount_control = 1;
            $("#pleCheckInterCont").text("请选择部门");
            $(".interControl_firstStep").css("display","flex");
            $(".interControl_secondStep").css("display","none");
            $("#two_cont,#three_cont,#four_cont,#five_cont").parent().removeClass("click_con");
        } else if(differentPage == "technicalSupport"){
            StepCount_control = 2;
            $(".interControl_secondStep").css("display","flex");
            $("#three_cont,#four_cont,#five_cont").parent().removeClass("click_con");
        }
        
    }

    function tbDatas() {
        var index = layer.open({
            area: ["200px", "200px"],
            title:false,
            content: $(".tbData"),
            closeBtn: 0,
            type: 1,
            skin: 'tbData_class'
        });
        tbDataIndex = index;
        tbDataLayer = layer;
    }
});
