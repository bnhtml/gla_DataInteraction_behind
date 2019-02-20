$(function () {
    var userDatas = [],
        dataDatas = [],
        safeDatas = [],
        bridgingDatas = [],
        departDatas = [];
    var datas;
    var departs;
    var userNum = 0,
        dataNum = 0,
        safeNum = 0,
        bridgingNum = 0;
    var colors = ['#399','#FFF176','#6cc','#CCFF99','#669','#99CCFF','#66CC99','#ccc','#666699','#009999','#66CCCC','#CCFFFF','#66CCCC','#CCFF66','#FF99CC','#339999','#FFFF00','#336699','#CC9933','#339999','#FFCC33','#FFCC00','#009999','#CC3333','#669999','#CCCCCC','#CC99CC','#339999','#FFCC33','#FFCC00','#009999','#CC3333','#669999','#CCCCCC','#CC99CC'];
    // var colors = ['#f44336','#03A9F4','#8BC34A','#FF9800','#9E9E9E'];
    // $("#top").css({"height":$("#sum_top").height() + 'px',"line-height":$("#sum_top").height() + "px"});
    // console.log($("#sum_top").height());
    // $("#departPie").css({ "width": $("#sum_num").height() + "px", "height": $("#sum_num").height() + "px" })
    var departPie = echarts.init(document.getElementById("departPie"));
    var user_pie = echarts.init(document.getElementById("userPie"));
    var data_pie = echarts.init(document.getElementById("dataPie"));
    var safe_pie = echarts.init(document.getElementById("safePie"));
    var bridging_pie = echarts.init(document.getElementById("bridgingPie"));
    $.get("get_catalogInfo", function (data) {
        datas = data.result;
        $(".sum_top_num").text(datas[0][5]);
        for (var i = 0; i < datas.length; i++) {
            userNum += datas[i][1];
            dataNum += datas[i][2];
            safeNum += datas[i][3];
            bridgingNum += datas[i][4];
        }

        userList();
        dataList();
        safeList();
        bridgingList();
    });
    $.get("/get_departInfo/", function (data) {
        departs = data.result;
        departList();
    });
    function departList() {
        option = {
            // title : {
            //     text: '用户目录(' + userNum + ')',
            //     x:'center',
            //     y: 'bottom',
            //     textStyle:{
            //         fontSize:14,
            //         color:"#606266"
            //     }
            // },
            tooltip: {
                trigger: 'item',
                formatter: "部门：{b}<br/>个数：{c}<br/>占比：{d}%",
                // position:[10,10],
                // extraCssText:'width:180px;height:70px;'
            },
            legend: {
                // orient: 'vertical',
                // top: 'middle',
                // type: 'scroll',
                // orient: 'vertical',
                show: true,
                bottom: 15,
                // bottom: 10,
                left: 'center',
                textStyle: {
		        	fontSize: 12
                },
                itemGap: 10,
                itemWidth: 20,
                itemHeight: 14,
                data: ['国家部门', '省直部门', '地州市部门', '省外部门'],
                formatter: function (name) {
                    return (name.length > 8 ? (name.slice(0, 8) + "...") : name);
                },
                tooltip: {
                    trigger: 'item',
                    formatter: "部门：{b}<br/>个数：{c}<br/>占比：{d}%",
                    // position:[10,10],
                    // extraCssText:'width:180px;height:70px;'
                }
            },
            series: [
                {
                    type: 'pie',
                    radius: '65%',
                    center: ['50%', '50%'],
                    data: [],
                    itemStyle: {
                        normal: {
                            label: { show: false },
                            labelLine: { show: false }
                        },
                        // normal : {
                        //     labelLine : {
                        //         length : 8,
                        //         length2 : 5
                        //     }
                        // },
                        emphasis: {
                            label: { show: false },
                            labelLine: { show: true }
                        }
                    },
                    color: colors
                }
            ]
        };
        // $(departs).each(function(index,event){
        //     console.log(event);
        // });
        // for (var i = 0;i < departs.length; i ++){
        //     option.series[0].data.push({"value":datas[i][1],"name":datas[i][0]});
        // }
        option.series[0].data.push({ "value": departs.country, "name": "国家部门" });
        option.series[0].data.push({ "value": departs.village, "name": "省直部门" });
        option.series[0].data.push({ "value": departs.city, "name": "地州市部门" });
        option.series[0].data.push({ "value": departs.outcity, "name": "省外部门" });
        departPie.setOption(option);
    }

    function userList() {
        option = {
            title: {
                text: '用户目录(' + userNum + ')',
                x: 'center',
                y: 'bottom',
                textStyle: {
                    fontSize: 14,
                    color: "#606266"
                }
            },
            // legend : {
            //     padding : 0
            // },
            tooltip: {
                trigger: 'item',
                formatter: "部门：{b}<br/>个数：{c}<br/>占比：{d}%",
                // position:[10,10],
                // extraCssText:'width:180px;height:70px;'
            },
            series: [
                {
                    type: 'pie',
                    radius: '65%',
                    center: ['50%', '50%'],
                    data: userDatas,
                    itemStyle: {
                        normal: {
                            label: { show: false },
                            labelLine: { show: false }
                        },
                        emphasis: {
                            label: { show: false },
                            labelLine: { show: true }
                        }
                    },
                    color: colors
                }
            ]
        };
        for (var i = 0; i < datas.length; i++) {
            option.series[0].data.push({ "value": datas[i][1], "name": datas[i][0] });
        }
        user_pie.setOption(option);
    }

    function dataList() {
        option = {
            title: {
                text: '数据目录(' + dataNum + ')',
                x: 'center',
                y: 'bottom',
                textStyle: {
                    fontSize: 14,
                    color: "#606266"
                }
            },
            tooltip: {
                trigger: 'item',
                formatter: "部门：{b}<br/>个数：{c}<br/>占比：{d}%",
                // position:[10,10],
                // extraCssText:'width:180px;height:70px;'
            },
            series: [
                {
                    type: 'pie',
                    radius: '65%',
                    center: ['50%', '50%'],

                    data: [],
                    itemStyle: {
                        normal: {
                            label: { show: false },
                            labelLine: { show: false }
                        },
                        emphasis: {
                            label: { show: false },
                            labelLine: { show: true }
                        }
                    },
                    color: colors
                }
            ]
        };
        for (var i = 0; i < datas.length; i++) {
            option.series[0].data.push({ "value": datas[i][2], "name": datas[i][0] });
        }
        data_pie.setOption(option);
    }

    function safeList() {
        option = {
            title: {
                text: '安全目录(' + safeNum + ')',
                x: 'center',
                y: 'bottom',
                textStyle: {
                    fontSize: 14,
                    color: "#606266"
                }
            },
            tooltip: {
                trigger: 'item',
                formatter: "部门：{b}<br/>个数：{c}<br/>占比：{d}%",
                // position:[10,10],
                // extraCssText:'width:180px;height:70px;'
            },
            series: [
                {
                    type: 'pie',
                    radius: '65%',
                    center: ['50%', '50%'],

                    data: [],
                    itemStyle: {
                        normal: {
                            label: { show: false },
                            labelLine: { show: false }
                        },
                        emphasis: {
                            label: { show: false },
                            labelLine: { show: true }
                        }
                    },
                    color: colors
                }
            ]
        };
        for (var i = 0; i < datas.length; i++) {
            option.series[0].data.push({ "value": datas[i][3], "name": datas[i][0] });
        }
        safe_pie.setOption(option);
    }

    function bridgingList() {
        option = {
            title: {
                text: '数据桥接(' + bridgingNum + ')',
                x: 'center',
                y: 'bottom',
                textStyle: {
                    fontSize: 14,
                    color: "#606266"
                }
            },
            tooltip: {
                trigger: 'item',
                formatter: "部门：{b}<br/>个数：{c}<br/>占比：{d}%",
                // position:[10,10],
                // extraCssText:'width:180px;height:70px;'
            },
            series: [
                {
                    type: 'pie',
                    radius: '65%',
                    center: ['50%', '50%'],

                    data: [],
                    itemStyle: {
                        normal: {
                            label: { show: false },
                            labelLine: { show: false }
                        },
                        emphasis: {
                            label: { show: false },
                            labelLine: { show: true }
                        }
                    },
                    color: colors
                }
            ]
        };
        for (var i = 0; i < datas.length; i++) {
            option.series[0].data.push({ "value": datas[i][4], "name": datas[i][0] });
        }
        bridging_pie.setOption(option);
    }

})
