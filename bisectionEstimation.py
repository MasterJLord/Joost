import math

# TODO : figure out if lambdas would be relevant
def rootEstimation(expression, startPoints : tuple[int, int], tolerance : float):
    startValue0 = expression(startPoints[0])
    startValue1 = expression(startPoints[1])
    if startValue0 == 0:
        return startPoints[0]
    elif startValue1 == 0:
        return startPoints[1]
    if startValue0 > 0:
        if startValue1 > 0:
            raise ValueError("Starting points did not surround a zero of the function")
        negativePoint = startPoints[1]
        # negativeValue = startValue1
        positivePoint = startPoints[0]
        # positiveValue = startValue0
    else:
        if startValue1 < 0:
            raise ValueError("Starting points did not surround a zero of the function")
        negativePoint = startPoints[0]
        # negativeValue = startValue0
        positivePoint = startPoints[1]
        # positiveValue = startValue1
    while True:
        newPoint = (negativePoint + positivePoint) / 2
        # newPoint = negativePoint - negativeValue * ((positivePoint - negativePoint) / (positiveValue - negativeValue))
        print(newPoint)
        if abs(positivePoint - negativePoint) < tolerance * 2:
            return newPoint
        newValue = expression(newPoint)
        if newValue == 0:
            return newPoint
        if newValue > 0:
            positivePoint = newPoint
            # positiveValue = newValue
        else:
            negativePoint = newPoint
            # negativeValue = newValue