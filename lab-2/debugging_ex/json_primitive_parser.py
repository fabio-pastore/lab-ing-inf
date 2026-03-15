def parse_json_primitive(json_str, start_idx=0):
    """Parse a JSON primitive (number, string, boolean, null) from a string.
    Numbers can only be integers for simplicity.
    Retuns the end index so that parsing can continue from there."""
    i = start_idx
    while i < len(json_str) and json_str[i].isspace():
        i += 1
    
    if i >= len(json_str):
        return None, i
    
    if json_str[i] == '"':
        i += 1
        value_start = i
        while i < len(json_str) and json_str[i] != '"':
            i += 1
                
        value = json_str[value_start:i]
        return value, i + 1
    
    if json_str[i].isdigit():
        value_start = i
        while i < len(json_str):
            if json_str[i].isdigit():
                i += 1
            else:
                raise ValueError("Invalid number")
        
        value = json_str[value_start:i]
        try:
            return int(value), i
        except ValueError:
            raise ValueError(f"Invalid number: {value}")
    
    if json_str[i:i+4] == "true":
        return True, i + 4
    if json_str[i:i+6] == "false":
        return False, i + 5 ## this was i + 6
    if json_str[i:i+4] == "null":
        return None, i + 4
    
    raise ValueError(f"Invalid JSON primitive at position {i}")
