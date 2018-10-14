var provinceCode = {
    "11": "北京市",
    "12": "天津市",
    "31": "上海市",
    "50": "重庆市",
    "13": "河北省",
    "41": "河南省",
    "53": "云南省",
    "21": "辽宁省",
    "23": "黑龙江省",
    "43": "湖南省",
    "34": "安徽省",
    "37": "山东省",
    "65": "新疆维吾尔自治区",
    "32": "江苏省",
    "36": "江西省",
    "42": "湖北省",
    "45": "广西壮族自治区",
    "62": "甘肃省",
    "14": "山西省",
    "15": "内蒙古自治区",
    "61": "陕西省",
    "22": "吉林省",
    "35": "福建省",
    "52": "贵州省",
    "44": "广东省",
    "63": "青海省",
    "54": "西藏自治区",
    "51": "四川省",
    "64": "宁夏回族自治区",
    "46": "海南省",
    "34": "安徽省",
    "101": "香港",
    "102": "澳门",
    "103": "台湾省",
    "0": "海外"
};

var geoCoordMap = {
    "北京市": [116.41667,39.91667],
    "天津市": [117.20000,39.13333],
    "上海市": [121.47333,31.23000],
    "香港": [114.10000,22.20000],
    "广东省": [113.23333,23.16667],
    "浙江省": [120.20000,30.26667],
    "重庆市": [106.45000, 29.56667],
    "福建省": [119.30000,26.08333],
    "甘肃省": [103.73333,36.03333],
    "贵州省": [106.71667,26.56667],
    "湖南省": [113.00000,28.21667],
    "江苏省": [118.78333,32.05000],
    "江西省": [115.90000,28.68333],
    "辽宁省": [123.38333,41.80000],
    "山西省": [112.53333,37.86667],
    "四川省": [104.06667,30.66667],
    "西藏自治区": [91.00000,29.60000],
    "新疆维吾尔自治区": [87.68333,43.76667],
    "云南省": [102.73333,25.05000],
    "陕西省": [108.95000,34.26667],
    "青海省": [101.75000,36.56667],
    "宁夏回族自治区": [106.26667,38.46667],
    "黑龙江省": [126.63333,45.75000],
    "吉林省": [125.35000,43.88333],
    "湖北省": [114.31667,30.51667],
    "河南省": [113.65000,34.76667],
    "海南省": [110.35000,20.01667],
    "河北省": [114.48333,38.03333],
    "澳门": [113.50000,22.20000],
    "内蒙古自治区": [111.748703,40.842532],
    "山东省": [116.7584101167, 36.5598443152,],
    "台湾省": [121.5200760000, 25.0307240000,],
    "安徽省": [117.2922150938, 31.8673137419,],
    "广西壮族自治区": [108.3340400357, 22.8212837740,]
}

var convertData = function (data) {
    var res = [];
    for (var i = 0; i < data.length; i++) {
        // var geoCoord = geoCoordMap[data[i].name];
        var geoCoord = geoCoordMap[provinceCode[data[i]['province_code']]];
        if (geoCoord) {
            res.push({
                name: provinceCode[data[i]['province_code']],
                value: geoCoord.concat(data[i]['num'])
            });
        }
    }
    console.log(res);
    return res;
};


