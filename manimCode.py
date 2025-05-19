from manim import *
from utilities import myScale , truncate_decimal
from icons import screenRectanlge , CheckMark
from math import sin , cos

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


class Scene2(MovingCameraScene):
    def construct(self):
        title_text_1 = Text("Symmetry", color=BLUE, stroke_color=BLUE)
        title_text_2 = Text("Transformation", color=BLUE, stroke_color=BLUE)
        title_texts = VGroup(title_text_1, title_text_2).arrange(RIGHT, buff=3).scale(0.585).shift(RIGHT * 0.2)

        symmetryDescription = Tex("The property of being " , "unchanged" , " after a transformation." , color=WHITE).scale(0.7)
        symmetryDescription[1].color=RED

        triangle = Triangle(fill_color = RED , fill_opacity = 1 , stroke_width = 0 , stroke_color = RED).shift(DOWN * 0.5)

        triangleCenter = triangle.get_center()[1]
        symmetryLine = DashedLine(start = [0 , triangleCenter+1 , 0] , end = [0 , triangleCenter-1 , 0] , stroke_width = 2)

        rotationSymbol1 = CurvedArrow(start_point=[0.4 , 0.65 , 0] , end_point=[-0.4 , 0.65 , 0] , tip_length = 0.1 , stroke_width = 2)
        rotationSymbol2 = CurvedArrow(end_point=[0.4 , 0.65 , 0] , start_point=[-0.4 , 0.65 , 0] , tip_length = 0.1 , stroke_width = 2).shift(DOWN * 2)
        rotationSymbolLabel = MathTex(r"120^{\circ}").scale(0.4).next_to(rotationSymbol2 , DOWN , buff=0.1)

        upperGroup = VGroup()
        lowerGroup = VGroup()

        for i in range(3):
            miniTriangle = Triangle(fill_color = RED , fill_opacity = 1 , stroke_width = 0 , stroke_color = RED).shift(DOWN * 0.2)
            miniLine = DashedLine(start = miniTriangle.get_center()+[0,1,0] , end = miniTriangle.get_center()+[0,-1,0] , stroke_width = 2).rotate(i * (TAU/3) , about_point=miniTriangle.get_center_of_mass())
            miniBox = Square(side_length=3 , color=YELLOW , stroke_width = 3)
            group = VGroup(miniBox , miniTriangle , miniLine)
            group = myScale(group , 0.6)
            upperGroup.add(group)
        
        for i in range(3):
            miniTriangle = Triangle(fill_color = RED , fill_opacity = 1 , stroke_width = 0 , stroke_color = RED).shift(DOWN * 0.2)
            
            miniRotationSymbol1 = CurvedArrow(start_point=[0.4 , 0.65 , 0] , end_point=[-0.4 , 0.65 , 0] , tip_length = 0.1 , stroke_width = 2).shift(UP * 0.2)
            miniRotationSymbol2 = CurvedArrow(end_point=[0.4 , 0.65 , 0] , start_point=[-0.4 , 0.65 , 0] , tip_length = 0.1 , stroke_width = 2).shift(DOWN * 1.6)
            miniRotationSymbolLabel = MathTex(f"{i * 120}" , r"^{\circ}").scale(0.4).next_to(miniRotationSymbol2 , DOWN , buff=0.1)
            
            miniBox = Square(side_length=3 , color=YELLOW , stroke_width = 3)
            group = VGroup(miniBox , miniTriangle , miniRotationSymbol1 , miniRotationSymbol2 , miniRotationSymbolLabel)
            group = myScale(group , 0.6)
            lowerGroup.add(group)

        upperGroup.arrange(RIGHT , buff=1)
        lowerGroup.arrange(RIGHT , buff=1)
        allGroups = VGroup(upperGroup , lowerGroup).arrange(DOWN , buff=1).shift(DOWN * 0.5)


        self.add(title_texts)
        self.play(title_text_1.animate.move_to(ORIGIN).to_edge(UP) , FadeOut(title_text_2))
        self.play(Write(symmetryDescription[:2]))
        self.play(Write(symmetryDescription[2:]))

        self.play(symmetryDescription.animate.scale(0.8).next_to(title_text_1 , DOWN))
        self.play(DrawBorderThenFill(triangle) , run_time = 1)

        self.play(Create(symmetryLine) , run_time = 0.5)
        self.play(triangle.animate.scale([-1 , 1 , 1]) , run_time = 0.6)
        self.wait(0.5)
        self.play(triangle.animate.scale([-1 , 1 , 1]) , run_time = 0.6)
        self.play(Circumscribe(symmetryDescription[1] ,shape=Rectangle , time_width=3 , stroke_width=1 , buff=0.05))
        
        self.play(Rotate(symmetryLine , (TAU/3) , about_point=[triangle.get_center_of_mass()]))
        self.play(Rotate(triangle , PI , [cos(PI/6) , sin(PI/6) , 0] , triangle.get_center_of_mass()))
        self.play(Rotate(symmetryLine , (TAU/3) , about_point=[triangle.get_center_of_mass()]))
        self.play(Rotate(triangle , PI , [cos(-PI/6) , sin(-PI/6) , 0] , triangle.get_center_of_mass()))
        self.play(Uncreate(symmetryLine) , run_time=0.3)
        self.play(Rotate(triangle , TAU/3 , about_point=triangle.get_center_of_mass()) , FadeIn(rotationSymbol1 , rotationSymbol2 , rotationSymbolLabel))

        animations = [FadeIn(mobj) for mobj in upperGroup] 
        animations += [FadeIn(lowerGroup[0]), FadeIn(lowerGroup[2])] 

        self.play(ReplacementTransform(triangle , lowerGroup[1][1]) , ReplacementTransform(rotationSymbol1 , lowerGroup[1][2]) , ReplacementTransform(rotationSymbol2 , lowerGroup[1][3]) , TransformMatchingTex(rotationSymbolLabel , lowerGroup[1][4]) , FadeIn(lowerGroup[1][0]))
        self.play(AnimationGroup(*animations , lag_ratio=0.25))

        for i in range(5):
            self.play(
                upperGroup[0][1].animate.scale([-1,1,1]),
                Rotate(upperGroup[1][1] , PI , [cos(PI/6) , sin(PI/6) , 0] , upperGroup[1][1].get_center_of_mass()),
                Rotate(upperGroup[2][1] , PI , [cos(-PI/6) , sin(-PI/6) , 0] , upperGroup[2][1].get_center_of_mass()),
                Rotate(lowerGroup[1][1] , TAU/3 , about_point=lowerGroup[1][1].get_center_of_mass()),
                Rotate(lowerGroup[2][1] , (2*TAU)/3 , about_point=lowerGroup[2][1].get_center_of_mass())
            )
            self.wait(0.5)
        

        functionText = MathTex(r"f(" , r"x" , r") = " , r"x" , r"^3 - 3" , r"x" , color=OUTPUT_COLOR).scale(0.7).to_corner(UL)
        functionText[1].set_color(INPUT_COLOR)
        functionText[3].set_color(INPUT_COLOR)
        functionText[5].set_color(INPUT_COLOR)

        number_plane = NumberPlane(
            x_range=[-10, 10, 1],        
            y_range=[-6, 6, 1],        
            x_length = config.frame_width,
            y_length = config.frame_height,

            background_line_style={
                "stroke_color": BLUE,
                "stroke_width": 1,
            },
            axis_config={
                "include_numbers": True,
                "font_size": 15,
                "line_to_number_buff" : 0.07,
                "stroke_color": WHITE,
            },
            tips=False
        )
        number_plane.set_stroke(opacity=0.35) 
        curve = number_plane.plot(lambda x : (x**3) - (3 * x) , [-2.3553 , 2.3553] , stroke_width = 3 , color=OUTPUT_COLOR)

        number_plane.shift(UP * config.frame_height)
        curve.shift(UP * config.frame_height)
        ghostCurve = curve.copy()
        ghostCurve.set_stroke(opacity=0.3)
        functionText.shift(UP * config.frame_height)

        self.add(number_plane , ghostCurve , curve , functionText)

        self.play(self.camera.frame.animate.shift(UP * config.frame_height))


        self.wait()
    
