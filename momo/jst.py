

def get_converter(type: type) -> str:
    return {
        float: 'Number',
        int: 'Number'
    }.get(type, type.__name__)
