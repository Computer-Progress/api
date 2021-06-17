def parseInt(value):
    try:
        return int(float(value))
    except Exception:
        return None


def parseFloat(value):
    try:
        return float(value)
    except Exception:
        return None
