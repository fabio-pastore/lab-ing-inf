import time

def throttle(func, limit):
    """
    Makes a new function that is called at most 1 time every `limit` seconds
    if the function is called again too soon, just give the same result as the last allowed call.
    """
    last_called = 0
    # we should probably save the last return result too! (the function originally didn't do this)
    last_result = None
    
    def throttled(*args, **kwargs):
        nonlocal last_called, last_result
        current_time = time.time()
        
        if current_time - last_called >= limit:
            result = func(*args, **kwargs)
            last_called = current_time
            # save obtained result into last_result
            last_result = result
            return result

        return last_result # if throttled, return last available result, not "None".
    
    return throttled

def expensive_operation(x):
    print(f"Executing expensive operation with {x}")
    return x * 2
