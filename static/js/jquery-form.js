$.fn.formSubmit = function(){
	$(document).on('submit', 'form', function(event){
		$.ajax({
			type: $(this).attr('method'),
			url: $(this).attr('action'),
			data: $(this).serialize(),
			dataType: 'json',
			context: this,
			success: function(json) {
				if (json.status) {
					if (json.username) {
						$('#no-login').css('display','none');
						$('#is-login .login').text(json.username);
						$('#is-login').css('display','block');
					}
					if (json.url) loadUrl(json.url, 'section>div');
				} else {
					$(this).children('div.err').remove();
					$('<div class="err">'+json.msg+'</div>').prependTo(this);
				}
			}
		});
		event.preventDefault();
	});
}
$(function(){
	$.fn.formSubmit();
});