option = {
    // backgroundColor: '#404a59',
    // title: {
    //     text: '全国主要城市空气质量',
    //     subtext: 'data from PM25.in',
    //     sublink: 'http://www.pm25.in',
    //     left: 'center',
    //     textStyle: {
    //         color: '#fff'
    //     }
    // },
    tooltip : {
        trigger: 'item',
        formatter: function(params) {
            return params.data.name + '<br />祝福数量: ' + params.value[2];
        }
    },
    bmap: {
        center: [104.114129, 37.550339],
        zoom: 5,
        roam: true,
        mapStyle: {
            styleJson: [
            {
                "featureType": "water",
                "elementType": "all",
                "stylers": {
                    "color": "#044161"
                }
            },
            {
                "featureType": "land",
                "elementType": "all",
                "stylers": {
                    "color": "#004981"
                }
            },
            {
                "featureType": "boundary",
                "elementType": "geometry",
                "stylers": {
                    "color": "#064f85"
                }
            },
            {
                "featureType": "railway",
                "elementType": "all",
                "stylers": {
                    "visibility": "off"
                }
            },
            {
                "featureType": "highway",
                "elementType": "geometry",
                "stylers": {
                    "color": "#004981"
                }
            },
            {
                "featureType": "highway",
                "elementType": "geometry.fill",
                "stylers": {
                    "color": "#005b96",
                    "lightness": 1
                }
            },
            {
                "featureType": "highway",
                "elementType": "labels",
                "stylers": {
                    "visibility": "off"
                }
            },
            {
                "featureType": "arterial",
                "elementType": "geometry",
                "stylers": {
                    "color": "#004981"
                }
            },
            {
                "featureType": "arterial",
                "elementType": "geometry.fill",
                "stylers": {
                    "color": "#00508b"
                }
            },
            {
                "featureType": "poi",
                "elementType": "all",
                "stylers": {
                    "visibility": "off"
                }
            },
            {
                "featureType": "green",
                "elementType": "all",
                "stylers": {
                    "color": "#056197",
                    "visibility": "off"
                }
            },
            {
                "featureType": "subway",
                "elementType": "all",
                "stylers": {
                    "visibility": "off"
                }
            },
            {
                "featureType": "manmade",
                "elementType": "all",
                "stylers": {
                    "visibility": "off"
                }
            },
            {
                "featureType": "local",
                "elementType": "all",
                "stylers": {
                    "visibility": "off"
                }
            },
            {
                "featureType": "arterial",
                "elementType": "labels",
                "stylers": {
                    "visibility": "off"
                }
            },
            {
                "featureType": "boundary",
                "elementType": "geometry.fill",
                "stylers": {
                    "color": "#029fd4"
                }
            },
            {
                "featureType": "building",
                "elementType": "all",
                "stylers": {
                    "color": "#1a5787"
                }
            },
            {
                "featureType": "label",
                "elementType": "all",
                "stylers": {
                    "visibility": "off"
                }
            }
            ]
        }
    },
    // series : [
    // {
    //     name: 'pm2.5',
    //     type: 'scatter',
    //     coordinateSystem: 'bmap',
    //     data: convertData(data),
    //     symbolSize: function (val) {
    //         return val[2] / 5;
    //     },
    //     label: {
    //         normal: {
    //             formatter: '{b}',
    //             position: 'right',
    //             show: true
    //         },
    //         emphasis: {
    //             show: true
    //         }
    //     },
    //     itemStyle: {
    //         normal: {
    //             color: '#ddb926'
    //         }
    //     }
    // },
    // {
    //     name: 'Top 5',
    //     type: 'effectScatter',
    //     coordinateSystem: 'bmap',
    //     data: convertData(data.sort(function (a, b) {
    //         return b.value - a.value;
    //     }).slice(0, 6)),
    //     symbolSize: function (val) {
    //         return val[2] / 5;
    //     },
    //     showEffectOn: 'emphasis',
    //     rippleEffect: {
    //         brushType: 'stroke'
    //     },
    //     hoverAnimation: true,
    //     label: {
    //         normal: {
    //             formatter: '{b}',
    //             position: 'right',
    //             show: true
    //         }
    //     },
    //     itemStyle: {
    //         normal: {
    //             color: '#f4e925',
    //             shadowBlur: 10,
    //             shadowColor: '#333'
    //         }
    //     },
    //     zlevel: 1
    // }
    // ]
};

function load_data(data2) {
    series = []
    sery = {
        name: 'wish',
        type: 'scatter',
        coordinateSystem: 'bmap',
        data: convertData(data2),
        symbolSize: function (val) {
            return val[2] / 10;
        },
        label: {
            normal: {
                formatter: '{b}',
                position: 'right',
                show: false
            },
            emphasis: {
                show: true
            }
        },
        itemStyle: {
            normal: {
                color: '#ddb926'
            }
        }
    };
    sery2 = {
        name: 'Top 5',
        type: 'effectScatter',
        coordinateSystem: 'bmap',
        data: convertData(data2.sort(function (a, b) {
            return b.value - a.value;
        }).slice(0, 6)),
        symbolSize: function (val) {
            return val[2] / 10;
        },
        showEffectOn: 'emphasis',
        rippleEffect: {
            brushType: 'stroke'
        },
        hoverAnimation: true,
        label: {
            normal: {
                formatter: '{b}',
                position: 'right',
                show: true
            }
        },
        itemStyle: {
            normal: {
                color: '#f4e925',
                shadowBlur: 10,
                shadowColor: '#333'
            }
        },
        zlevel: 1
    };
    sery3 = 
    {
        name: '点',
        type: 'scatter',
        coordinateSystem: 'bmap',
        symbol: 'pin', //气泡
        symbolSize: function(val) {
            var a = (maxSize4Pin - minSize4Pin) / (max - min);
            var b = minSize4Pin - a * min;
            b = maxSize4Pin - a * max;
            return a * val[2] + b;
        },
        label: {
            normal: {
                formatter: function(obj) {
                    console.log(obj);
                    return obj.value[2];
                },
                show: true,
                textStyle: {
                    color: '#fff',
                    fontSize: 9,
                }
            }
        },
        itemStyle: {
            normal: {
                color: '#F62157', //标志颜色
            }
        },
        zlevel: 6,
        data: convertData(data2),
    },
    series.push(sery3);
    series.push(sery2);
    series.push(sery);
    option.series = series;
    chart.setOption(option);
}

$(document).ready(function() {
    $.ajax({
        url: 'http://112.74.183.47:8099/modian/get-birthday-wish/',
        dataType: 'json',
        method: 'GET',
        success: function(data) {
            load_data(data)
        },
        error: function(xhr) {
            console.error('error:' + JSON.stringify(xhr));
        }
    });

    $('#submit-wish').click(function() {
        $(window).attr('location', './wish-form');
    }) 
});

var max = 480,
    min = 1; // todo 
var maxSize4Pin = 100,
    minSize4Pin = 40;

var chart = echarts.init(document.getElementById('map-main'));
chart.showLoading();
chart.setOption(option);
chart.hideLoading();

// 获取百度地图实例，使用百度地图自带的控件
var bmap = chart.getModel().getComponent('bmap').getBMap();
bmap.addControl(new BMap.NavigationControl()); // 缩放控件
bmap.addControl(new BMap.ScaleControl()); // 比例尺