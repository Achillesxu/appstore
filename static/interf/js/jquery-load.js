$(function(){
	var url;
	if (url = window.location.href.getQueryString('t')) {
		$('section>div').load(url);
	} else {
		$('section>div').load('login/login.html');
	}
	$.loadHtml('[name=to_login]', 'login/login.html', 'section>div', true);
	$.loadHtml('[name=to_register]', 'login/register.html', 'section>div',true);
	$.loadHtml('[name=to_find_pass]', 'login/find_pass.html', 'section>div', true);
	$.loadHtml('[name=to_admin_overview]', 'admin/index.html', 'section>div');
	$.loadHtml('[name=to_admin_review_apps_list]', 'admin/review_apps_list.html', '#admin');
	$.loadHtml('[name=to_admin_ready_apps_list]', 'admin/ready_apps_list.html', '#admin');
	$.loadHtml('[name=to_admin_form_add_app]', 'admin/form_add_app.html', '#admin');
	$.loadHtml('[name=to_admin_review_user_list]', 'admin/review_user_list.html', '#admin');
	$.loadHtml('[name=to_admin_ready_user_list]', 'admin/ready_user_list.html', '#admin');
	$.loadHtml('[name=to_admin_feedback_list]', 'admin/feedback_list.html', '#admin');
	
	$.loadHtml('[name=to_user_index]', 'user/index.html', 'section>div');
	$.loadHtml('[name=to_user_form_add_app]', 'user/form_add_app.html', '#user');
	$.loadHtml('[name=to_user_my_apps]', 'user/my_apps.html', '#user');
	$.loadHtml('[name=to_user_apps]', 'user/apps.html', '#user');
	$.loadHtml('[name=to_user_info]', 'user/info.html', '#user');
	$.loadHtml('[name=to_user_set]', 'user/set_person.html', '#user');
	$.loadHtml('[name=to_user_person_develop]', 'user/person.html', 'section>div');
	$.loadHtml('[name=to_user_corp_develop]', 'user/corp.html', 'section>div');
	$.loadHtml('[name=to_user_set_person]', 'user/set_person.html', '#user');
	$.loadHtml('[name=to_user_set_corp]', 'user/set_corp.html', '#user');
	$.loadHtml('[name=to_user_set_pass]', 'user/set_pass.html', '#user');
});

function loadUrl (url, target) {
	var ifHref = false;
	var param = '';
	if (arguments[2]) {
		if ($.type(arguments[2]) === 'boolean') {
			ifHref = arguments[2];
			if (arguments[3]) param = arguments[3];
		} else param = arguments[2];
	}
	$(target).load(url);
	var json = {};
	if (ifHref) json['t'] = url;
	if (param != '') json[param.split(':')[0]] = param.split(':')[1];
	if (!$.isEmptyObject(json)) window.location.href = window.location.href.newHrefString(json);
}

$.loadHtml = function(id, url, target){
	var ifHref = arguments[3] ? arguments[3] : false;
	
	$(document).on('click', id, function(){
		$(id).siblings('.current').removeClass('current');
		$(id).addClass('current');
		$(target).load(url);
		if (window.location.href.clearHrefString()) window.location.href = window.location.href.clearHrefString();
		if (ifHref) window.location.href = window.location.href.newHrefString({t:url});
		return false;
	});
}