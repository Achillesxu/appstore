$(function(){
	var url;
	if (url = window.location.href.getQueryString('t')) {
		$('section>div').load(url);
	} else {
		$('section>div').load('/user/login');
	}
	$.loadHtml('[name=to_login]', '/user/login', 'section>div', true);
	$.loadHtml('[name=to_register]', '/user/register', 'section>div',true);
	$.loadHtml('[name=to_find_pass]', '/user/find_password', 'section>div', true);
	$.loadHtml('[name=to_admin_overview]', '/admin/home', 'section>div');
	$.loadHtml('[name=to_admin_review_apps_list]', '/admin/review_apps_list', '#admin');
	$.loadHtml('[name=to_admin_ready_apps_list]', '/admin/ready_apps_list', '#admin');
	$.loadHtml('[name=to_admin_form_add_app]', '/admin/add_app', '#admin');
	$.loadHtml('[name=to_admin_review_user_list]', '/admin/review_user_list', '#admin');
	$.loadHtml('[name=to_admin_ready_user_list]', '/admin/ready_user_list', '#admin');
	$.loadHtml('[name=to_admin_feedback_list]', '/admin/feedback_list', '#admin');
	
	$.loadHtml('[name=to_user_index]', '/user/home', 'section>div');
	$.loadHtml('[name=to_user_form_add_app]', '/user/add_app', '#user');
	$.loadHtml('[name=to_user_my_apps]', '/user/my_apps', '#user');
	$.loadHtml('[name=to_user_apps]', '/user/apps', '#user');
	$.loadHtml('[name=to_user_info]', '/user/info', '#user');
	$.loadHtml('[name=to_user_set]', '/user/set_person', '#user');
	$.loadHtml('[name=to_user_person_develop]', '/user/person', 'section>div');
	$.loadHtml('[name=to_user_corp_develop]', '/user/corp', 'section>div');
	$.loadHtml('[name=to_user_set_person]', '/user/set_person', '#user');
	$.loadHtml('[name=to_user_set_corp]', '/user/set_corp', '#user');
	$.loadHtml('[name=to_user_set_pass]', '/user/set_pass', '#user');
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