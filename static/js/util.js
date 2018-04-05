function copyToClipboard(txt) {
	if(window.clipboardData) {
		window.clipboardData.clearData();
		window.clipboardData.setData("Text", txt);
		alert("复制成功");
	} else if(navigator.userAgent.indexOf("Opera") != -1) {
		window.location = txt;
	} else if (window.netscape) {
		try {
			netscape.security.PrivilegeManager.enablePrivilege("UniversalXPConnect");
		} catch (e) {
			alert("被浏览器拒绝！\n请在浏览器地址栏输入'about:config'并回车\n然后将'signed.applets.codebase_principal_support'设置为'true'");
		}
		var clip = Components.classes['@mozilla.org/widget/clipboard;1'].createInstance(Components.interfaces.nsIClipboard);
		if (!clip) return;
		var trans = Components.classes['@mozilla.org/widget/transferable;1'].createInstance(Components.interfaces.nsITransferable);
		if (!trans) return;
		trans.addDataFlavor('text/unicode');
		var str = new Object();
		var len = new Object();
		var str = Components.classes["@mozilla.org/supports-string;1"].createInstance(Components.interfaces.nsISupportsString);
		var copytext = txt;
		str.data = copytext;
		trans.setTransferData("text/unicode",str,copytext.length*2);
		var clipid = Components.interfaces.nsIClipboard;
		if (!clip) return false;
		clip.setData(trans,null,clipid.kGlobalClipboard);
		alert("复制成功");
	}
}

String.prototype.getQueryString = function(target) {
	var reg = new RegExp("(^|&|\\#)" + target + "=([^&]*)(&|$)"), r;
	if (r = this.match(reg))
		return unescape(r[2]);
	return null;
};

String.prototype.newHrefString = function(obj) {
	var a = document.createElement('a');
	a.href = this;
	var q = a.hash, str = '';
	var ps = (function () {
				var r = {}, seg = q.replace(/^\#/, '').split('&'), l = seg.length, s;
				for (var i=0; i<l; i++) {
					if (!seg[i]) continue;
					s = seg[i].split('=');
					r[s[0]] = s[1];
				}
				return r;
			})();
	$.extend(ps,obj);
	for (var p in ps) {
        str += (p + '=' + ps[p] + '&');
    }
    if (q) return a.href.replace(q, '#'+str.replace(/&$/, ''));
    else return a.href.replace('#','')+'#'+str.replace(/&$/, '');
}

String.prototype.clearHrefString = function() {
	var a = document.createElement('a');
	a.href = this;
    if (a.hash != '') return a.href.replace(a.hash, '#');
    else return false;
}

String.prototype.len = function() {
    return this.replace(/[^\x00-\xff]/g, "xx").length;
}