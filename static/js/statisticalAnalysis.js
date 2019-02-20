//基于浏览器
var pieChar;
//top10
var lineChar;
//http成功失败
var requestChar;
//时间段
var timerSlotChar;
//数据目录3D
var mainChar;
//数据
var datas;
//客户端饼图数据
var clientData = [];
//网络状态饼图数据
var httpstatusData = [];
//数据目录3D数据
var ipServiceCountData = [];

$(function () {
    lineChar = echarts.init(document.getElementById("lineGraph"));
    timerSlotChar = echarts.init(document.getElementById("timeSlot"));
    // mainChar = echarts.init(document.getElementById("main"));
    $.post("/superAdmin/staAnaDatas/",function (data) {
        console.log(data);
        datas = data;
        for(var i = 0; i < datas.client.length; i ++){
            clientData.push([datas.client[i].data,datas.client[i].num]);
        }
        for(var j = 0; j < datas.httpstatus.length; j ++){
            httpstatusData.push([datas.httpstatus[j].data,datas.httpstatus[j].num]);
        }
        pieCharData(clientData);
        lineGraphData();
        timeSlotData();
        requestResultsData(httpstatusData);
        // contentData();
    });







});

//客户端(饼图)
function pieCharData(clientData) {
    pieChar = Highcharts.chart('pieChart', {
        chart: {
            type: 'pie',
            backgroundColor: 'rgba(0,0,0,0)',
            options3d: {
                enabled: true,
                alpha: 45,
                beta: 0
            }
        },
        title: {
            text: '数据资源客戶端访问占比',
            textAlign: 'left'
        },
        tooltip: {
            pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
        },
        plotOptions: {
            pie: {
                allowPointSelect: true,
                cursor: 'pointer',
                depth: 35,
                dataLabels: {
                    enabled: true,
                    format: '{point.name}'
                }
            }
        },
        series: [{
            type: 'pie',
            name: '客户端访问占比',
            data: clientData
        }],

        credits: {
            enabled: false
        }
    });

}
//TOP10(线图)
function lineGraphData() {
    option = {
        title: {
            text: '数据资源历史访问Top10',
            left: 'center'
        },
        color: ['#3398DB'],
        tooltip : {
            trigger: 'axis',
            axisPointer : {            // 坐标轴指示器，坐标轴触发有效
                type : 'shadow'        // 默认为直线，可选为：'line' | 'shadow'
            },
            formatter: function (data) {
                return "数据资源名称：" + data[0].data.name + "<br/>访问次数：" + data[0].data.value;
            }
        },
        grid: {
            left: '3%',
            right: '4%',
            bottom: '3%',
            containLabel: true
        },
        xAxis : [
            {
                type : 'category',
                data : ['1','2','3','4','5','6','7','8','9','10'],
                axisTick: {
                    alignWithLabel: true
                }
            }
        ],
        yAxis : [
            {
                type : 'value'
            }
        ],
        series : [
            {
                // name:'直接访问',
                type:'bar',
                barWidth: '60%',
                data:[]
            }
        ]
    };
    for(var i = 0; i < datas.totalTop.length; i ++){
        option.series[0].data.push({"name":datas.totalTop[i].data,"value": datas.totalTop[i].num});
    }
    lineChar.setOption(option);
}

//http状态(饼图)
function requestResultsData(httpstatusData) {
    requestChar = Highcharts.chart('requestResults', {
        chart: {
            type: 'pie',
            backgroundColor: 'rgba(0,0,0,0)',
            options3d: {
                enabled: true,
                alpha: 45,
                beta: 0
            }
        },
        title: {
            text: '数据资源访问状态占比'
        },
        tooltip: {
            pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
        },
        plotOptions: {
            pie: {
                allowPointSelect: true,
                cursor: 'pointer',
                depth: 35,
                dataLabels: {
                    enabled: true,
                    format: '{point.name}'
                }
            }
        },
        series: [{
            type: 'pie',
            name: '状态次数占比',
            data: httpstatusData
        }],

        credits: {
            enabled: false
        }
    });
}

