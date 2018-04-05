(function($,window){
$.fn.slide = function(options){
	return this.each(function(){
		var o = $.extend({},$.fn.slide.options, options || {}),
		
			loopBody = $(o.loopBody),
			loops = loopBody.children();
		
		if(loops.length <= 1) return;
		
		var control = $(o.control.selector),
	    	conChilds,
	    	conCurClass,
	    	
	    	isLoop = true,
	    	timer = null,
	    	curClass = o.curClass,
	        cell = 0,
	        timeDo = new Date().getTime(),
	        
	        moveType = o.moveType,
	        
	        start = function(){
	    		clearTimeout(timer);
	            timer = setTimeout(autoPlay,o.gap);
	            isLoop = true;
	        },
	        
	        stop = function(){
            	clearTimeout(timer);
            	isLoop = false;
            },
            
            autoPlay = function(){
	        	jump('+');
	        },
	        
	        jump = function(type,idx){
            	var c = loopBody.children(),cur,next;
            	if(idx === undefined){
            		cur = c.filter('.' + curClass);
            		if(type === '+'){
            			next = cur.next();
            			if(!next.length) next = c.eq(0);
            		}else{
            			next = cur.prev();
            			if(!next.length) next = c.eq(-1);
            		}
            		idx = next.index();
            	}
            	
            	move(type,idx);
            },
            
            move = function(type,idx){
            	var i = 0,
            		len = moves.length;
            	do{
            		moves[i++](type,idx);
            	}while(i < len);
            },
            
            controlMove = function(type,idx){
            	conChilds.eq(idx).addClass(conCurClass).siblings('.' + conCurClass).removeClass(conCurClass);
            },
            
            slideMove = function(type,idx){
            	var currentLoop = loops.filter('.' + curClass),
	        		nextLoop = loops.eq(idx),
	        		left = 0;
            	
        		if(type === '+'){
	        		nextLoop.css('margin-left', cell+'px');
	        		left = -cell;
	        	}else{
	        		nextLoop.css('margin-left', -cell+'px');
	        		left = cell;
	        	}
        		
        		nextLoop.addClass(curClass);
	        	timeDo = new Date().getTime();
        		nextLoop.animate({ marginLeft: 0 },o.speed,o.easing,function(){
	        		nextLoop.addClass(curClass);
	            });
            	currentLoop.animate({ marginLeft: left },o.speed,o.easing,function(){
            		currentLoop.removeClass(curClass);
	            	if(isLoop) start();
	            	o.loopEnd(type,idx);
            	});
            },
            slide2Move = function(type,idx){
                var currentLoop = loopBody.children().filter('.' + curClass),
                    nextLoop = loopBody.children().eq(idx),
                    left = -cell;
                
                timeDo = new Date().getTime();
                nextLoop.addClass(curClass);

                if(type === '+'){
                    currentLoop.animate({ marginLeft: left },o.speed,o.easing,function(){
                        currentLoop.removeClass(curClass).appendTo(loopBody).removeAttr('style');
                        if(isLoop) start();
                        o.loopEnd(type,idx);
                    });
                }else{
                    nextLoop.prependTo(loopBody).css({ marginLeft: left }).animate({marginLeft: 0}, o.speed,o.easing,function(){
                        currentLoop.removeClass(curClass);
                        nextLoop.removeAttr('style');
                        if(isLoop) start();
                        o.loopEnd(type,idx);
                    });
                }
                
            },
            dissolveMove = function(type,idx){
            	var currentLoop = loops.filter('.' + curClass),
        			nextLoop = loops.eq(idx);
            	
            	timeDo = new Date().getTime();
            	currentLoop.animate({ opacity: 0},o.speed,o.easing,function(){
	        		$(this).removeClass(curClass);
	        	});
            	nextLoop.animate({ opacity: 1},o.speed,o.easing,function(){
	        		$(this).addClass(curClass);
	        		if(isLoop) start();
	        		o.loopEnd(type,idx);
	        	});
            },
            
	        resize = function(){
	        	var lb = loopBody;
        		cell = lb.width();
        		loops.width(cell);
        		loops.not('.current').css('margin-left', cell+'px');
            },
            
            canMove = function(){
            	var now = new Date().getTime();
        		if((now - timeDo) < o.speed) return false;
        		timeDo = now;
        		return true;
            },
            
            controlClick = function(e){
            	clearTimeout(timer);
            	var t = $(e.target).closest(conChilds[0].tagName,this),
            		nextIdx,curIdx,type;
            	if(t.length && !t.is('.' + conCurClass) && canMove()){
            		nextIdx = t.index(o.control.selector + ' ' + o.control.child);
                	curIdx = t.siblings('.' + conCurClass).index(o.control.selector + ' ' + o.control.child);
                	type = nextIdx > curIdx ? '+' : '-';
	        		isLoop = true;
	        		jump(type,nextIdx);
            	}
            },
            
            moves = [],
            
            setMoves = function(){
            	if(control.length){
            		conChilds = control.children(o.control.child);
            		conCurClass = o.control.curClass
            		control.bind('click',controlClick);
        	    	moves.push(controlMove);
            	}
            	moves.push(o.looping);
            };
            
            
	     if(o.moveType == 'slide'){   
	    	 resize();
	    	 moves.push(slideMove);
	    	 //$(window).resize(resize);
	     } else if (o.moveType == 'slide2') {
            cell = 366;
            moves.push(slide2Move);
         }else{
	    	 moves.push(dissolveMove);
	     }
	     
	     setMoves();
	     
	     start();
	     
	     $(this).hover(stop,start);
	     
	     if(o.prev){
         	$(o.prev).on('click',function(){
         		clearTimeout(timer);
         		if(canMove()){
         			jump('-');
         		}
         		return false;
         	});
         }
         
         if(o.next){
         	$(o.next).on('click',function(){
         		clearTimeout(timer);
         		if(canMove()){
         			jump('+');
         		}
         		return false;
         	});
         }
	});
};
//参数设置
$.fn.slide.options = {
	loopBody: '',					//焦点图的主体（selector）
    curClass: 'current',			//焦点图当前选中的样式
    speed: 500,						//焦点图切换的速度（单位：ms）
    gap: 5000,						//焦点图切换的间隔（单位：ms）
    next: '',						//下一张焦点图按钮，可选（selector）	
    prev: '',						//上一张焦点图按钮，可选（selector）
    control: {						//焦点图带有下标的切换，可选
    	curClass: 'current',
    	selector: '',
    	child: ''
    },
    moveType: 'slide',				//动画方式：slide为滑动，向左滑动；dissolve为溶解。默认为滑动
    easing: 'easeOutCirc',
    looping: $.noop,				//loop时的回调，可选
    loopEnd: $.noop					//loop结束后的回调，可选
};
})(jQuery,window);