class Scene3(Scene):
    def construct(self):
        functionText = MathTex(r"f(" , r"x" , r") = " , r"x" , r"^3 - 3" , r"x" , color=OUTPUT_COLOR).scale(0.7).to_corner(UL)
        functionText[1].set_color(INPUT_COLOR)
        functionText[3].set_color(INPUT_COLOR)
        functionText[5].set_color(INPUT_COLOR)

        number_plane = NumberPlane(
            x_range=[-10, 10, 1],        
            y_range=[-6, 6, 1],        
            x_length = config.frame_width,
            y_length = config.frame_height,

            background_line_style={
                "stroke_color": BLUE,
                "stroke_width": 1,
            },
            axis_config={
                "include_numbers": True,
                "font_size": 15,
                "line_to_number_buff" : 0.07,
                "stroke_color": WHITE,
            },
            tips=False
        )
        number_plane.set_stroke(opacity=0.35) 
        curve = number_plane.plot(lambda x : (x**3) - (3 * x) , [-10 , 10] , stroke_width = 3 , color=OUTPUT_COLOR)
        ghostCurve = curve.copy()
        ghostCurve.set_stroke(opacity=0.3)

        screen_rectangle = screenRectanlge(0.75)

        definition = Tex(r"A function is an " ,  r"odd" , r" function" , r" if the graph of that function" , r"\\ is " , r"symmetric" , r" under a " , r"$180^{\circ}$ rotation about the origin.", tex_environment="center")
        definition[1].set_color(RED)
        definition[5].set_color(RED)

        wordEven = Tex("even").set_color(RED)
        wordEven.move_to(definition[1]).align_to(definition[1] , DOWN)

        replacement2 = Tex("reflection about the y-axis.").move_to(definition[7]).shift(LEFT * 0.2)
        
        endSentence1 = Tex(r"A function is an " ,  r"odd" , r" function if the graph of that function\\ is " , r"symmetric" , r" under a $180^{\circ}$ rotation about the origin.", tex_environment="center").scale(0.7)
        endSentence1[1].set_color(RED)
        endSentence1[3].set_color(RED)
        
        endSentence2 = Tex(r"A function is an " ,  r"even" , r" function if the graph of that function\\ is " , r"symmetric" , r" under a reflection about the y-axis.", tex_environment="center").scale(0.7)
        endSentence2[1].set_color(RED)
        endSentence2[3].set_color(RED)

        VGroup(endSentence1 , endSentence2).arrange(DOWN , buff=1)

        cornerText1 = Tex(r"$\bullet$ Odd Function").scale(0.55).to_corner(UL)
        cornerText2 = Tex(r"$\bullet$ Even Function").scale(0.55).next_to(cornerText1 , DOWN).align_to(cornerText1 , LEFT)


        self.add(number_plane , ghostCurve , curve , functionText)
        self.wait()

        self.play(Rotate(curve , PI))
        self.wait(0.5)
        self.play(Rotate(curve , PI))

        self.play(Indicate(functionText))
        self.play(FadeIn(screen_rectangle) , Write(definition[:3]))
        self.play(Write(definition[3:6]))
        self.play(Write(definition[6:]))
        self.play(Wiggle(definition[5]))
        self.play(Circumscribe(definition[7] , fade_in=True , stroke_width=1.5))
        self.play(ReplacementTransform(definition[1] , wordEven) , definition[0].animate.shift(LEFT * 0.05) , definition[2:4].animate.shift(RIGHT * 0.05))
        self.play(ReplacementTransform(definition[7] , replacement2) , definition[4:7].animate.shift(RIGHT * 0.2))
        self.play(FadeOut(screen_rectangle) , VGroup(definition , wordEven , replacement2).animate.scale(0.6).to_edge(UP))
        self.play(Circumscribe(replacement2 , fade_in=True , stroke_width=1.5))
        self.play(curve.animate.scale([-1,1,1])) 
        self.play(FadeOut(functionText , number_plane , curve , ghostCurve) , ReplacementTransform(VGroup(definition , wordEven , replacement2) , VGroup(endSentence1 , endSentence2)))

        self.play(TransformFromCopy(endSentence1[1] , cornerText1) , TransformFromCopy(endSentence2[1] , cornerText2) , FadeOut(endSentence1 , endSentence2) , FadeIn(number_plane))


        self.wait()
    

