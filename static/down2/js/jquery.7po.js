
function getDeviceList() {
    var qp_url = "http://store.7po.com/api/tuisong";

    function qp_getDeviceList(){
        $.ajax({
            type: "GET",
            url: qp_url,
            dataType: "jsonp",
            cache: false,
            jsonpCallback:"devices",
            success: function(msg) {
                if ($.isEmptyObject(msg)) {
                    $('#ins_wait').hide();
                    $('#ins_nofind').show();
                } else {
                    $('#ins_devices').empty();
                    $('#ins_wait').hide();
                    var apk_url = encodeURIComponent($('#app_install').attr('href'));
                    var icon_url = encodeURIComponent($('#app_install').attr('icon'));
                    var app_name = encodeURIComponent($('#app_install').attr('name'));
                    var app_id = $('#app_install').attr('appid');
                    var pack = $('#app_install').attr('package');
                    for(var key in msg) {
                        $('#ins_devices').append('<a href="http://'+msg[key][0]+'/tuisong?package='+pack+'&appicon='+icon_url+'&appname='+app_name+'&appurl='+apk_url+'&appid='+app_id+'" class="device">'+key+'</a>');
                        $('#ins_devices').show();
                    }
                }
            }
        });
    }

    $.ajax({
        url:"https://jsonip.com",
        async : false,
        cache: false,
        type: "GET",
        timeout: 2000,
        dataType: 'json',
        beforeSend: function() {
            $('#ins_nofind').hide();
            $('#ins_devices').hide();
            $('#ins_wait').show();
        },
        success:function(ip_data){
            if (!($.isEmptyObject(ip_data))) {
                for(var key in ip_data) {
                    if (key == 'ip'){
                        qp_url = qp_url + '?remote_ip=' + ip_data[key];
                        break;
                    }
                }
            }
            qp_getDeviceList();
        },
        error: function(XMLHttpRequest, textStatus) {
            qp_getDeviceList();
        }
    });
}
function pushApp(This) {
    $.ajax({
        type: "GET",
        url: $(This).attr('href'),
        dataType: "jsonp",
        cache:false,
        jsonpCallback:"pushEnd",
        timeout: 2000,
        beforeSend: function() {
            $('#ins_devices').hide();
            $('#ins_wait').show();
        },
        success: function(msg) {
            if (msg.status) {
                $('#ins_finish').html('<p>'+$('#app_install').attr('name')+' 已推送到 '+$(This).text()+'</p>')
                $('#ins_wait').hide();
                $('#ins_finish').show();   
            } else {
                alert('服务器忙，应用推送失败！！！');
                $('#ins_nofind').show();
                $('#ins_wait').hide();
            }
        },
        error: function(XMLHttpRequest, textStatus) {
            $('#ins_nofind').show();
            $('#ins_wait').hide();
        }
    });
}
jQuery(function($){
    $(document).keydown(function(event) {
        if(event.keyCode == 27 && $('.window').length>0) {
            $('.window').remove();
            $('#mask').remove();
        }
    });
    $(document).on('click','.winclose,#mask',function(){
        $('.window').remove();
        $('#mask').remove();
    });
    $(document).on('click','.device',function(){
        pushApp(this);
        return false;
    });
    $(document).on('click','.refind',function(){
        getDeviceList();
        return false;
    });
    $('#app_install').click(function(){
        $('body').append('<div id="mask" style="height:'+$(document).height()+'px;"></div><div class="window"><div class="winhead"><p>远程安装<a class="seehelp" href="http://www.7po.com/thread-428523-1-1.html" target="_blank">使用帮助</a></p><div class="winclose"></div></div><div class="wincontent"><div id="ins_nofind"><p>暂未找到设备<br/>请在电视上打开“奇珀市场”</p><a class="seehelp" href="http://www.7po.com/thread-428523-1-1.html" target="_blank">查看帮助</a><a class="refind">重新查找</a></div><div id="ins_devices"><a class="device">YYY</a></div><div id="ins_finish"><p>已推送XXX到YYY安装</p></div><div id="ins_wait"><p>数据加载中...</p></div></div></div>');
        getDeviceList();
        return false;
    });
    $('.model_sorts li').mouseover(function(){
        $(this).addClass('action').siblings().removeClass('action');
    });
    $('.model_menu a').mouseover(function(){
        var jq_start = $(this).parent().find('.action .act_icon');
        var curr_left = jq_start.offset().left;
        var jq_target = $(this).find('.act_icon');
        $(this).css('color','#2aa468');
        if (jq_target[0] !== jq_start[0]) {
            $(this).addClass('action');
            var targ_left = jq_target.offset().left;
            $(this).removeClass('action');
            var margin_left = targ_left-curr_left;
            var THIS = this;
            jq_start.animate({marginLeft: margin_left-8+'px'}, 300, function(){
                jq_start.removeAttr('style');
                $(THIS).removeAttr('style');
                $(THIS).addClass('action').siblings().removeClass('action');
                var index = $(THIS).index()/2;
                var jq = $(THIS).closest('.model').find('.model_apps li');
                jq.fadeOut('normal');
                jq.eq(index).css('position','absolute').css('top','54px').css('left','0px').fadeIn('normal',function(){
                    $(this).css('position','static');
                });
            });
        }
    });
    $('.overshow').mouseover(function(){
        $('.show',this).show();
    }).mouseleave(function() {
        $('.show',this).hide();
    });
    $('#slide_imgs').hover(function(){
        $('.do',this).show();
    },function(){
        $('.do',this).hide();
    });
    $('#slide_imgs').slide({
        loopBody: '#slide_imgs .focus-list',
        curClass: 'current',
        speed: 500,
        gap: 2000,
        next: '.next',
        prev: '.prev', 
        moveType: 'slide2',
        looping: function(type,idx){    }
    });
    $(window).scroll(function(){
        if ($(document).scrollTop() > 10) $('#scrolltop').show();
        else $('#scrolltop').hide();
        if ($(document).scrollTop() >= 263) {
            if ($('.fix').length == 0) {
                if ($('#category').length>0) {
                    var left = $('#category').offset().left;
                    var clone = $('#category').clone().addClass('fix').css({'position':'fixed','top':'0px','left':left+'px','z-index':'100'});
                    clone.insertAfter('#category');
                }
                if ($('#hot_search').length>0) {
                    var left = $('#hot_search').offset().left;
                    var clone = $('#hot_search').clone().addClass('fix').css({'position':'fixed','top':'0px','left':(left-30)+'px','z-index':'100'});
                    clone.insertAfter('#hot_search');
                }
            }
        } else {
            $('.fix').remove();
        }
    });
    $('#scrolltop').click(function(){
        $("html,body").animate({scrollTop:0},'slow');
    });
    var a=2,c=1,f=1,h=1;
    $('#ajax_apps .go').click(function(){
        if (c<a && f) {
            f = 0;
            var left = parseInt($('#ajax_apps li:first').css('margin-left'))-925;
            $('#ajax_apps li:first').animate({ marginLeft: left },'slow','linear',function(){ 
                f=1;
                if (h) $('#ajax_apps .back').show();
            });
            ++c;
            var last_li = $('#ajax_apps li:last');
            var last_time = last_li.attr("id").substring(4);
            //console.log(last_time);
            $.get('/api/new_app/list?t='+last_time,function(data){
                if (data !== 'false') {
                    $('#ajax_apps .focus-list').append(data);
                    ++a;
                } else {
                    $('#ajax_apps .go').hide();
                }
            });
        }
    });
    $('#ajax_apps .back').click(function(){
        if (f) {
            f = 0;
            var left = parseInt($('#ajax_apps li:first').css('margin-left'))+925;
            $('#ajax_apps li:first').animate({ marginLeft: left },'slow','linear',function(){ 
                f=1;
            });
            --c;
            if (c == 1) {
                $('#ajax_apps .back').hide();
            }
        }
    });
    $('#ajax_apps').hover(function(){
        h=1;
        if(c==1 && a>=2) {
            $('.go',this).show();
            $('.back',this).hide();
        } else if (c == a && c>=2) {
            $('.go',this).hide();
            $('.back',this).show();
        } else {
            $('.do',this).show();
        }
    },function(){
        h=0;
    });
    $('.model_apps .model_app').hover(
        function(){
            $('.app_num',this).css('display','none');
            var offset = $(this).offset();
            var sncard = jQuery.parseJSON($(this).attr('tipdata'));
            $('#sn-name').text(sncard.name);
            $('.sn-top p').text(sncard.down_num+'下载');
            $('.sn-top i').css('width',sncard.mark+'%');
            $('.sn-brief').text(sncard.desc);
            $('.sn-top label').html((sncard.mark/10).toFixed(1));
            $('#sncard').css({'display':'block','top':(offset.top-18)+'px','left':(offset.left+152)+'px'});
            $('.app_btn', this).css('display','inline-block');
        },
        function(){
            $('.app_num',this).css('display','inline-block');
            $('.app_btn', this).css('display','none');
            $('#sncard').css('display','none');
        }
    );
    $('#qrcode').hover(function(){
        $('#contact').show();
    },function(){
        $('#contact').hide();
    });
    $('#slides').slide({
        loopBody: '.focus-list',
        curClass: 'current',
        speed: 500,
        gap: 5000,
        next: '.next',
        prev: '.prev', 
        control: {
            curClass: 'current',
            selector: '.control-list',
            child: 'li'
        },
        moveType: 'dissolve',
        looping: function(type,idx){    }
    });
    $('#slides').hover(function(){
        $('.do',this).show();
    },function(){
        $('.do',this).hide();
    });
});