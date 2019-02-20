$(function(){
    console.log(123);
    var canshu;
    var reg = /^[\u4e00-\u9fa5]+$/;
    var regnoen = /[\u4e00-\u9fa5]+/;
    var kg = true;
    var kg2 = true;
    var oneLevelName,
        twoLevelName;
    var reg_en = /^[A-Za-z]+$/;
    // var date_now = new Date().getTime();
    var tableName;
    var depname = window.parent.depart;
    // console.log(depname);
    var titMesso;
    var titMesst;
    //修改按钮
    $(".wrapper").on('click',"#update",function(e){
        e.stopPropagation();
        var thisUl;
        var old_table_ch;
        var old_table_en;
        var dier = $(this).parents('.Level_div').find('h3').text().trim();
        switch (dier){
            case "名称":
                thisUl = $(this).parents('ul');
                old_table_ch = $(this).parents("ul").find(".table_ch").text().trim();
                $("#table_ch").val(old_table_ch);
                updateListName(thisUl,"修改名称",old_table_ch);
                break;
            case "表名":
                thisUl = $(this).parents('ul');
                old_table_ch = $(this).parents("ul").find(".table_ch").text().trim();
                old_table_en = $(this).parents("ul").find(".table_en").text().trim();
                $("#table_ch").val(old_table_ch);
                $("#table_en").val(old_table_en);
                updateListName(thisUl,"修改表名",old_table_ch);
                break;
            case "参数":
                thisUl = $(this).parents('ul');
                updateParams(thisUl,"修改参数",$(this));
                break;
            case "字段":
                thisUl = $(this).parents('ul');
                updateParams(thisUl,"修改字段",$(this));
                break;
        }
    });

    //点击添加按钮
    $(".Level_addbtn").click(function(e){
        e.stopPropagation();
        var dier = $(this).parents('.condiv').find('h3').text().trim();
        var luyou;
        switch (dier){
            case "名称":
                $("#table_ch").val('');
                addListName("添加名称");
                break;
            case "表名":
                $("#table_ch").val('');
                $("#table_en").val('');
                addListName("添加表名");
                break;
            case "参数":
                addParams("新增参数")
                break;
            case "字段":
                addParams("新增字段");
                break;
        }
    });
    //点击每一行数据
    $(".tablename").on('click',"ul",function(){
        if($(".table_en").text()){
            tableName = $(this).find(".table_en").text().trim();
        }else{
            tableName = $(this).find(".table_ch").text().trim();
        }
        var dierstr = $(this).attr('class');
        if(!dierstr){
            $(this).toggleClass("active").siblings().removeClass("active");
            var dier = $(this).parents(".Level_div").find('h3').text();
            if(dier == '表名' || dier == '名称'){
                $(".TwoLevel .Level_content").html('');
                oneLevelName = $(this).children().eq(1).text();
                $(".TwoLevel .Level_add input[type='button']").removeAttr('disabled').css("background-color","#0ae").css("cursor","default");
                $.post(metashow,{"tableName":tableName,"depname":depname,"metatype":metatype},function (data) {
                    var fieldData = data.result;
                    var fieldStr = '';
                    console.log(data);
                    for(var i = 0 ; i < fieldData.length; i ++){
                        fieldStr += '<ul>';
                        fieldStr += '<li class="num_field">' + (i + 1) + '</li>';
                        fieldStr += '<li class="fieldname" title=' + fieldData[i].fieldName + '>' + fieldData[i].fieldName + '</li>';
                        fieldStr += '<li class="fielddesc" title=' + fieldData[i].fieldDesc + '>' + fieldData[i].fieldDesc + '</li>';
                        fieldStr += '<li class="fieldtype" title=' + fieldData[i].fieldType + '>' + fieldData[i].fieldType + '</li>';
                        // fieldStr += "<li><a title='修改' class='glyphicon glyphicon-pencil' id='update'></a>&nbsp;";
                        // fieldStr += "<a title='删除' class='glyphicon glyphicon-trash' id='delete'></a></li>";
                        fieldStr += "</ul>";
                    }
                    $(".TwoLevel .Level_content").append(fieldStr);
                });
            }
        }

    });
    //删除
    $(".Level_content").on('click','#delete',function (e) {
        e.stopPropagation();
        var dier = $(this).parents('.Level_div').find('h3').text().trim();
        var thisUl = $(this).parents('ul');
        var table_en;
        layer.confirm('确认删除吗?', {
            title: "提示",
            btn: ["确定", "取消"],
            yes:function (index) {
                switch (dier){
                    case "名称":
                        deleteListName(thisUl);
                        break;
                    case "表名":
                        deleteListName(thisUl);
                        break;
                    case "参数":
                        deleteParams(thisUl);
                        break;
                    case "字段":
                        deleteParams(thisUl);
                        break;
                }
            },
            btn2:function (index) {
                layer.close(index);
            }
        });
    });
    //添加名称或表名
    function addListName(titles) {
        var table_en;
        layer.open({
            area: ['480px', '250px'],
            title: titles,
            content: $('.list_layer'),
            type: 1,
            btn: ["保存", "取消"],
            yes: function (index) {
                var table_ch = $("#table_ch").val().trim().replace(/\s/g,'');
                if($("#table_en").val()){
                    table_en = $("#table_en").val().trim().replace(/\s/g,'');
                    titMesso = "添加失败，表名已存在";
                    titMesst = "表名不能为空";
                }else{
                    table_en = "zzzz";
                    titMesso = "添加失败，名称已存在";
                    titMesst = "名称不能为空";
                }
                if(table_ch != '') {
                    if (table_en != '') {
                        if(!regnoen.test(table_en)){
                            var params = {
                                "table_ch":table_ch,
                                "depname":depname
                            }
                            if(metatype){
                                params.metatype = metatype;
                            }
                            if(table_en != 'zzzz'){
                                params.table_en = table_en;
                            }
                            $.post(route_add,params,function (data) {
                                if(data.result == 1){
                                    layer.alert('添加成功',function (index) {
                                        location.reload();
                                    });
                                }else{
                                    layer.alert(titMesso);
                                }
                            });
                            layer.close(index);
                        }else{
                            layer.alert("表名(英文)：不能为中文",function (index) {
                                layer.close(index);
                                $("#table_en").focus();
                            });
                        }
                    }else{
                        layer.alert('表名(英文)：不能为空',function (index) {
                            layer.close(index);
                            $("#table_en").focus();
                        });
                    }
                }else{
                    layer.alert(titMesst,function (index) {
                        layer.close(index);
                        $("#table_ch").focus();
                    });
                }
            },
            btn2: function (index) {
                layer.close(index);
            }
        });
        myclose = layer.close;
    }
    //添加参数或字段
    function addParams(titles) {
        if($(".table_en").text()){
            tableName = $(".active").find(".table_en").text().trim();
            titMesso = "字段名称不能为空";
        }else {
            tableName = $(".active").find(".table_ch").text().trim();
            titMesso = "参数名称不能为空";
        }
        $("#field_name").val('');
        $("#field_desc").val('');
        $("#field_type").val('');
        layer.open({
            area: ['500px', '300px'],
            title: titles,
            content: $('.add_field'),
            type: 1,
            btn: ["保存", "取消"],
            yes: function (index) {
                var field_name = $("#field_name").val().trim().replace(/\s/g,'');
                var field_desc = $("#field_desc").val().trim().replace(/\s/g,'');
                var field_type = $("#field_type").val().trim().replace(/\s/g,'');
                if(field_name != ''){
                    if(!regnoen.test(field_name)){
                        if(!regnoen.test(field_type)) {
                            var params = {
                                "table_name":tableName,
                                "metatype":metatype,
                                "field_name":field_name,
                                "field_desc":field_desc,
                                "field_type":field_type,
                                "depname":depname
                            }
                            $.post(add_params,params,function (data) {
                                if(data.result == 1){
                                    layer.alert('添加成功');
                                    var fieldStr = '';
                                    var num = Number($(".TwoLevel .Level_content").find("ul:last-child li:first-child").text().trim());
                                    if(!num){
                                        num = 0;
                                    }
                                    fieldStr += '<ul class="content_ul">';
                                    fieldStr += '<li class="num_field">' + (num + 1) + '</li>';
                                    fieldStr += '<li class="fieldname">' + field_name + '</li>';
                                    fieldStr += '<li class="fielddesc">' + field_desc + '</li>';
                                    fieldStr += '<li class="fieldtype">' + field_type + '</li>';
                                    // fieldStr += "<li><a title='修改' class='glyphicon glyphicon-pencil' id='update'></a>&nbsp;";
                                    // fieldStr += "<a title='删除' class='glyphicon glyphicon-trash' id='delete'></a></li>";
                                    fieldStr += "</ul>";
                                    $(".TwoLevel .Level_content").append(fieldStr);
                                }else{
                                    layer.alert('添加失败，字段已存在');
                                }
                            });
                            layer.close(index);
                        }else{
                            layer.alert('字段类型不能为中文',function (index) {
                                layer.close(index);
                                $("#field_type").focus();
                            });
                        }
                    }else{
                        layer.alert('字段名称不能为中文',function (index) {
                            layer.close(index);
                            $("#field_name").focus();
                        });
                    }
                }else{
                    layer.alert('字段名称不能为空',function (index) {
                        layer.close(index);
                        $("#field_name").focus();
                    });
                }
            },
            btn2: function (index) {
                layer.close(index);
            }
        });
        myclose = layer.close;
    }
    //修改名称或表名
    function updateListName(thisUl,titles,old_table_ch) {
        var table_en;
        layer.open({
            area: ['480px', '250px'],
            title: titles,
            content: $('.list_layer'),
            type: 1,
            btn: ["保存", "取消"],
            yes: function (index) {
                var table_ch = $("#table_ch").val().trim().replace(/\s/g,'');
                if($("#table_en").val()){
                    table_en = $("#table_en").val().trim().replace(/\s/g,'');
                    titMesso = "表名不能为空";
                }else {
                    table_en = 'zzzz';
                    titMesso = "名称不能为空";
                }
                if(table_ch != ''){
                    if(table_en != ''){
                        if(!regnoen.test(table_en)){
                            var params = {
                                "old_table_ch":old_table_ch,
                                "table_ch":table_ch,
                                "depname":depname,
                                "metatype":metatype
                            }
                            if(table_en != 'zzzz'){
                                params.table_en = table_en;
                            }
                            $.post(update_name,params,function (data) {
                                if(data.result == 1){
                                    layer.alert('修改成功');
                                    $(thisUl).find('.table_ch').text(table_ch);
                                    $(thisUl).find('.table_en').text(table_en);
                                }else{
                                    layer.alert('修改失败');
                                }
                            });
                            layer.close(index);
                        }else{
                            layer.alert('表名(英文)：不能为中文',function (index) {
                                layer.close(index);
                                $("#table_en").focus();
                            });
                        }
                    }else{
                        layer.alert('表名(英文)：不能为空',function (index) {
                            layer.close(index);
                            $("#table_en").focus();
                        });
                    }
                }else{
                    layer.alert(titMesso,function (index) {
                        layer.close(index);
                        $("#table_ch").focus();
                    });
                }
            },
            btn2: function (index) {
                layer.close(index);
            }
        });
    }
    //修改参数或字段
    function updateParams(thisUl,titles,thiscon) {
        var old_fieldname = $(thiscon).parents("ul").find(".fieldname").text().trim();
        var old_fielddesc = $(thiscon).parents("ul").find(".fielddesc").text().trim();
        var old_fieldtype = $(thiscon).parents("ul").find(".fieldtype").text().trim();
        $("#field_name").val(old_fieldname);
        $("#field_desc").val(old_fielddesc);
        $("#field_type").val(old_fieldtype);
        layer.open({
            area: ['500px', '300px'],
            title: titles,
            content: $('.add_field'),
            type: 1,
            btn: ["保存", "取消"],
            yes: function (index) {
                var field_name = $("#field_name").val().trim().replace(/\s/g,'');
                var field_desc = $("#field_desc").val().trim().replace(/\s/g,'');
                var field_type = $("#field_type").val().trim().replace(/\s/g,'');
                if(field_name != ''){
                    if(!regnoen.test(field_name)){
                        if(!regnoen.test(field_type)){
                            var params = {
                                "tableName":tableName,
                                "old_fieldname":old_fieldname,
                                "metatype":metatype,
                                "field_name":field_name,
                                "field_desc":field_desc,
                                "field_type":field_type,
                                "depname":depname
                            }
                            console.log(params)
                            $.post(update_params,params,function (data) {
                                console.log(data);
                                if(data.result == 1){
                                    layer.alert('修改成功');
                                    $(thisUl).find(".fieldname").text(field_name);
                                    $(thisUl).find(".fielddesc").text(field_desc);
                                    $(thisUl).find(".fieldtype").text(field_type);
                                }else{
                                    layer.alert('修改失败，字段已存在');
                                }
                            });
                            layer.close(index);
                        }else {
                            layer.alert('字段类型不能为中文',function (index) {
                                layer.close(index);
                                $("#field_type").focus();
                            });
                        }
                    }else {
                        layer.alert('字段名称不能中文',function (index) {
                            layer.close(index);
                            $("#field_name").focus();
                        });
                    }
                }else{
                    layer.alert('名称不能为空',function (index) {
                        layer.close(index);
                        $("#field_name").focus();
                    });
                }
            },
            btn2: function (index) {
                layer.close(index);
            }
        });
    }
    //删除名称或表名
    function deleteListName(thisUl) {
        var table_ce;
        if($('.table_en').text()){
            table_ce = $(thisUl).find('.table_en').text().trim();
        }else {
            table_ce = $(thisUl).find('.table_ch').text().trim();
        }

        $.post(del_meta,{"table_en":table_ce,"depname":depname,'metatype':metatype},function (data) {
            if(data.result == 1){
                layer.alert('删除成功');
                $(thisUl).remove();
                var num_tables = $(".num_table");
                $(num_tables).each(function (index,ele) {
                    $(ele).text(index + 1);
                });
                $("#field").html('');
            }else{
                layer.alert('删除失败');
            }
        });
    }
    //删除参数或字段
    function deleteParams(thisUl) {
        var fieldname = $(thisUl).find('.fieldname').text().trim();
        $.post(del_params,{"fieldname":fieldname,"depname":depname, "metatype":metatype},function (data) {
            if(data.result == 1){
                layer.alert('删除成功');
                $(thisUl).remove();
                var num_fields = $(".num_field");
                $(num_fields).each(function (index,ele) {
                    $(ele).text(index + 1);
                });
            }else{
                layer.alert('删除失败');
            }
        });
    }


    var LevelConHei = $(".oneLevel .Level_div").height() - $(".oneLevel .Level_div>h3").height() - 20 - $(".oneLevel .Level_div>ul").height();
    $(".oneLevel .Level_div>.Level_content").css("height",LevelConHei + "px");
    // console.log($(".twoLevel .Level_div>.Level_content"));
    $(".TwoLevel .Level_div>.Level_content").css("height",LevelConHei + "px");
    $(".Level_add").css("line-height",$(".Level_add").height() + 3 + "px");


    $("#meta_synchro").click(function () {
        // layer.open({
        //         area: ['500px', '300px'],
        //         content: $('.add_field'),
        //         type: 1
        //     });
        window.parent.tbDatasBL();
        var count = 0;
        var pinner = window.parent.spinner;
        var timer = setInterval(function () {
            count += 1.5;
            $(pinner).css("transform","rotateZ(" + count + "deg)");
        },10);
        $.post("/metadata_synchro/",{"department":depname},function (data) {
            clearInterval(timer);
            window.parent.tbDataLayer.close(window.parent.tbDataIndex);
            if(data.result) {
                layer.alert("同步成功",function () {
                    window.location.reload();
                });
            } else {
                layer.alert("同步失败");
            }
        });
    });
});
