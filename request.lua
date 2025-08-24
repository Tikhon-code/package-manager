f = ''
function load(for_file, file)
    local https = require('ssl.https')
    local body, code = https.request("https://raw.githubusercontent.com/Tikhon-code/package-manager/refs/heads/main/repository/" .. for_file .. file)

    directory = 'files/' .. file
    if directory ~= 'files/' then
        f = assert(io.open(directory, 'wb'))
        f:write(body)
        f:close()
    end
end

load(arg[1], arg[2])