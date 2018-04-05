local res = ngx.location.capture("/upload/apk")
if res.status == 200 then
    ngx.say(res.body)
else
    ngx.say("服务器出错")
    ngx.say(res.status)
end