//时间段
function timeSlotData() {
    option = {
        title: {
            text: '数据资源今日访问Top10',
            left: 'center'
        },
        color: ['#3398DB'],
        tooltip : {
            trigger: 'axis',
            axisPointer : {            // 坐标轴指示器，坐标轴触发有效
                type : 'shadow'        // 默认为直线，可选为：'line' | 'shadow'
            },
            formatter: function (data) {
                return "数据资源名称：" + data[0].data.name + "<br/>访问次数：" + data[0].data.value;
            }
        },
        grid: {
            left: '3%',
            right: '4%',
            bottom: '3%',
            containLabel: true
        },
        xAxis : [
            {
                type : 'category',
                data : ['1','2','3','4','5','6','7','8','9','10'],
                axisTick: {
                    alignWithLabel: true
                }
            }
        ],
        yAxis : [
            {
                type : 'value'
            }
        ],
        series : [
            {
                // name:'直接访问',
                type:'bar',
                barWidth: '60%',
                data:[]
            }
        ]
    };
    for(var i = 0; i < datas.dayTop.length; i ++){
        option.series[0].data.push({"name":datas.dayTop[i].data,"value": datas.dayTop[i].num});
    }
    timerSlotChar.setOption(option);
}

//数据目录3D
function contentData() {
    var num = 0;
    var serviceName = {};
    var days = [];
    var count = 0;
    var data = [];
    for (var i = 0; i < datas.ipServiceCount.length; i ++) {
        serviceName[datas.ipServiceCount[i].data] = 1;
    }
    for (var hh in serviceName){
        ipServiceCountData.push({"serName":hh,"nums":num,"x":0});
        days.push(hh);
        num ++;
    }
    console.log(ipServiceCountData)
    for (var j = 0; j < datas.ipServiceCount.length; j ++){
        for (var k = 0; k < ipServiceCountData.length; k ++){
            if(datas.ipServiceCount[j].data == ipServiceCountData[k].serName){
                data.push([datas.ipServiceCount[j].ip,ipServiceCountData[k].nums,ipServiceCountData[k].x,datas.ipServiceCount[j].num]);
                ipServiceCountData[k].x += 1;
            }
        }
    }
    console.log(data);
    var hours = ['','','','','','','','','',''];


    option = {
        tooltip: {
            textStyle: {
                align: "left"
            },
            // backgroundColor:"pink",
            trigger: "item",
            formatter: function (data) {
                return "访问IP:" + data.data.dataName + "</br>" + "访问次数:" + data.data.value[2];

            }
        },

        visualMap: {
            max: 50,
            inRange: {
                color: ['#313695', '#4575b4', '#74add1', '#abd9e9', '#e0f3f8', '#ffffbf', '#fee090', '#fdae61', '#f46d43', '#d73027', '#a50026']
            },
            show:false
        },
        xAxis3D: {
            type: 'category',
            data: hours
        },
        yAxis3D: {
            type: 'category',
            data: days
        },
        zAxis3D: {
            type: 'value'
        },
        grid3D: {
            boxWidth: 200,
            boxDepth: 80,
            light: {
                main: {
                    intensity: 1.2
                },
                ambient: {
                    intensity: 0.3
                }
            }
        },
        series: [{
            type: 'bar3D',
            data: data.map(function (item) {
                return {
                    value: [item[2], item[1], item[3]],
                    dataName: item[0]
                }
            }),
            shading: 'color',
            label: {
                show: false,
                textStyle: {
                    fontSize: 16,
                    borderWidth: 1
                }
            },

            itemStyle: {
                opacity: 0.6
            },
            emphasis: {
                label: {
                    textStyle: {
                        fontSize: 20,
                        color: '#0ae'
                    }
                },
                itemStyle: {
                    color: '#0ae'
                }
            }
        }]
    }

    mainChar.setOption(option);
}