--
-- Created by IntelliJ IDEA.
-- User: weis
-- Date: 15-8-25
-- Time: 下午4:02
-- To change this template use File | Settings | File Templates.
--
local upload = require "resty.upload"
local cjson = require "cjson"
local resty_md5 = require "resty.md5"
local str = require "resty.string"

ngx.header.content_type = "application/json;charset=UTF-8"

local osfilepath = "/Users/achilles_xushy/PycharmProjects/config_and_log/ssdb/attachment/static/upload/"
local i
local file_md5
local file_size
local cur_uri = ngx.var.uri -- /user/(upload/img|v5/upload/file)

local chunk_size = 4096 -- should be set to 4096 or 8192
local now_str = tostring(ngx.now()*1000)
local ym_str = tostring(os.date("%Y%m"))

local form_dict
local form_key
local form_value

local filename
local file
local file_path
local file_path_new

local act
local actdir
local file_url

if cur_uri == '/user/upload/img' then
    actdir = 'store_img'
elseif cur_uri == '/user/v5/upload/file' then
    actdir = 'store_img_v5'
end

function get_filename(res)
    local filename = ngx.re.match(res,'(.+)filename="(.+)"(.*)')
    if filename then
        return filename[2]
    end
end

function get_keyname(res)
    local filename = ngx.re.match(res,'(.+)name="(.+)"(.*)')
    if filename then
        return filename[2]
    end
end

function getextension(filename)
    return filename:match(".+%.(%w+)$")
end

function checkormkdir(path)
    local f = io.open(path, "r")
    if f == nil then
        os.execute( "mkdir -p " .. path)
        --ngx.log(ngx.ERR, 'create new dir:', path)
        return
    end
    -- local ok, err, code = f:read(1)
    f:close()
    ---if code == 21 is dir
end

form_dict = {}

-- 处理上传文件
local form, err = upload:new(chunk_size)
if not form then
    ngx.log(ngx.ERR, "failed to new upload: ", err)
    ngx.say(cjson.encode({status=500, msg=err .. " here "}))
    ngx.exit(200)
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

    --ngx.say("read: ", cjson.encode({typ, res}))

    if typ == "header" then
        if res[1] ~= "Content-Type" then
            form_key = get_keyname(res[2])
            if form_key then
                form_value = {""}
            end

            filename = get_filename(res[2])
            if filename then
                i=i+1
                -- file_path = osfilepath .. now_str .. ".png"
                checkormkdir(osfilepath .. actdir .. '/' .. ym_str .. '/')
                file_path = osfilepath .. actdir .. '/' .. ym_str .. '/' .. now_str .. ".png"
                file = io.open(file_path, "w+")
                if not file then
                    ngx.say(cjson.encode({status=400, msg="读取文件失败" .. file_path}))
                    return
                end
            end
        end
    elseif typ == "body" then
        if file then
            file:write(res)
            md5:update(res)
            file_size = file_size + string.len(res)
        else
            if form_key then
                table.insert(form_value, res)
            end
        end
    elseif typ == "part_end" then
        if form_key then
           form_dict[form_key] = table.concat(form_value, "")
            if form_key == 'act' then
                actdir = form_dict[form_key] .. '_tmp'
            end
        end

        if file then
            file:close()
            file = nil
            local digest = md5:final()
            file_md5 = str.to_hex(digest)
            -- rename file
            -- file_path_new = osfilepath .. file_md5 .. ".png"
            file_url = 'static/upload/' .. actdir .. '/' .. ym_str .. '/' .. file_md5 .. '.png'
            file_path_new = osfilepath .. actdir .. '/' .. ym_str .. '/' .. file_md5 .. ".png"
            os.rename (file_path, file_path_new)
        end
    elseif typ == "eof" then
        break
    end
end

local notused

--for key, val in pairs(form_dict) do
--    ngx.log(ngx.ERR, key, ": ", val)
--end

if i > 0 then

    local api_url
    act = form_dict['act']
    if act == 'icon' or act == 'cover' or act == 'capture' then
        -- dev
        -- http://dev.7po.com/upload/imgfile
        api_url = '/upload/imgfile' -- ngx.location.capture 仅支持相对路径
    else
        -- store
        -- 直接返回
        if cur_uri == '/user/upload/img' then
            ngx.say(cjson.encode({status=200, msg="ok", url='/' .. file_url}))
            ngx.exit(200)
        elseif cur_uri == '/user/v5/upload/file' then
            ngx.say(cjson.encode({status=200, msg="ok", file_url='/' .. file_url, v1=form_dict['v1']}))
            ngx.exit(200)
        end
        api_url = '/upload/imgfile' -- 可不要
        -- ngx.log(ngx.ERR, 'cur_uri', cur_uri)
    end

    local res
    res = ngx.location.capture(api_url, { args = { act=form_dict['act'], time=form_dict['time'], secure_email=form_dict['secure_email'], file_url=file_url} })
    if res.status == 200 then
        ngx.say(res.body)
    else
        ngx.say(cjson.encode({status=400, msg="服务器内部网络出错，请稍后再试 " .. tostring(res.status), code=res.status}))
    end
else
    ngx.say(cjson.encode({status=400, msg="至少上传一个文件"}))
end

ngx.exit(200)
