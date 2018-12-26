$(function(){
	
	//点开或 刷新页面 屏幕广告
	$('.fixed_img_X').on('click',function(event){
		event.preventDefault();

		$("#fixed_opa").css('display','none');
		$("#fixed_img").css('display','none');
	});
	
	
	
	//主页 头部 微博 微信 二维码 显示与隐藏
	$('.weixin').hover(
		function(){
			$('.weixin2').stop().fadeIn(); //二维码显示
		},
		function(){
			$('.weixin2').stop().fadeOut(); //二维码隐藏
		}
	);
	
	$('.weibo').hover(
		function(){
			$('.weibo2').stop().fadeIn(); //二维码显示
		},
		function(){
			$('.weibo2').stop().fadeOut(); //二维码隐藏
		}
	);
	
	//导航 全部商品分类  
	var $ali = $('#center_left>li');
	$ali.each(function(){
		$(this).hover(
			function(){
				$(this).first().css('backgroundColor','#b81c22');
				$(this).find('div').show(); //滑过li 当前之下的div 显示
			},
			function(){
				$(this).find('div').hide();  //滑出li 当前之下的div 隐藏
				$(this).first().css('backgroundColor','');
			}	
		);
	
	});
	
	
	//******** 主页轮播 放在slide.js  **********

	//用户中心导航效果
	$(".user_all_goods").hover(
		function(){
			$(".user_banner_center").css('display','block')
		},
		function(){
			$(".user_banner_center").css('display','none');
		}
	);
	
	
	//主页 板块下 商标 滑过显示商标名
	var $aLi = $('#whiteSpiritBottom li');			
	$aLi.each(function(){
		$(this).hover(
			function(){
				var $span = $(this).children("span");
				$span.show().animate({top:0,height:65,fontSize:14,borderRadius:5},300);
			},
			function(){
				var $span = $(this).children("span");
				$span.animate({top:32,height:0,fontSize:0},300,function(){
					$span.hide();
				})
			}
		);
	});
	
	
	
	$(window).on("scroll",function() {
		//主页 右侧浮动框的显示 与出现
		var $scrolltop = $(window).scrollTop();  //获取滚动条高度
		
		if($scrolltop>1000){                   //滚动条大于1000出现 否则消失 卷帘效果
			$('#fixed_nav').slideDown(1000);   //出现
		}else{
			$('#fixed_nav').slideUp(1000);     //隐藏
		}
		
		
		//我的中酒 用户中心 菜单吸顶
//		if($scrolltop>252){
//			$('.accountSide').addClass('account_top')
//		}else if($scrolltop<252){
//			$('.accountSide').removeClass('account_top')
//			$('.accountSide').removeClass('active_absolute')
//		}
		
		
		
		$height1 = $('#userCenter_center').height();	//包含左侧导航栏 中间大区域的高度
		$height2 = $('.accountSide').height();         //左侧导航栏的高度

		
		if($scrolltop<252){
			$('.accountSide').removeClass('active_absolute');
			$('.accountSide').removeClass('account_top');
		}else if($scrolltop>252&&$scrolltop<($height1-$height2+250)){
			$('.accountSide').removeClass('active_absolute');
			$('.accountSide').addClass('account_top');
		}else if($scrolltop>($height1-$height2+250)){
			$('.accountSide').removeClass('account_top');
			$('.accountSide').addClass('active_absolute');
		}
		

		
		var $clientHeight = $(window).height();
		var $chid = $("#userCenter_center").children("#accountSetting_warp");
		$chid.each(function(index){
			if($scrolltop>=$(this).offset().top-$clientHeight/10&&$scrolltop<=$(this).offset().top){
				//console.log(index)  记录下标
				$(".accountSide").find('a').removeClass('active')
				$(".accountSide").find('a').eq(index).addClass('active');
			}
		});
	
	});
	
	
	
	
	//我的中酒 用户中心 楼梯效果
	$(".accountSide").find('a').each(function(index){
		$(this).on('click',function(){
			$(".accountSide").find('a').removeClass('active')
			$(this).addClass('active');
			var $chid = $("#userCenter_center").children("#accountSetting_warp");
			var $gotop = $chid.eq(index).offset().top;
			$('body,html').animate({scrollTop:$gotop},500);
			
		});

	});	
			
	
	
	
	//主页 回到顶部
	$('.goTop').on("click",function(){
        $('body,html').animate({scrollTop:0},1000);  
	});



	//用户中心 个人资料 详细信息 点击事件
	$('.nav_a1').on('click',function(){
		$('.nav_a').removeClass('active_new_a');
		$('.nav_a1').addClass("active_new_a");	
		$('.personalData_table').css('display','block');
		$('.detailedInformation_table').css('display','none');
		$('#setting').css('height',245);
	});
	$('.nav_a2').on('click',function(){
		$('.nav_a').removeClass('active_new_a');
		$('.nav_a2').addClass("active_new_a");	
		$('.personalData_table').css('display','none');
		$('.detailedInformation_table').css('display','block');
		$('#setting').css('height',800);
	});
	//用户中心 个人资料 详细信息 滑过事件
	$('.nav_a').each(function(){
		$(this).hover(
			function(){
				$(this).addClass("active_nav");
			},
			function(){
				$(this).removeClass("active_nav");
			}
		);
		
	});
		

	

	

	//购物车商品的 - cutNum
	var $cutNum = $('.cutNum');
	$cutNum.each(function(){
		$(this).on('click',function(){
			var num1 = Number($(this).next().val())-1;
			if(num1<=0){
				$(this).next().val(1)
			}else{
				$(this).next().val(num1)
			}	
		});
	});

	//购物车商品的 + addNum
	var $addNum = $('.addNum');
	$addNum.each(function(){
		$(this).on('click',function(){
			var num2 = Number($(this).prevAll().eq(0).val())+1;
			$(this).prevAll().eq(0).val(num2)	
		});
	});
	
	
	//帮助中心 侧边栏 点击事件
	$dt = $('#nav_underline_left dt');
	//console.log($dt)
	$dt.each(function(){
		$(this).on('click',function(){
			$dt.next().css('display','none');
			$(this).next().css('display','block');
			$dt.css('background','#f8f6f4 url(../images/login/sidebar2.png) no-repeat 20px -27px');
			$(this).css('background','#f8f6f4 url(../images/login/sidebar2.png) no-repeat 19px 20px');
		});
	});
	
	
	//	品牌特卖
	$('.list1').each(function(){
		$('.list1').on('click',function(){
			$(this).parents().eq(0).find('li>ul').css('display','none')
			$(this).children('ul').css('display','block')
			$(this).parents().eq(0).children().removeClass('methidli')
			
			$(this).addClass('methidli');
			
		});
	});
		
	
//	主页内容区 选项卡 及标题下红色三角的运动
	$('.whiteSpirit_nav').each(function(){
		$(this).on('mouseenter',function(){
			var num = $(this).index()
			$('.whiteSpirit_nav').removeClass('select')
			$(this).addClass('select')
			
			$('.whiteSpiritCenter>.whiteSpiritCenter_center').each(function(){

				$('.whiteSpiritCenter>.whiteSpiritCenter_center').css('display','none')
				$('.whiteSpiritCenter>.whiteSpiritCenter_center').eq(num-2).css('display','block')

			});
			
			$('#icon_v').stop(false).animate({left:574+92*(num-2)})
		});
		
	});
	
	
	
	//购物车 去结算按钮
	$('.payment').on('click',function(){
		$('.payment').css('display','none');
		$('.load_skip').css('display','block');
		setTimeout(function(){window.location="orderSubmit.html";},1000);
	});
	
	
	
	//订单提交页面 提交订单按钮
	$('.sub_btn').on('click',function(){
		$('.sub_btn').css('display','none');
		$('.load_sub').css('display','block');
		setTimeout(function(){window.location="ordersucceed.html";},1000);
	});
	
	
	
    
        
	
	
	
	
}); 
















	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	

