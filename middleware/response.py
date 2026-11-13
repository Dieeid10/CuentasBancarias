def success(message=None, status_code=200):
    return {
        "status": "success",
        "message": message,
        "status_code": status_code
    }

def error(message=None, status_code=500):
    return {
        "status": "error",
        "message": message,
        "status_code": status_code
    }