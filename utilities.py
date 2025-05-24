from manim import *

def myScale(mobject, factor):
    """Scales both the mobject and its stroke width. Works for individual objects and groups."""
    mobject.scale(factor)  

    if isinstance(mobject, VGroup):
        for submob in mobject:
            if hasattr(submob, "set_stroke"):
                submob.set_stroke(width=submob.stroke_width * factor)

    elif hasattr(mobject, "set_stroke"):
        mobject.set_stroke(width=mobject.stroke_width * factor)
    
    return mobject

def truncate_decimal(num, digits):
    s = str(num)
    if '.' in s:
        int_part, dec_part = s.split('.')
        if len(dec_part) <= digits:
            cleaned = s.rstrip('0').rstrip('.')
        else:
            truncated = '.'.join([int_part, dec_part[:digits]])
            cleaned = truncated.rstrip('0').rstrip('.')
        return int(cleaned) if '.' not in cleaned else float(cleaned)
    return int(num)

from manim import *

def TransformMatchingFromCopy(source, target, **kwargs):
    temp = source.copy()
    return TransformMatchingShapes(temp, target, **kwargs)



class FadeInAndOutDirectional(Succession):
    def __init__(self, mobject, shift , **kwargs):
        super().__init__(
            FadeIn(mobject, shift=shift, rate_func=rush_into),
            FadeOut(mobject, shift=shift, rate_func=rush_from),
            **kwargs
        )

