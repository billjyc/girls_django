'use strict';

function convertLatLntToProvince(resolve, reject, lng, lat) {
	var geoc = new BMap.Geocoder();
	var pt = new BMap.Point(lng, lat)
	geoc.getLocation(pt, function(rs) {
		if(rs) {
			var addComp = rs.addressComponents;
			console.log(addComp.province + ", " + addComp.city + ", " + addComp.district + ", " + addComp.street + ", " + addComp.streetNumber);
			resolve(addComp)
		} else {
			reject(Error('网络错误'))
		}
		
	});
}


function locate(resolve, reject) {
    console.log('method locate()...')
	var geolocation = new BMap.Geolocation();
	var rst = {};
	geolocation.getCurrentPosition(function(r){
		if(this.getStatus() == BMAP_STATUS_SUCCESS){
			// var mk = new BMap.Marker(r.point);
			// map.addOverlay(mk);
			// map.panTo(r.point);
			console.log('您的位置：'+r.point.lng+','+r.point.lat);
			rst["lng"] = r.point.lng;
			rst["lat"] = r.point.lat;
			convertLatLntToProvince(resolve, reject, rst.lng, rst.lat);
		}
		else {
			alert('failed '+this.getStatus());
		}        
	});
}

var provinceCode = {
	"北京市": 11,
	"天津市": 12,
	"上海市": 31,
	"重庆市": 50,
	"河北省": 13,
	"河南省": 41,
	"云南省": 53,
	"辽宁省": 21,
	"黑龙江省": 23,
	"湖南省": 43,
	"山东省": 37,
	"新疆维吾尔自治区": 65,
	"江苏省": 32,
	"浙江省": 33,
	"江西省": 36,
	"湖北省": 42,
	"广西壮族自治区": 45,
	"甘肃省": 62,
	"山西省": 14,
	"内蒙古自治区": 15,
	"陕西省": 61,
	"吉林省": 22,
	"福建省": 35,
	"贵州省": 52,
	"广东省": 44,
	"青海省": 63,
	"西藏自治区": 54,
	"四川省": 51,
	"宁夏回族自治区": 64,
	"海南省": 46,
	"安徽省": 34,
	"香港": 101,
	"澳门": 102,
	"台湾省": 103,
	"海外": 0
};

//ajax在发送之前，做的header头
function csrfSafeMethod(method) {
    // 匹配method的请求模式，js正则匹配用test
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
};

$(function() {
	$('#submit').attr('disabled', true);
	$('#submit').text('正在获取IP中，请稍等...');
	//全局配置jquery ajax请求填上防止跨域请求伪造的http头X-XSRF-TOKEN
	// 为ajax请求做csrf_token
	$.ajaxSetup({
		beforeSend:function (xhr, settings) {
	            // 在请求头设置一次csrf_token,除了上面正则匹配到的不带csrf_token，其他的都要带
	            if(!csrfSafeMethod(settings.type)){
	            	xhr.setRequestHeader("x-CSRFToken", $.cookie("csrftoken"));
	            }
	        }
	    });

	var province = '';
	var pm = new Promise(locate)
	pm.then(function(addComp) {
		// console.log(addComp);
		province = addComp.province;
		// console.log(province);

        if(provinceCode[province]) {
		    $('#province_code').val(provinceCode[province]);
		} else {
		    console.log('在国外');
		    $('#province_code').val(0);
		}
		// console.log($('#province_code').val());

		// console.log(returnCitySN["cip"]);
		$('#ip').val(returnCitySN["cip"]);
		$('#submit').removeAttr('disabled');
		$('#submit').text('提交');
	});

	$('#submit').on("click", function() {
		console.log(province);
		$('#submit').attr('disabled', true);
		console.log($("#birthday_wish").val().length);
		console.log($("#userid").val().length);
		$('#form').ajaxSubmit({
			url: 'http://112.74.183.47:8099/modian/submit-birthday-wish/',
			type: "POST",
			data: $('#form').serialize(),
			dataType: "JSON",
			success: function(data) {
				console.log(data);
				$('#submit').removeAttr('disabled')
				alert('提交成功');
				$(window).attr('location', './birthday-index');
			},
			error: function() {
				console.log('error');
				$('#submit').removeAttr('disabled')
				alert('提交失败，请检查网络');
			}
		});
	});

	$('#form').bootstrapValidator({
	    feedbackIcons: {
            valid: 'glyphicon glyphicon-ok',
            invalid: 'glyphicon glyphicon-remove',
            validating: 'glyphicon glyphicon-refresh'
        },
        fields: {
            user_id: {
                message: 'ID验证失败',
                validators: {
                    notEmpty: {
                        message: 'ID不能为空'
                    },
                    stringLength: {/*长度提示*/
                        max: 24,
                        message: '用户名长度必须在24以下'
                    },
                }
            },
            birthday_wish: {
                message: '生日祝福验证失败',
                validators: {
                    notEmpty: {
                        message: '生日祝福不能为空'
                    },
                    stringLength: {/*长度提示*/
                        max: 120,
                        message: '生日祝福长度必须在120以下' //120
                    }
                }
            }
        }
	});
})

