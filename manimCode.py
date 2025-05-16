from manim import *
from utilities import myScale , truncate_decimal
from icons import screenRectanlge

INPUT_COLOR = WHITE
OUTPUT_COLOR = RED
PROCESS_COLOR = BLUE
INTERSECTION_COLOR = YELLOW


class Scene1(MovingCameraScene):
    def construct(self):
        title_text_1 = Text("Symmetry", color=BLUE, stroke_color=BLUE)
        title_text_2 = Text("Transformation", color=BLUE, stroke_color=BLUE)
        title_texts = VGroup(title_text_1, title_text_2).arrange(RIGHT, buff=3).scale(0.585).shift(RIGHT * 0.2)

        recall_text = Text("Recall:", color=YELLOW)
        recall_text = myScale(recall_text, 0.5)
        recall_text.to_corner(UL, 0.267)

        number_plane = NumberPlane(
            x_range=[-10, 10, 1],        # From -10 to 10 with spacing of 1
            y_range=[-6, 6, 1],          # From -6 to 6 with spacing of 1
            x_length = 14,
            y_length = 8,

            background_line_style={
                "stroke_color": BLUE,
                "stroke_width": 1,
            },
            axis_config={
                "include_numbers": True,
                "font_size": 15,         # Small to medium label size
                "line_to_number_buff" : 0.07,
                "stroke_color": WHITE,
            },
            tips=False                   # No arrow tips on axes
        )
        number_plane.set_stroke(opacity=0.35) 
        

        functionTextCanvas = Rectangle(BLACK, 0.5, 2.2 , stroke_opacity = 1, fill_color=BLACK, fill_opacity=1)
        functionText = MathTex(r"f(", r"x", r") = ", r"x", r"^3 - 3", r"x", color=OUTPUT_COLOR)
        functionText[1].set_color(INPUT_COLOR)
        functionText[3].set_color(INPUT_COLOR)
        functionText[5].set_color(INPUT_COLOR)
        functionTextCanvas.next_to(recall_text, DOWN).shift(RIGHT * 0.5 + UP * 0.085)


        number_plane.z_index = -5
        functionTextCanvas.z_index = 0
        functionText.z_index = 1


        def function(x):
            return (x**3) - (3 * x)
        x_value = ValueTracker(-1)

        functionText2 = MathTex(r"f(", r"-1", r")" ,  r"= (", r"-1", r")^3 - 3(", r"-1", r")" , color=OUTPUT_COLOR).scale(0.6).next_to(recall_text , DOWN , 0.75).align_to(recall_text , LEFT).shift(LEFT * 0.2)
        functionText2[1].set_color(INPUT_COLOR)
        functionText2[4].set_color(INPUT_COLOR)
        functionText2[6].set_color(INPUT_COLOR)

        def functionText3_function():
            a = MathTex(r"f(", f"{truncate_decimal(x_value.get_value() , 2)}", r")" , r"=" , f"{truncate_decimal(function(x_value.get_value()) , 2)}" , color=OUTPUT_COLOR).scale(0.6).move_to(functionText2).align_to(functionText2 , LEFT)
            a[1].set_color(INPUT_COLOR)
            return a
        
        functionText3 = always_redraw(functionText3_function)
        functionText3Static = functionText3_function()

        exampleInputDot = always_redraw(lambda: Dot(number_plane.c2p(x_value.get_value() , 0) , color=YELLOW , radius=0.03))

        pointOnCurve = always_redraw(lambda: Dot(number_plane.c2p(x_value.get_value() , function(x_value.get_value())) , radius=0.04 , color=OUTPUT_COLOR))
        
        def changing_curve_function():
            if x_value.get_value() > -1:
                return number_plane.plot(function , [-1 , x_value.get_value()] , stroke_width = 3 , color=OUTPUT_COLOR)
            else:
                return number_plane.plot(function , [x_value.get_value() , -1] , stroke_width = 3 , color=OUTPUT_COLOR)

        changing_curve = always_redraw(changing_curve_function)

        right_curve = number_plane.plot(function , [-1 , 2.5] , stroke_width = 3 , color=OUTPUT_COLOR)

        
        self.wait()

        self.play(Write(title_text_1))
        self.play(Write(title_text_2))

        self.wait()
        self.play(FadeOut(title_texts, run_time=0.25))
        self.play(Write(recall_text))


        self.play(Write(functionText))
        self.play(Create(number_plane) , FadeIn(functionTextCanvas)  , functionText.animate.scale(0.6).next_to(recall_text, DOWN).align_to(recall_text, LEFT))

        self.play(FadeIn(exampleInputDot) , FocusOn(exampleInputDot , run_time = 0.7))
        self.play(Write(functionText2[:3]))
        self.wait(0.3)
        self.play(Write(functionText2[3:]))
        self.play(TransformMatchingTex(functionText2 , functionText3Static))

        self.play(Indicate(functionText3Static[1]) , run_time = 0.7)
        self.play(Indicate(functionText3Static[4]) , run_time = 0.7)

        self.add(functionText3)
        self.play(FadeOut(functionText3Static , run_time = 0.1))

        self.play(GrowFromCenter(pointOnCurve , run_time = 0.3) , FocusOn(number_plane.c2p(-1,2) , run_time = 0.6))
        self.wait(0.2)
        self.add(changing_curve)
        self.play(x_value.animate.set_value(2.5) , run_time = 2 , rate_func = linear)
        self.wait(0.5)
        self.add(right_curve)
        self.play(x_value.animate.set_value(-2.5) , run_time = 2 , rate_func = linear)

        self.play(FadeOut(functionText3 , pointOnCurve , exampleInputDot))

        self.wait(0.5)

        title_texts.shift(DOWN * config.frame_height)
        self.add(screenRectanlge(1).shift(DOWN * config.frame_height))
        self.add(title_texts)
        self.play(self.camera.frame.animate.shift(DOWN * config.frame_height))

        self.wait()


class Scene2(Scene):
    def construct(self):
        title_text_1 = Text("Symmetry", color=BLUE, stroke_color=BLUE)
        title_text_2 = Text("Transformation", color=BLUE, stroke_color=BLUE)
        title_texts = VGroup(title_text_1, title_text_2).arrange(RIGHT, buff=3).scale(0.585).shift(RIGHT * 0.2)

        symmetryDescription = Tex("The property of being " , "unchanged" , " after a transformation." , color=WHITE).scale(0.7)
        symmetryDescription[1].color=RED

        triangle = Triangle(fill_color = RED , fill_opacity = 1 , stroke_width = 0 , stroke_color = RED).shift(DOWN * 0.5)

        line1 = DashedLine(start = [0 , 0.7 , 0] , end = [0 , -1.3 , 0] , stroke_width = 2)


        self.add(title_texts)
        self.play(title_text_1.animate.move_to(ORIGIN).to_edge(UP) , FadeOut(title_text_2))
        self.play(Write(symmetryDescription[:2]))
        self.play(Write(symmetryDescription[2:]))

        self.play(symmetryDescription.animate.scale(0.8).next_to(title_text_1 , DOWN))
        self.play(DrawBorderThenFill(triangle) , run_time = 1)

        self.play(Create(line1) , run_time = 0.5)
        self.play(triangle.animate.scale([-1 , 1 , 1]) , run_time = 0.6)
        self.wait(0.5)
        self.play(triangle.animate.scale([-1 , 1 , 1]) , run_time = 0.6)
        self.play(Circumscribe(symmetryDescription[1] ,shape=Rectangle , time_width=3 , stroke_width=1 , buff=0.05))
        
        #Rotate the line

        self.wait()