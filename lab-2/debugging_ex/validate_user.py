def validate_user(user, this_user_validation_problems):

    if this_user_validation_problems is None:
        this_user_validation_problems = [] # define mutable argument inside the function, else we are using the same list over and over again! 

    if user.get("name") is None:
        this_user_validation_problems.append("Name must be present") 

    if user.get("age") is None:
        this_user_validation_problems.append("Age must be present") 
        return this_user_validation_problems # added early return to avoid TypeError in later check

    if user["age"] < 18: 
        this_user_validation_problems.append("Age must be at least 18") 

    return this_user_validation_problems



