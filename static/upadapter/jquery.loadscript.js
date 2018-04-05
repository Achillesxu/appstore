$.loadScript = function(url,type, callback){
	var head = document.getElementsByTagName('head')[0];
    var exists = false;
    
    var head_script = head.children;
    for(var i = 0;i<head_script.length;i++){
	    var js_script_name = '';
	    if(head_script[i].nodeName.toLowerCase() == 'script'){
	    	
	    	js_script_name =  head_script[i].src;
	    	if(js_script_name&&url.indexOf(js_script_name.split('/').pop()) !== -1){
	    		 	
	    		exists = true;
	    		break; 					 	
	    	}
	    		     	
		}else if(head_script[i].nodeName.toLowerCase() == 'link'){
			
			js_script_name =  head_script[i].href;
	    	if(js_script_name&&url.indexOf(js_script_name.split('/').pop()) !== -1){
	    		 	
	    		exists = true;
	    		break; 					 	
	    	}
			
		}

    }
    if(!exists){

    	var callbackFunc = function(){
    		if(type=='js'){
    			var script = document.createElement('script');
    		}
    		else if(type=='css'){
    			var script  = document.createElement('link');
    		}
    		head.appendChild(script);
    		
    		var canListenEvent = false; //是否可以通过监听事件来进行回调
			if('onload' in script){
				canListenEvent = true;
				script.onload = function(){
	    			callback&&callback();
		    	};
			}
			else {
				if('onreadystatechange' in script){
					canListenEvent = true;
					script.onreadystatechange = function(){
						if(!this.readyState || this.readyState==='loaded' || this.readyState==='complete'){
			    			callback&&callback();
			        	}
			        }
				}
			}
			//如果可以通过监听事件的方式回调，则直接赋值地址，否则通过ajax方式获取
		    if(canListenEvent){
		    	if(type=='js'){
		    		script.src = url;
		    	}
		    	else if(type=='css'){
		    		script.rel = "stylesheet";
					script.type = "text/css";
					script.href = url;
		    	}
		    }
		    else{
		    	$(script).remove();
				$.ajax({
					url :url,
					success:function(data){
						if(type=='js'){
							$(head).append('<script type="text/javascript">' + data + '</script>');	
						}
						else if(type=='css'){
							$(head).append('<style type="text/css">' + data + '</style>');	
						}
						
			    		callback&&callback();
					}
				});
			}
    	}
    	callbackFunc();
    	
    }
    else{
    	callback();
    }
	
}