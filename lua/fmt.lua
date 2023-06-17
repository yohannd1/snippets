local M = {}

local function string2table(str)
    strc = {}
    for i = 1, #str do
        table.insert(strc, string.sub(str, i, i))
    end
    return strc
end

M.fmt = function(format_string, args)
    local context = "base"

    local start_ptr = 1
    local end_ptr = 1

    local schars = string2table(format_string)
    local accumulated_string = ""

    local current_arg_idx = 1

    while true do
        local current_char = schars[end_ptr]

        if current_char == "{" then
            if context == "base" then
                context = "{"
            elseif context == "{" then
                accumulated_string = accumulated_string .. format_string:sub(start_ptr, end_ptr - 2) .. "{"

                start_ptr = end_ptr + 1
                end_ptr = start_ptr

                context = "base"
            elseif context == "}" then
                error("Trailing { at index " .. end_ptr)
            else
                error("Invalid context: " .. context)
            end
        elseif current_char == "}" then
            if context == "base" then
                context = "}"
            elseif context == "}" then
                accumulated_string = accumulated_string .. format_string:sub(start_ptr, end_ptr - 2) .. "}"

                start_ptr = end_ptr + 1
                end_ptr = start_ptr

                context = "base"
            elseif context == "{" then
                accumulated_string = accumulated_string .. format_string:sub(start_ptr, end_ptr - 2)

                local current_arg = args[current_arg_idx]
                if current_arg ~= nil then
                    accumulated_string = accumulated_string .. current_arg
                else
                    error("Missing argument #" .. current_arg_idx .. " (required at the '{}' at #" .. end_ptr - 1 .. ")")
                end
                current_arg_idx = current_arg_idx + 1

                start_ptr = end_ptr + 1
                end_ptr = start_ptr

                context = "base"
            else
                error("Invalid context: " .. context)
            end
        elseif current_char == nil then
            if context == "base" then
                accumulated_string = accumulated_string .. format_string:sub(start_ptr, end_ptr)
                break
            elseif context == "{" then
                error("Trailing {")
            else
                error("Strange context: " .. context)
            end
        end

        end_ptr = end_ptr + 1
    end

    if current_arg_idx ~= #args + 1 then
        error("Trailing arguments")
    end

    return accumulated_string
end

return M
