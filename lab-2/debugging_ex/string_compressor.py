def compress_string(s):
    if not s:
        return ""
    
    result = []
    count = 1
    current_char = s[0]
    
    for i in range(1, len(s)):
        if s[i] == current_char: # used to be s[i] is current_char, which would work fine, but we mean to compare the value of the chars not their position in memory (the only reason why that
            # check works is probably thanks to optimization, since creating a new obj for each char would introduce great memory overhead)
            count += 1
        else:
            if count > 1:
                result.append(current_char + str(count))
            else:
                result.append(current_char)
            
            current_char = s[i]
            count = 1
    
    if count > 1:
        result.append(current_char + str(count))
    else:
        result.append(current_char)
    
    compressed = "".join(result)
    return compressed
