/*!
 * jQuery Cookie Plugin v1.4.1
 * https://github.com/carhartl/jquery-cookie
 *
 * Copyright 2013 Klaus Hartl
 * Released under the MIT license
 */
(function (factory) {
	if (typeof define === 'function' && define.amd) {
		// AMD
		define(['jquery'], factory);
	} else if (typeof exports === 'object') {
		// CommonJS
		factory(require('jquery'));
	} else {
		// Browser globals
		factory(jQuery);
	}
}(function ($) {

	var pluses = /\+/g;

	function encode(s) {
		return config.raw ? s : encodeURIComponent(s);
	}

	function decode(s) {
		return config.raw ? s : decodeURIComponent(s);
	}

	function stringifyCookieValue(value) {
		return encode(config.json ? JSON.stringify(value) : String(value));
	}

	function parseCookieValue(s) {
		if (s.indexOf('"') === 0) {
			// This is a quoted cookie as according to RFC2068, unescape...
			s = s.slice(1, -1).replace(/\\"/g, '"').replace(/\\\\/g, '\\');
		}

		try {
			// Replace server-side written pluses with spaces.
			// If we can't decode the cookie, ignore it, it's unusable.
			// If we can't parse the cookie, ignore it, it's unusable.
			s = decodeURIComponent(s.replace(pluses, ' '));
			return config.json ? JSON.parse(s) : s;
		} catch(e) {}
	}

	function read(s, converter) {
		var value = config.raw ? s : parseCookieValue(s);
		return $.isFunction(converter) ? converter(value) : value;
	}

	var config = $.cookie = function (key, value, options) {

		// Write

		if (value !== undefined && !$.isFunction(value)) {
			options = $.extend({}, config.defaults, options);

			if (typeof options.expires === 'number') {
				var days = options.expires, t = options.expires = new Date();
				t.setTime(+t + days * 864e+5);
			}

			return (document.cookie = [
				encode(key), '=', stringifyCookieValue(value),
				options.expires ? '; expires=' + options.expires.toUTCString() : '', // use expires attribute, max-age is not supported by IE
				options.path    ? '; path=' + options.path : '',
				options.domain  ? '; domain=' + options.domain : '',
				options.secure  ? '; secure' : ''
			].join(''));
		}

		// Read

		var result = key ? undefined : {};

		// To prevent the for loop in the first place assign an empty array
		// in case there are no cookies at all. Also prevents odd result when
		// calling $.cookie().
		var cookies = document.cookie ? document.cookie.split('; ') : [];

		for (var i = 0, l = cookies.length; i < l; i++) {
			var parts = cookies[i].split('=');
			var name = decode(parts.shift());
			var cookie = parts.join('=');

			if (key && key === name) {
				// If second argument (value) is a function it's a converter...
				result = read(cookie, value);
				break;
			}

			// Prevent storing a cookie that we couldn't decode.
			if (!key && (cookie = read(cookie)) !== undefined) {
				result[name] = cookie;
			}
		}

		return result;
	};

	config.defaults = {};

	$.removeCookie = function (key, options) {
		if ($.cookie(key) === undefined) {
			return false;
		}

		// Must not alter options, thus extending a fresh object...
		$.cookie(key, '', $.extend({}, options, { expires: -1 }));
		return !$.cookie(key);
	};

}));







/*********************************************	cookie	*****************************************/




//购物车
var Cart = function () {
		this.Count = 0;// 购买的商品数量
		this.Total = 0;// 总计金额
		this.Items = new Array();// 购买的商品
};
//购物车集合对象
var CartItem = function () {
  	this.Id = 0; // 商品ID
  	this.Name = "";// 商品名称
  	this.Count = 0;// 购买数量
  	this.Price = 0;// 单价
  	this.imgPath="";// 商品图片路径
};
  
//购物车操作
var CartHelper = function () {
  	this.cookieName = "myCart";
  
  	this.Clear = function () {
    		var cart = new Cart();
    		this.Save(cart);
    		return cart;
  	};
  
  //向购物车添加
  this.Add = function (id, name, count, price, imgPath) {
    	var cart = this.Read();
    	var index = this.Find(id);
    	//如果ID已存在，覆盖数量
    	if (index > -1) {
      		var oldCount = cart.Items[index].Count;
      		var newCount = Number(oldCount) + Number(count);
      		cart.Items[index].Count = newCount;
      		cart.Total += (((cart.Items[index].Count * 100) * (cart.Items[index].Price * 100)) / 10000);
    	} else {
     		 var item = new CartItem();
      		item.Id = id;
      		item.Name = name;
      		item.Count = count;
      		item.Price = price;
      		item.imgPath = imgPath;
      
      		cart.Items.push(item);
      		cart.Count++;
      		cart.Total += (((cart.Items[cart.Items.length - 1].Count * 100) * (cart.Items[cart.Items.length - 1].Price * 100)) / 10000);
   		}
    	this.Save(cart);
    	return cart;
  };
  
  //改变数量
  this.Change = function (id, count) {
    	var cart = this.Read();
    	var index = this.Find(id);
    	cart.Items[index].Count = count;
    	this.Save(cart);
    	return cart;
  };
  
  //移出购物车
  this.Del = function (id) {
    	var cart = this.Read();
    	var index = this.Find(id);
    	if (index > -1) {
      		var item = cart.Items[index];
      		cart.Count--;
      		cart.Total = cart.Total - (((item.Count * 100) * (item.Price * 100)) / 10000);
      		cart.Items.splice(index, 1);
      		this.Save(cart);
    	}
    	return cart;
  };
  
  //根据ID查找
  this.Find = function (id) {
    	var cart = this.Read();
    	var index = -1;
    	for (var i = 0; i < cart.Items.length; i++) {
      		if (cart.Items[i].Id == id) {
        			index = i;
      		}
    	}
    	return index;
  };
  
  //COOKIE操作
  this.Save = function (cart) {
    	var source = "";
    	for (var i = 0; i < cart.Items.length; i++) {
      		if (source != "") { source += "|$|"; }
      				source += this.ItemToString(cart.Items[i]);
    			}
    			$.cookie(this.cookieName, source, {expires:7});
  		};
  
  		this.Read = function () {
    			//读取COOKIE中的集合
    			var source = $.cookie(this.cookieName);
    			var cart = new Cart();
    			if (source == null || source == "") {
     					 return cart;
    			}
    			var arr = source.split("|$|");
    			cart.Count = arr.length;
    			for (var i = 0; i < arr.length; i++) {
      				var item = this.ItemToObject(arr[i]);
      				cart.Items.push(item);
      				cart.Total += (((item.Count * 100) * (item.Price * 100)) / 10000);
    			}
    			return cart;
  		};
  		this.ItemToString = function (item) {
    			return item.Id + "||" + escape(item.Name) + "||" + item.Count + "||" + item.Price + "||" + item.imgPath;
  		};
  
  	this.ItemToObject = function (str) {
  	  	var arr = str.split('||');
  	 	 	var item = new CartItem();
  	 	 	item.Id = arr[0];
  	  	item.Name = unescape(arr[1]);
  	  	item.Count = arr[2];
  	  	item.Price = arr[3];
  	  	item.imgPath = arr[4];
  	  	return item;
  	};
};


/*************************************************	所有操作 	******************************************************/






$(function () {				
	// 创建购物车
	$(window).on("load", function () {
		loadCart();	
		
		//购物车滑过商品名 出现商品详情
		var $a =  $('.cartShop_name_warp>a');
		$a.each(function(){
			$(this).hover(			
				function(){
					var $lastchild = $(this).parents("div").eq(1).children().last();//商品详情
					//console.log($lastchild)
					$lastchild.css('display','block');
				},
				function(){
					var $lastchild = $(this).parents("div").eq(1).children().last();//商品详情
					 $lastchild.css('display','none');
				}
			);
			
		});

		
		//购物车商品的 - cutNum
		$('#cart_warp').on('click','.cutNum',function(){
			
				var num1 = Number($(this).next().val())-1;
				if(num1<=0){
					$(this).next().val(1)
				}else{
					$(this).next().val(num1)
					var id = $('.spanLeft_down').text();
					count=Number($(this).next().val());
					new CartHelper().Change(id,count);
					loadCart();
				}
		});
		

		//购物车商品的 + addNum
		$('#cart_warp').on('click','.addNum',function(){
			var num2 = Number($(this).prevAll().eq(0).val())+1;
			$(this).prevAll().eq(0).val(num2);
			var id = $('.spanLeft_down').text();
			count=Number($(this).prevAll().eq(0).val());
			new CartHelper().Change(id,count);
			loadCart();
		});




		//删除购物车 信息
		$('#cart_warp').on('click','.remove',function(){
		
			var id = $('.spanLeft_down').text();
			new CartHelper().Del(id);
			loadCart();
		});
		
		
		
		//详情页 侧边栏  删除购物车 信息
		$('.shop_area_dl').on('click','.fixed_a',function(){
			var id = $('.spanLeft_down').text();
			new CartHelper().Del(id);
			loadCart();
		});
		
		
		
		
		
		
	});
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	// 加载购物车中的商品
	function loadCart() {
		var carts = new CartHelper().Read();// 读取购物车中的数据
		$(".cart_warp").children().remove();
		$('.shop_area_dl').children().remove();
		// 加载到页面上
		/******************* 加载购买商品信息 BEGIN***********************/
		$.each(carts.Items, function(index,cartItem) {
			// console.log(index + "---" + cartItem);
			// console.log(value);	
			updateCartPage(cartItem.Id, cartItem.Name, cartItem.Count, cartItem.Price, cartItem.imgPath);
		});
		/******************* 加载购买商品信息 END***********************/
		// 加载购物结算信息
		$(".calculate1>span").text(carts.Count);	//购买商品种类
		$(".moneyNum1").text('￥'+carts.Total.toFixed(2));			//总价格
		$('.settleAccounts').text('￥'+(carts.Total).toFixed(2));
	}
	
	$(".add_btn").on("click", function() {
		// 获取商品id
		var id = $('.goodsid>i').text();
		// 获取图片路径
		var imgPath = $('.tb-booth>a').find('img').attr("src");
		// 获取名称
		var goodsName = $('.shop_name').text();
		// 获取单价
		var price = ($('.goodsprice').text()).slice(1);
		// 获取购买数量
		var count = $('.changenum>input').val();
		
		// 写购物车到cookie中
		new CartHelper().Add(id, goodsName, count, price, imgPath);
		
		// 加载购物车中的数据
		loadCart();		
	});
	
	
	
	
	
	
	
	
	
	
	
	
	/********************** 更新页面 ************************/
	function updateCartPage(id, goodsName, count, price, imgPath) {

		//添加图片及其外面的包裹
//		<div class="cartShop_img_warp">
//			<a href="" class="imglink">
//				<img src="../images/mall/444dcd76-82dc-4bac-85f0-bf9d60942902M.jpg.png" />
//			</a>
//		</div>
		$div1 = $('<div>');						//<div id="cartShop" class="cartShop">
		$div1.addClass('cartShop');
			
		$div2 = $('<div>');
		$div2.addClass('cartShop_img_warp');	//<div class="cartShop_img_warp">
		
		$a1 = $('<a>');
		$a1.addClass('imglink').attr("href",'');	//<a href="" class="imglink">
		
		$img1 = $('<img>');
		$img1.attr("src",imgPath);				//<img src="" />
		
		$a1.append($img1);
		$div2.append($a1);
		$div1.append($div2);
		
		

		//添加商品名称 及其周围的包裹
//		<div class="cartShop_name_warp">
//			<a href="" class="cartShop_name">
//				42°西藏天佑德青稞酒-加持 500ml（2瓶装）<i>[特价]</i>
//			</a>
//		</div>
		$div3 = $('<div>');						
		$div3.addClass('cartShop_name_warp');			//<div class="cartShop_name_warp">
		
		$a2 = $('<a>');
		$a2.addClass('cartShop_name').attr("href",'');		//<a href="" class="cartShop_name">
		
		$a2.text(goodsName);
		$div3.append($a2);
		$div1.append($div3);
		
		
//		添加商品单价
//		<div class="cartShop_price">
//			￥299.00
//		</div>
		$div4 = $('<div>');						
		$div4.addClass('cartShop_price');		//<div class="cartShop_price">
		
		$div4.text(price);
		$div1.append($div4);
		
		
//		添加商品数量
//		<div class="cartShop_num">
//			<a class="cutNum" href="javascript:;">-</a>
//			<input class="numValue" type="text" value="1" />
//			<a class="addNum" href="javascript:;">+</a>
//		</div>
		$div5 = $('<div>');						
		$div5.addClass('cartShop_num');		//<div class="cartShop_num">
		
		$a3 = $('<a>');
		$a3.addClass('cutNum').attr("href",'javascript:;').text('-');	//<a class="cutNum" href="javascript:;">-</a>
		$div5.append($a3);
		
		$input = $('<input>');						
		$input.addClass('numValue').attr("type",'text').val(count);	//<input class="numValue" type="text" value="1" />
		$div5.append($input);
		
		$a4 = $('<a>');
		$a4.addClass('addNum').attr("href",'javascript:;').text('+');	//<a class="addNum" href="javascript:;">+</a>
		$div5.append($a4);
		
		$div1.append($div5);
		
		
		//添加商品总额  单价X数量
		//<div class="priceCount">￥299.00</div>
		$div6 = $('<div>');	
		$div6.addClass('priceCount').text('￥'+(price*count).toFixed(2));	//总价计算 涉及到字符串的截取与拼接
		$div1.append($div6);
		//console.log(price.slice(1))
		
		
		//添加操作键
//		<div class="operation">
//			<a class="push" href="javascript:;">加入收藏夹</a>
//			<a class="remove" href="javascript:;">删除</a>
//		</div>
		$div7 = $('<div>');						
		$div7.addClass('operation');	//<div class="operation">
		
		$a5 = $('<a>');
		$a5.addClass('push').attr("href",'javascript:;').text('加入收藏夹');	//<a class="push" href="javascript:;">加入收藏夹</a>
		$div7.append($a5);
		
		$a6 = $('<a>');
		$a6.addClass('remove').attr("href",'javascript:;').text('删除');	//<a class="remove" href="javascript:;">加入收藏夹</a>
		$div7.append($a6);
		
		$div1.append($div7);
		
		
//		<!--商品详情  滑过商品名出现的详情框-->
//		<div class="cartShop_name_area">
//			<span class="spanLeft_up">商品编号</span>
//			<span class="spanCenter_up">商品名称</span>
//			<span class="spanRight_up">数量</span>
//			
//			<span class="spanLeft_down">A0001535</span>
//			<span class="spanCenter_down">42°西藏天佑德青稞酒-加持 500ml（2瓶装）</span>
//			<span class="spanRight_down">2</span>
//		</div>
		$div8 = $('<div>');						
		$div8.addClass('cartShop_name_area');
		
		$span1 = $('<span>');						
		$span1.addClass('spanLeft_up').text('商品编号');
		$div8.append($span1);
		
		$span2 = $('<span>');						
		$span2.addClass('spanCenter_up').text('商品名称');
		$div8.append($span2);
		
		$span3 = $('<span>');						
		$span3.addClass('spanRight_up').text('数量');
		$div8.append($span3);
		
		
		$span4 = $('<span>');						
		$span4.addClass('spanLeft_down').text(id);
		$div8.append($span4);
		
		$span5 = $('<span>');						
		$span5.addClass('spanCenter_down').text(goodsName);
		$div8.append($span5);
		
		$span6 = $('<span>');						
		$span6.addClass('spanRight_down').text('见包装说明');
		$div8.append($span6);
		
		$div1.append($div8);
		
		$('#cart_warp').prepend($div1);   	//将创建的cookie商品 div 加入到购物车
		
		
		
		//将商品种类数 显示到商品详情侧边栏上的购物车区域 数字显示上
		$('.pd_cartnum').text(count);
		

		//商品详情 头部购物车数量显示
		$('.pr_num').text(count);
		
		
		
		//信息加入到提交页面
		$('.sub_img>img').attr("src",imgPath);
		$('.sub_name').text(goodsName);
		$('.sub_num').text(count);
		$('.sub_total').text('￥'+(price*count).toFixed(2));
		$('.sub_totalprice').text('￥'+(price*count-1.58).toFixed(2));
		$('.sub_singleprice').text('￥'+(price*count).toFixed(2));
		$('.sub_nums').text(count+'件商品，总金额为：');
		$('.sub_singleprice').text('￥'+(price*count).toFixed(2));
		
		
		//数量信息加入 用户中心 显示区域
		$('.car_num').text(count);
		
		//将数量 显示在主页面的 头部显示区域
		$('.pr_num').text(count);
		
		//将信息加到提交成功页面
		$('.os_total').text('￥'+(price*count-1.58).toFixed(2));
		
		
		
		
		
		//信息添加到  商品详情 侧边栏
		var $fixed_cartwarp = $('<dt>');
		$fixed_cartwarp.addClass('fixed_cartwarp');		//创建外围包裹
		
		var $fixed_img = $('<img>');
		$fixed_img.attr("src",imgPath).addClass('fixed_img');	
		$fixed_cartwarp.append($fixed_img);						//加入商品图片
		
		var $fixed_name = $('<h2>').text(goodsName);
		$fixed_cartwarp.append($fixed_name);	//加入商品名称
		
		var $fixed_p = $('<p>');
		var $fixed_price = $('<span>').text('￥'+price+' x '+count).addClass('fixed_price');
		$fixed_p.append($fixed_price);					//加入价格
		
		var $fixed_a = $('<a>').text('删除').attr("href",'javascript:;').addClass('fixed_a');
		$fixed_p.append($fixed_a);									//加入删除按钮
		
		
		$fixed_cartwarp.append($fixed_p);
		
		
		$('.shop_area_dl').append($fixed_cartwarp);	//加入到侧边栏购物车
		
		
		var $btn_warp = $('<dd>').addClass("btn_warp");
		var $btn_a = $('<a>').text('去购物车结算').attr('href','myShoppingCart.html').addClass('btn_a');
		$btn_warp.append($btn_a);
		
		$('.shop_area_dl').append($btn_warp);
		
		
		
		
	}
	
	
	
	
	
	
	
	
	
	
	
	
	
	
});