class Scene4(Scene):
    def construct(self):
        cornerText1 = Tex(r"$\bullet$ Odd Function").scale(0.55).to_corner(UL)
        cornerText2 = Tex(r"$\bullet$ Even Function").scale(0.55).next_to(cornerText1 , DOWN).align_to(cornerText1 , LEFT)
        number_plane = NumberPlane(
            x_range=[-10, 10, 1],        
            y_range=[-6, 6, 1],        
            x_length = config.frame_width,
            y_length = config.frame_height,

            background_line_style={
                "stroke_color": BLUE,
                "stroke_width": 1,
            },
            axis_config={
                "include_numbers": True,
                "font_size": 15,
                "line_to_number_buff" : 0.07,
                "stroke_color": WHITE,
            },
            tips=False
        )
        number_plane.set_stroke(opacity=0.35) 
        cross = Cross(Dot() , RED , stroke_width=2 , scale_factor=1.5).next_to(cornerText1 , RIGHT)
        check = CheckMark().scale(0.3).next_to(cornerText2 , RIGHT)

        curve1 = number_plane.plot(lambda x : (x**2) , [-10 , 10] , stroke_width = 3 , color=OUTPUT_COLOR)
        curve1_mini = number_plane.plot(lambda x : (x**2) , [-2.7 , 2.7] , stroke_width = 3 , color=OUTPUT_COLOR)
        ghostCurve1 = curve1.copy()
        ghostCurve1.set_stroke(opacity=0.3)
        functionText1 = MathTex(r"f(" , r"x" , r") = " , r"x" , r"^2" , color=OUTPUT_COLOR).scale(0.7).to_corner(UR)
        functionText1[1].set_color(INPUT_COLOR)
        functionText1[3].set_color(INPUT_COLOR)

        curve2_1 = number_plane.plot(lambda x : -1 , [-10 , 0] , stroke_width = 3 , color=OUTPUT_COLOR)
        curve2_2 = number_plane.plot(lambda x : 1 , [0 , 10] , stroke_width = 3 , color=OUTPUT_COLOR)
        curve2 = VGroup(curve2_1 , curve2_2)

        ghostCurve2 = curve2.copy()
        ghostCurve2.set_stroke(opacity=0.3)
        functionText2 = MathTex(r"f(" , r"x" , r") = \frac{\left|x\right|}{" , r"x" , r"}" , color=OUTPUT_COLOR).scale(0.7).to_corner(UR)
        functionText2[1].set_color(INPUT_COLOR)
        functionText2[2][3].set_color(INPUT_COLOR)
        functionText2[3].set_color(INPUT_COLOR)
        # functionText2[5].set_color(INPUT_COLOR)

        self.add(number_plane , cornerText1 , cornerText2)
        self.play(Write(functionText1) , Create(curve1 , rate_func = linear) , Create(ghostCurve1 , rate_func = linear))
        self.play(cornerText1.animate.set_color(YELLOW))
        self.play(Rotate(curve1 , PI , about_point=ORIGIN))
        self.play(cornerText1.animate.set_color(RED) , FadeIn(cross))
        self.play(Rotate(curve1 , -PI , about_point=ORIGIN))
        self.play(cornerText2.animate.set_color(YELLOW))
        self.play(curve1.animate.scale([-1,1,1]))
        self.play(cornerText2.animate.set_color(GREEN) , FadeIn(check))

        self.play(FadeOut(ghostCurve1) , FadeIn(curve1_mini) , run_time = 0.1)
        self.play(FadeOut(curve1))
        self.play(TransformMatchingTex(functionText1 , functionText2) , ReplacementTransform(curve1_mini , curve2) , FadeOut(cross , check) , cornerText1.animate.set_color(WHITE) , cornerText2.animate.set_color(WHITE))
        self.play(FadeIn(ghostCurve2) , run_time = 0.1)

        


        self.wait()
