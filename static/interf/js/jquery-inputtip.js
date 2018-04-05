/**
+------------------------------------------------------------------------------
* input提示插件
* 参数
* @input 入参
*     json对象
*     @ tip_val    input表单提示默认值
*     @ tip        默认提示信息样式名class
*     @ no_tip     在指定的input执行click时替换的样式名class
+------------------------------------------------------------------------------
* 使用方法:
* $("#xxx").inputTip();
* @ #xxx 为需要提示的input的id
+------------------------------------------------------------------------------
* IE兼容性处理
* 1. 29行，不用clone而用转文本再替换方式
* 2. 29行，文本替换的两种方式，第２种供ie使用
* 3. 37行，两次focus()操作，ie才能聚焦
**/
$.fn.inputTip = function(G){
	var D;
	D = {
		tip_val:"用户名",//表单默认值
		tip:"tip",       //默认提示信息样式名class
		no_tip:"tip_no"  //在指定的input执行click时替换的样式名class
	};
	$.extend(D,G);
	D.jq_old = $(this).clone();
	D.jq_new = $($(this).prop('outerHTML').replace('type="password"', 'type="text"').replace('type=password', 'type=text'));
	$(this).replaceWith(D.jq_new);
	D.jq_new.val(D.tip_val).addClass(D.tip);
	D.jq_old.addClass(D.no_tip);
	D.jq_new.focus(function(){
		if ($(this).val()==D.tip_val) {
			D.jq_new = $(this).clone(true);
			$(this).replaceWith(D.jq_old);
			D.jq_old.focus().focus();
		}
	});
	D.jq_old.blur(function(){
		if ($(this).val()=="") {
			D.jq_old = $(this).clone(true);
			$(this).replaceWith(D.jq_new);
			$(D.jq_new).val(D.tip_val);
		}
	});
}