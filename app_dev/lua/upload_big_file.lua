--
-- Created by IntelliJ IDEA.
-- User: weis
-- Date: 14-7-25
-- Time: 下午5:17
-- To change this template use File | Settings | File Templates.
--
local upload = require "resty.upload"
local cjson = require "cjson"
local resty_md5 = require "resty.md5"
local str = require "resty.string"

ngx.header.content_type = "application/json;charset=UTF-8"

local osfilepath = "/Users/achilles_xushy/PycharmProjects/config_and_log/ssdb/attachment/static/upload/bigfile_tmp/"
local i
local file_md5
local file_size

local chunk_size = 4096 -- should be set to 4096 or 8192
local now_str = tostring(ngx.now()*1000)

local filename
local file
local file_path

function get_filename(res)
    local filename = ngx.re.match(res,'(.+)filename="(.+)"(.*)')
    if filename then
        return filename[2]
    end
end

function getextension(filename)
    return filename:match(".+%.(%w+)$")
end

local arg_act = ngx.var['arg_act']
local arg_code = ngx.var['arg_code']
local arg_next = ngx.var['arg_next']
local arg_time = ngx.var['arg_time']

if arg_code == nil or arg_next == nil or arg_time == nil  or arg_act == nil then
    ngx.say(cjson.encode({status=400, msg="缺少合法参数"}))
    return
end

local form, err = upload:new(chunk_size)
if not form then
    ngx.log(ngx.ERR, "failed to new upload: ", err)
    ngx.say(cjson.encode({status=500, msg=err .. " here "}))
    ngx.exit(500)
end

form:set_timeout(2000000) -- 10000/10 sec

local md5 = resty_md5:new()

i = 0
file_size = 0
while true do
    local typ, res, err = form:read()
    if not typ then
        ngx.say(cjson.encode({status=400, msg="读取表单失败： " .. err}))
        return
    end

    if typ == "header" then
        if res[1] ~= "Content-Type" then
            filename = get_filename(res[2])
            if filename then
                i=i+1
                file_path = osfilepath .. arg_time .. "." .. getextension(filename)
                file = io.open(file_path, "w+")
                if not file then
                    ngx.say(cjson.encode({status=400, msg="读取文件失败"}))
                    return
                end
            end
        end
    elseif typ == "body" then
        if file then
            file:write(res)
            md5:update(res)
            file_size = file_size + string.len(res)
        end
    elseif typ == "part_end" then
        if file then
            file:close()
            file = nil
            local digest = md5:final()
            file_md5 = str.to_hex(digest)
        end
    elseif typ == "eof" then
        break
    end
end

if i > 0 then
    local res
    res = ngx.location.capture(arg_next, { args = { act=arg_act, time=arg_time, code=arg_code, file_md5=file_md5, file_path=file_path, file_size=file_size} })
    if res.status == 200 then
        ngx.say(res.body)
    else
        ngx.say(cjson.encode({status=400, msg="服务器内部网络出错，请稍后再试 " .. tostring(res.status), code=res.status}))
    end
else
    ngx.say(cjson.encode({status=400, msg="至少上传一个文件"}))
end


