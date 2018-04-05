/* 代码整理：大头网 www.datouwang.com */
; (function ($) {
    $.extend({
        'nicenav': function (con) {
            con = typeof con === 'number' ? con : 600;
            var $lis = $('#nav>li'), $h = $('#buoy')
            $lis.hover(function () {
                $h.stop().animate({
                    'left': $(this).offsetParent().context.offsetLeft
                }, con);
            }, function () {
                $h.stop().animate({
                    'left': '333px'
                }, con);
            })
        }
    });
	
	 $.extend({
        'stnav': function (con) {
            con = typeof con === 'number' ? con : 600;
            var $lis = $('#nav>li'), $h = $('#st')
            $lis.hover(function () {
                $h.stop().animate({
                    'left': $(this).offsetParent().context.offsetLeft
                }, con);
            }, function () {
                $h.stop().animate({
                    'left': '190px'
                }, con);
            })
        }
    });
	
	
    $.extend({
        'rmnav': function (con) {
            con = typeof con === 'number' ? con : 600;
            var $lis = $('#nav>li'), $h = $('#rm')
            $lis.hover(function () {
                $h.stop().animate({
                    'left': $(this).offsetParent().context.offsetLeft
                }, con);
            }, function () {
                $h.stop().animate({
                    'left': '475px'
                }, con);
            })
        }
    });
	
	
	
	
	 $.extend({
        'hdnav': function (con) {
            con = typeof con === 'number' ? con : 600;
            var $lis = $('#nav>li'), $h = $('#hd')
            $lis.hover(function () {
                $h.stop().animate({
                    'left': $(this).offsetParent().context.offsetLeft
                }, con);
            }, function () {
                $h.stop().animate({
                    'left': '50px'
                }, con);
            })
        }
    });
		
    $.extend({
        'synav': function (con) {
            con = typeof con === 'number' ? con : 600;
            var $lis = $('#nav>li'), $h = $('#sy')
            $lis.hover(function () {
                $h.stop().animate({
                    'left': $(this).offsetParent().context.offsetLeft
                }, con);
            }, function () {
                $h.stop().animate({
                    'left': '761px'
                }, con);
            })
        }
    });


    $.extend({
        'zxflnav': function (con) {
            con = typeof con === 'number' ? con : 600;
            var $lis = $('#nav>li'), $h = $('#zxfl')
            $lis.hover(function () {
                $h.stop().animate({
                    'left': $(this).offsetParent().context.offsetLeft
                }, con);
            }, function () {
                $h.stop().animate({
                    'left': '620px'
                }, con);
            })
        }
    });
		
	
}(jQuery));







