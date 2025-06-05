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


def TransformMatchingFromCopy(source, target, **kwargs):
    temp = source.copy()
    return TransformMatchingShapes(temp, target, **kwargs)


class FadeInAndOutDirectional(Succession):
    def __init__(self, mobject, shift , run_time = 0.5 , **kwargs):
        super().__init__(
            FadeIn(mobject, shift=shift * 0.5, rate_func=rush_into , run_time = run_time),
            FadeOut(mobject, shift=shift * 0.5, rate_func=rush_from , run_time = run_time),
            **kwargs
        )

class FadeOutAll(AnimationGroup):
    def __init__(self, scene: Scene, **kwargs):
        if not isinstance(scene, Scene):
            raise TypeError("FadeOutAll must be given a Scene instance.")
        animations = [FadeOut(mob) for mob in scene.mobjects]
        super().__init__(*animations, **kwargs)


class FadeOutAllExcept(AnimationGroup):
    def __init__(self, scene: Scene, *exceptions: Mobject, **kwargs):
        if not isinstance(scene, Scene):
            raise TypeError("First argument to FadeOutAllExcept must be a Scene.")
        exceptions_set = set(exceptions)
        animations = [
            FadeOut(mob) for mob in scene.mobjects if mob not in exceptions_set
        ]
        super().__init__(*animations, **kwargs)


class Slider(VMobject):
    def __init__(
        self,
        x_min=-3,
        x_max=3,
        x=0,
        length=6,
        dot_config=None,
        line_config=None,
        **kwargs
    ):
        super().__init__(**kwargs)

        self.x_min = x_min
        self.x_max = x_max
        self.length = length
        self.x = x

        dot_config = dot_config or {}
        line_config = line_config or {}

        # Create number line with forwarded config
        self.number_line = NumberLine(
            x_range=[x_min, x_max],
            length=length,
            **line_config
        )

        # Create dot with forwarded config
        self.dot = Dot().copy().set(**dot_config)
        self.set_value(x)  # Initializes dot position

        self.add(self.number_line, self.dot)

    def set_value(self, x):
        x = np.clip(x, self.x_min, self.x_max)
        self.x = x
        alpha = (x - self.x_min) / (self.x_max - self.x_min)
        position = interpolate(
            self.number_line.get_start(), self.number_line.get_end(), alpha
        )
        self.dot.move_to(position)
        return self

    def get_value(self):
        return self.x

    def __getattr__(self, attr):
        if attr == "set_value":
            return lambda x: UpdateFromFunc(self, lambda m: m.set_value(x))
        return super().__getattr__(attr)
