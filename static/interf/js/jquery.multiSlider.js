(function($){
	function sliderAnimate(dom, num) {
		var multiSlider = $(dom).data('multiSlider');
		var li_width = $(multiSlider.box+' li', dom).outerWidth(true);
		multiSlider.ul_left = multiSlider.ul_left || $(multiSlider.box+' ul', dom).position().left;
		multiSlider.ul_left = multiSlider.ul_left - (num*li_width);
		$(dom).data('multiSlider', multiSlider);
		$(multiSlider.box+" ul", dom).animate({left: multiSlider.ul_left+'px'}, "slow");
		setShow(dom);
	}

	function sliderFirst(dom) {
		var multiSlider = $(dom).data('multiSlider');
		var num = multiSlider.curr_pg - 1;
		multiSlider.curr_pg = 1;
		multiSlider.curr_num = multiSlider.pg_num;
		sliderAnimate(dom, -(multiSlider.pg_num*num));
		$(dom).data('multiSlider', multiSlider);
		setShow(dom);
	}

	function sliderPrev(dom) {
		var multiSlider = $(dom).data('multiSlider');
		multiSlider.curr_pg = multiSlider.curr_pg - 1;
		multiSlider.curr_num = multiSlider.pg_num;
		sliderAnimate(dom, -multiSlider.pg_num);
		$(dom).data('multiSlider', multiSlider);
		setShow(dom);
	}

	function sliderLast(dom) {
		var multiSlider = $(dom).data('multiSlider');
		var num = multiSlider.all_pg - multiSlider.curr_pg;
		multiSlider.curr_pg = multiSlider.all_pg;
		multiSlider.curr_num = multiSlider.all_num%multiSlider.pg_num;
		sliderAnimate(dom, multiSlider.pg_num*num);
		$(dom).data('multiSlider', multiSlider);
		setShow(dom);
	}

	function sliderNext(dom) {
		var multiSlider = $(dom).data('multiSlider');
		multiSlider.curr_pg = multiSlider.curr_pg + 1;
		if (multiSlider.curr_pg == multiSlider.all_pg) multiSlider.curr_num = multiSlider.all_num%multiSlider.pg_num;
		multiSlider.curr_num = multiSlider.curr_num ? multiSlider.curr_num : multiSlider.pg_num;
		sliderAnimate(dom, multiSlider.pg_num);
		$(dom).data('multiSlider', multiSlider);
		setShow(dom);
	}

	function setInit(dom) {
		var multiSlider = $(dom).data('multiSlider');
		multiSlider.li_width = $(multiSlider.box+' li', dom).outerWidth(true);
		var ul_width = multiSlider.li_width * multiSlider.all_num;
		$(multiSlider.box+' ul', dom).css('width', ul_width+'px');
	}

	function setShow(dom) {
		var multiSlider = $(dom).data('multiSlider');
		$(multiSlider.prev, dom).removeClass(multiSlider.doAct);
		$(multiSlider.next, dom).removeClass(multiSlider.doAct);
		$(multiSlider.first, dom).removeClass(multiSlider.doAct);
		$(multiSlider.last, dom).removeClass(multiSlider.doAct);
		if (multiSlider.curr_pg == 1) {
			$(multiSlider.prev, dom).addClass(multiSlider.doAct);
			$(multiSlider.first, dom).addClass(multiSlider.doAct);
		}
		if (multiSlider.curr_pg == multiSlider.all_pg) {
			$(multiSlider.next, dom).addClass(multiSlider.doAct);
			$(multiSlider.last, dom).addClass(multiSlider.doAct);
		}
	}

	function setBind(dom) {
		var multiSlider = $(dom).data('multiSlider');
		$(dom).off('click', multiSlider.prev).on('click', multiSlider.prev, function(){sliderPrev(dom);});
		$(dom).off('click', multiSlider.next).on('click', multiSlider.next, function(){sliderNext(dom);});
		if (multiSlider.first.length > 0) $(dom).off('click', multiSlider.first).on('click', multiSlider.first, function(){sliderFirst(dom);});
		if (multiSlider.last.length > 0) $(dom).off('click', multiSlider.last).on('click', multiSlider.last, function(){sliderLast(dom);});
		//$(dom).on('mouseover', '.slide_prev', function(){});
	}

	$.fn.multiSlider = function(options, param){
		if (typeof options == 'string') {
			return $.fn.multiSlider.methods[options](this, param);
		}
		obj = options || {};
		return this.each(function(){
			var box = obj.box ? obj.box : '.img_box';
			var prev = obj.prev ? obj.prev : '.slide_prev';
			var next = obj.next ? obj.next : '.slide_next';
			var first = obj.first ? obj.first : '';
			var last = obj.last ? obj.last : '';
			var doAct = obj.doAct ? obj.doAct : 'slide_hidden';
			var li_num = $(box+' li', this).length;
			var pg_num = obj.page_num;
			var curr_pg = obj.curr_page ? obj.curr_page : 1;
			var pgs = Math.ceil(li_num/pg_num);
			if (curr_pg == pgs) var curr_num = li_num%pg_num;
			else var curr_num = pg_num;
			curr_num = curr_num ? curr_num : pg_num;
			$(this).data('multiSlider', {box:box,prev:prev,next:next,first:first,last:last,doAct:doAct,all_pg:pgs,curr_pg:curr_pg,pg_num:pg_num,all_num:li_num,curr_num:curr_num});

			setInit(this);
			setShow(this);
			setBind(this);
		});
	}

	$.fn.multiSlider.methods = {
		add: function(dom, index) {
			var multiSlider = $(dom).data('multiSlider');
			multiSlider.all_num = multiSlider.all_num + 1;
			multiSlider.all_pg = Math.ceil(multiSlider.all_num/multiSlider.pg_num);
			if (multiSlider.curr_pg == multiSlider.all_pg) multiSlider.curr_num = multiSlider.all_num%multiSlider.pg_num;
			multiSlider.curr_num = multiSlider.curr_num ? multiSlider.curr_num : multiSlider.pg_num;
			$(dom).data('multiSlider', multiSlider);
			setInit(dom);
			setShow(dom);
			$($(multiSlider.box+' li', dom).get(index)).before('<li><img src="/static/channel/img/channel_default_slider.png" /></li>');
		},
		del: function(dom, index) {
			var multiSlider = $(dom).data('multiSlider');
			if (multiSlider.all_num <= multiSlider.pg_num) {
				alert('无法删除，主题不能少于'+multiSlider.pg_num+'条');
			} else {
				multiSlider.all_num = multiSlider.all_num - 1;
				multiSlider.all_pg = Math.ceil(multiSlider.all_num/multiSlider.pg_num);
				if (multiSlider.curr_pg > multiSlider.all_pg) {
					multiSlider.curr_pg = multiSlider.curr_pg - 1;
					multiSlider.curr_num = multiSlider.pg_num;
					sliderAnimate(dom, -multiSlider.pg_num);
				} else {
					multiSlider.curr_num = multiSlider.curr_num - 1;
				}
				setInit(dom);
				setShow(dom);
				$($(multiSlider.box+' li', dom).get(index)).remove();
			}
		}
	};
})(jQuery)