$(function(){
    var canshu;
    var reg = /^[\u4e00-\u9fa5]+$/;
    var kg = true;
    var kg2 = true;
    var oneLevelName,
        twoLevelName;
    var date_now = new Date().getTime();

    //修改按钮
    $(".Level_content").on('click',"#update",function(e){
        e.stopPropagation();
        canshu = $(this).parents('#content_ul').find(".firstname").text().trim();
        $(this).parents('#content_ul').find(".firstname").html("<input type='text'><input type='button' value='确认' id='ok'>");
        $(this).parents('#content_ul').find(".firstname").children().eq(0).val(canshu).focus();
    });
    //确定修改按钮
    $(".Level_content").on('click',"#ok",function(e){
        e.stopPropagation();
        var updateName = $(this).prev().val().trim().replace(/\s/g,'');
        var dier = $(this).parents('.Level_div').find("h3").text().trim().replace(/\s/g,'');
        var updateLi = $(this).parent();
        if(updateName != canshu){
            layer.confirm('确认修改吗?',{
                title: "提示",
                btn: ["确定", "取消"],
                yes:function (index) {
                     if(reg.test(updateName)){
                        $.post('/update_list/',{"dier":dier,"update_name":updateName,"old_name": canshu},function (data) {
                            if(data.result[0].result == 1){
                                layer.alert('修改成功');
                                $(updateLi).html(updateName);
                                $(updateLi).next().html(data.result[0].us_updateName);
                            }else{
                                layer.alert('修改失败',function (index) {
                                    layer.close(index);
                                    $(updateLi).html(canshu);
                                });
                            }
                        });
                    }else{
                        layer.alert('必须为中文',function (index) {
                            layer.close(index);
                            $(".Level_content input[type='text']").focus();
                        });
                    }
                },
                btn2:function (index) {
                    layer.close(index);
                }
            });
        }else{
            $(this).parent().html(canshu);
        }
    });
    //修改框失去焦点时
    $(".Level_content").on('blur',"input[type='text']",function(){
        $(this).next().click();
    });

    //点击添加按钮
    $(".Level_addbtn").click(function(e){
        e.stopPropagation();
        var addblock = $(this);
        var btns = $(this);
        if((new Date().getTime() - date_now) >= 200){
            var dier = $(this).parent().prev().find('h3').text();
            var levelContent = $(this).parent().prev().children().eq(2);
            if(kg){
                kg = false;
                date_now = new Date().getTime();
                $(this).animate({"width":"30%"},400,function(){
                    $(this).before("<input type='text' id='addDier'>");
                    $(this).prev().attr("placeholder","请输入" + dier).focus();
                    $(this).val('确定');
                });
            }else{
                date_now = new Date().getTime();
                var canshu = $(this).prev().val().trim().replace(/\s/g,'');
                    var luyou;
                    var params;
                    switch (dier){
                        case "一级目录":
                            luyou = "/first_info/";
                            params = {'first_name':canshu};
                            break;
                        case "二级目录":
                            luyou = "/second_info/";
                            params = {'first_name':oneLevelName, 'second_name':canshu};
                            break;
                        case "三级目录":
                            luyou = "/third_info/";
                            params = {'first_name':oneLevelName, 'second_name':twoLevelName,'third_name':canshu};
                            break;
                    }
                if(reg.test(canshu)){
                    layer.confirm('确认添加吗?', {
                        title: "提示",
                        btn: ["确定", "取消"],
                        yes:function (index) {
                            $.post(luyou,params,function (data) {
                                if(data.result[0].result == 1) {
                                    layer.alert('添加成功',{
                                        title:"提示",
                                        btn:["确定"],
                                        yes:function (index) {
                                            layer.close(index);
                                            var str = '';
                                            str += "<ul id='content_ul'>";
                                            str += "<li class='dierData'>" + (Number($(levelContent).children("ul:last-child").children("li:first-child").text()) + 1) + '</li>';
                                            str += "<li class='firstname' title=" + canshu + ">" + canshu + '</li>';
                                            str += "<li  class='path' title=" + data.result[0].map_path + ">" + data.result[0].map_path + '</li>';
                                            str += "<li><a title='修改' class='glyphicon glyphicon-pencil' id='update'></a>&nbsp;";
                                            str += "<a title='删除' class='glyphicon glyphicon-trash' id='delete'></a></li>";
                                            str += "</ul>";
                                            $(levelContent).append(str);
                                            $(btns).prev().remove();
                                            $(btns).animate({"width":"100%"},500,function(){
                                                $(btns).val('添加');
                                                kg = true;
                                            });
                                        }
                                    });
                                }else{
                                    layer.alert('添加失败，目录已存在');
                                }
                            });
                        },
                        btn2:function (index) {
                            $(addblock).prev().remove();
                            $(addblock).animate({"width":"100%"},500,function(){
                            $(btns).val('添加');
                            kg = true;
                        });
                        }
                    });
                }else{
                    layer.alert('必须为中文',function (index) {
                        layer.close(index);
                        $('#addDier').focus();
                    });
                }
            }
        }
    });
    //点击每一行数据
    $(".Level_content").on('click',"ul",function(){
        var dierstr = $(this).attr('class');
        if(!dierstr){
            $(this).toggleClass("active").siblings().removeClass("active");
            var dier = $(this).parent().parent().children().eq(0).text();
            switch (dier){
                case "一级目录":
                    $(".TwoLevel .Level_content").html('');
                    $(".ThreeLevel .Level_content").html('');
                    oneLevelName = $(this).children().eq(1).text();
                    $(".TwoLevel .Level_add input[type='button']").removeAttr('disabled').css("background-color","#0ae").css("cursor","default");
                    $(".ThreeLevel .Level_add input[type='button']").attr("disabled","disabled").css("background-color","#ccc").css("cursor","not-allowed");
                    $.post('/second_list/',{"first_name":oneLevelName},function (data) {
                        var secondList = data.data;
                        var secondStr = '';
                        for(var i = 0;i < secondList.length; i++){
                            secondStr += "<ul id='content_ul'>";
                            secondStr += "<li class='dierData'>" + (i + 1) + '</li>';
                            secondStr += "<li class='firstname' title=" + secondList[i].secondName + ">" + secondList[i].secondName + '</li>';
                            secondStr += "<li class='path' title=" + secondList[i].us_secondName + ">" + secondList[i].us_secondName + '</li>';
                            secondStr += "<li><a title='修改' class='glyphicon glyphicon-pencil' id='update' style='margin-right:5px;'></a>&nbsp;";
                            secondStr += "<a title='删除' class='glyphicon glyphicon-trash' id='delete'></a></li>";
                            secondStr += "</ul>";
                        }
                        $(".TwoLevel .Level_content").append(secondStr);
                    });
                    break;
                case "二级目录":
                    $(".ThreeLevel .Level_content").html('');
                    twoLevelName = $(this).children().eq(1).text();
                    $(".ThreeLevel .Level_add input[type='button']").removeAttr('disabled').css("background-color","#0ae").css("cursor","default");
                    $.post('/third_list/',{"second_name":twoLevelName},function (data) {
                        var thirdList = data.data;
                        var thirdStr = '';
                        for(var j = 0; j <thirdList.length; j ++){
                            thirdStr += "<ul id='content_ul'>";
                            thirdStr += "<li class='dierData'>" + (j + 1) + '</li>';
                            thirdStr += "<li class='firstname' title=" + thirdList[j].thirdName + ">" + thirdList[j].thirdName + '</li>';
                            thirdStr += "<li class='path' title=" + thirdList[j].us_thirdName + ">" + thirdList[j].us_thirdName + '</li>';
                            thirdStr += "<li><a title='修改' class='glyphicon glyphicon-pencil' id='update' style='margin-right:5px;'></a>&nbsp;";
                            thirdStr += "<a title='删除' class='glyphicon glyphicon-trash' id='delete'></a></li>";
                            thirdStr += "</ul>";
                        }
                        $(".ThreeLevel .Level_content").append(thirdStr);
                    });
                    break;
            }
        }

    });
    //添加输入框失去焦点
    $(".Level_add").on('blur','#addDier',function () {
        var addcanshu = $(this).val().trim().replace(/\s/g,'');
        if(addcanshu == ''){
            date_now = new Date().getTime();
            $(this).next().val('添加');
            $(this).next().animate({"width":"100%"},500);
            $(this).remove();
            kg = true;
        }else{
            $(this).next().click();

        }
    });
    //删除
    $(".Level_content").on('click','#delete',function (e) {
        e.stopPropagation();
        var cl_dier = $(this).parents('.Level_div').find('h3').text().trim();
        var cl_select = $(this).parents("ul").attr("class");
        var deleteName = $(this).parent().prev().prev().text();
        var deleteUl = $(this).parent().parent();
        var dier = $(this).parents('.Level_content').parent().children().eq(0).text().trim().replace(/\s/g,'');
        var datas = $(this).parents('.Level_content');
        layer.confirm('确认删除吗?',{
           title: "提示",
            btn: ["确定", "取消"],
            yes:function (index) {
                $.post("/delete_list/",{"dier":dier,"delete_name" : deleteName},function (data) {
                    if(data.result == 1){
                        layer.alert('删除成功');
                        $(deleteUl).remove();
                        var datasou = $(datas).find(".dierData");
                        $(datasou).each(function (index,ele) {
                           $(ele).text(index + 1);
                        });
                        if(cl_select){
                            if(cl_dier == '一级目录'){
                                $(".TwoLevel").find('.Level_content').html('');
                                $(".ThreeLevel").find('.Level_content').html('');
                                $(".TwoLevel .Level_add input[type='button']").attr("disabled","disabled").css("background-color","#ccc").css("cursor","not-allowed");
                                $(".ThreeLevel .Level_add input[type='button']").attr("disabled","disabled").css("background-color","#ccc").css("cursor","not-allowed");
                            }else if(cl_dier == '二级目录'){
                                $(".ThreeLevel").find('.Level_content').html('');
                                $(".ThreeLevel .Level_add input[type='button']").attr("disabled","disabled").css("background-color","#ccc").css("cursor","not-allowed");
                            }
                        }
                    }else{
                        layer.alert('删除失败');
                    }
                });
            },
            btn2:function (index) {
                layer.close(index);
            }
        });
    });
});
