from manim import *
from utilities import myScale , truncate_decimal , TransformMatchingFromCopy , FadeInAndOutDirectional , Slider , FadeOutAll , FadeOutAllExcept
from icons import screenRectanlge , CheckMark
from math import sin , cos , floor , log , exp
from scipy.interpolate import interp1d
from scipy.integrate import quad

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
        cross2 = Cross(Dot() , RED , stroke_width=2 , scale_factor=1.5).next_to(cornerText2 , RIGHT)
        check = CheckMark().scale(0.3).next_to(cornerText1 , RIGHT)
        check2 = CheckMark().scale(0.3).next_to(cornerText2 , RIGHT)

        curve1 = number_plane.plot(lambda x : (x**2) , [-10 , 10] , stroke_width = 3 , color=OUTPUT_COLOR)
        curve1_mini = number_plane.plot(lambda x : (x**2) , [-2.7 , 2.7] , stroke_width = 3 , color=OUTPUT_COLOR)
        ghostCurve1 = curve1.copy()
        ghostCurve1.set_stroke(opacity=0.3)
        functionText1 = MathTex(r"f(" , r"x" , r") = " , r"x" , r"^2" , color=OUTPUT_COLOR).scale(0.7).to_corner(UR)
        functionText1[1].set_color(INPUT_COLOR)
        functionText1[3].set_color(INPUT_COLOR)

        curve2_1 = VGroup(
            number_plane.plot(lambda x : -1 , [-10 , -0.03] , stroke_width = 3 , color=OUTPUT_COLOR),
            Dot(number_plane.c2p(0,-1) , radius=0.035 , stroke_width=2 , fill_opacity=0 , color=OUTPUT_COLOR)
        )
        curve2_2 = VGroup(
            number_plane.plot(lambda x : 1 , [0.03 , 10] , stroke_width = 3 , color=OUTPUT_COLOR),
            Dot(number_plane.c2p(0,1) , radius=0.035 , stroke_width=2 , fill_opacity=0 , color=OUTPUT_COLOR)
        )
        curve2 = VGroup(curve2_1 , curve2_2)

        ghostCurve2 = curve2.copy()
        ghostCurve2.set_stroke(opacity=0.3)
        functionText2 = MathTex(r"f(" , r"x" , r") = \frac{\left|x\right|}{" , r"x" , r"}" , color=OUTPUT_COLOR).scale(0.7).to_corner(UR)
        functionText2[1].set_color(INPUT_COLOR)
        functionText2[2][3].set_color(INPUT_COLOR)
        functionText2[3].set_color(INPUT_COLOR)


        curve3 = number_plane.plot(lambda x: ((x**4) * 0.5) - (2 * x * x) - 1 + x , x_range=[-5 , 5] , color=OUTPUT_COLOR , stroke_width = 3)
        curve3_mini = number_plane.plot(lambda x: ((x**4) * 0.5) - (2 * x * x) - 1 + x , x_range=[-2.8 , 2.5] , color=OUTPUT_COLOR , stroke_width = 3)
        ghostCurve3 = curve3.copy()
        ghostCurve3.set_stroke(opacity=0.3)
        functionText3 = MathTex(r"f(" , r"x" , r") = " , r"\frac{x^4}{2}-2" , r"x" , r"^2 + " , r"x", r"-1" , color=OUTPUT_COLOR).scale(0.7).to_corner(UR)
        functionText3[1].set_color(INPUT_COLOR)
        functionText3[3][0].set_color(INPUT_COLOR)
        functionText3[4].set_color(INPUT_COLOR)
        functionText3[6].set_color(INPUT_COLOR)

        curve4 = number_plane.plot(lambda x: sin(x) , x_range=[-11 , 11] , color=OUTPUT_COLOR , stroke_width = 3)
        ghostCurve4 = curve4.copy()
        ghostCurve4.set_stroke(opacity=0.3)
        functionText4 = MathTex(r"f(" , r"x" , r") = \sin(" , r"x" , r")" , color=OUTPUT_COLOR).scale(0.7).to_corner(UR)
        functionText4[1].set_color(INPUT_COLOR)
        functionText4[3].set_color(INPUT_COLOR)

        curve5 = number_plane.plot(lambda x: 0 , x_range=[-11 , 11] , color=OUTPUT_COLOR , stroke_width = 3)
        ghostCurve5 = curve5.copy()
        ghostCurve5.set_stroke(opacity=0.3)
        functionText5 = MathTex(r"f(" , r"x" , r") = 0" , color=OUTPUT_COLOR).scale(0.7).to_corner(UR)
        functionText5[1].set_color(INPUT_COLOR)
        
        curve6 = VGroup()
        for i in range(-11 , 11 , 1):
            l = Line(number_plane.c2p(i , i) , number_plane.c2p(i+1 , i) , color=OUTPUT_COLOR , stroke_width = 3)
            s = Dot(number_plane.c2p(i , i) , radius=0.04 , fill_opacity=1 , fill_color = OUTPUT_COLOR)
            h = Dot(number_plane.c2p(i+1 , i) , radius=0.03 , fill_opacity=1 , fill_color = BLACK , stroke_width=3 , stroke_color=OUTPUT_COLOR)
            curve6.add(VGroup(l , s , h))

        ghostCurve6 = curve6.copy()
        ghostCurve6.set_stroke(opacity=0.3)
        ghostCurve6.set_fill(opacity=0.3)
        functionText6 = MathTex(r"f(" , r"x" , r") = \lfloor x \rfloor" , color=OUTPUT_COLOR).scale(0.7).to_corner(UR)
        functionText6[1].set_color(INPUT_COLOR)
        functionText6[2][3].set_color(INPUT_COLOR)


        self.add(number_plane , cornerText1 , cornerText2)
        self.play(Write(functionText1) , Create(curve1 , rate_func = linear) , Create(ghostCurve1 , rate_func = linear))
        self.play(cornerText1.animate.set_color(YELLOW))
        self.play(Rotate(curve1 , PI , about_point=ORIGIN))
        self.play(cornerText1.animate.set_color(RED) , FadeIn(cross))
        self.play(Rotate(curve1 , -PI , about_point=ORIGIN))
        self.play(cornerText2.animate.set_color(YELLOW))
        self.play(curve1.animate.scale([-1,1,1]))
        self.play(cornerText2.animate.set_color(GREEN) , FadeIn(check2))

        self.play(FadeOut(ghostCurve1) , FadeIn(curve1_mini) , run_time = 0.1)
        self.play(FadeOut(curve1))
        self.play(TransformMatchingTex(functionText1 , functionText2) , ReplacementTransform(curve1_mini , VGroup(curve2_1[0] , curve2_2[0])) , FadeIn(curve2_1[1] , curve2_2[1]) , FadeOut(cross , check2) , cornerText1.animate.set_color(WHITE) , cornerText2.animate.set_color(WHITE))
        self.play(FadeIn(ghostCurve2) , run_time = 0.1)

        self.play(cornerText1.animate.set_color(YELLOW) , Rotate(curve2 , PI , about_point=ORIGIN))
        
        self.play(cornerText1.animate.set_color(GREEN) , FadeIn(check))
        self.play(cornerText2.animate.set_color(YELLOW))
        self.play(curve2.animate.scale([-1,1,1]))
        self.play(cornerText2.animate.set_color(RED) , FadeIn(cross2))
        self.play(curve2.animate.scale([-1,1,1]))
        self.play(FadeOut(ghostCurve2) , run_time = 0.1)

        self.play(TransformMatchingTex(functionText2 , functionText3) , FadeTransform(curve2 , curve3_mini) , FadeOut(cross2 , check) , cornerText1.animate.set_color(WHITE) , cornerText2.animate.set_color(WHITE))
        self.play(FadeIn(ghostCurve3 , curve3) , run_time = 0.1)
        self.play(FadeOut(curve3_mini))
        self.play(cornerText1.animate.set_color(YELLOW))
        self.play(Rotate(curve3 , PI , about_point=ORIGIN))

        self.play(cornerText1.animate.set_color(RED) , FadeIn(cross))
        self.play(Rotate(curve3 , -PI , about_point=ORIGIN))
        self.play(cornerText2.animate.set_color(YELLOW))
        self.play(curve3.animate.scale([-1 , 1 , 1]))
        self.play(cornerText2.animate.set_color(RED) , FadeIn(cross2))
        self.play(curve3.animate.scale([-1 , 1 , 1]))

        self.play(FadeOut(ghostCurve3) , run_time = 0.1)
        self.play(TransformMatchingTex(functionText3 , functionText4) , ReplacementTransform(curve3 , curve4) , FadeOut(cross , cross2) , cornerText1.animate.set_color(WHITE) , cornerText2.animate.set_color(WHITE))
        self.add(ghostCurve4)
        self.play(cornerText1.animate.set_color(YELLOW))
        self.play(Rotate(curve4 , PI , about_point=ORIGIN))
        self.play(cornerText1.animate.set_color(GREEN) , FadeIn(check))
        self.play(cornerText2.animate.set_color(YELLOW))
        self.play(curve4.animate.scale([-1,1,1]))
        self.play(cornerText2.animate.set_color(RED) , FadeIn(cross2))
        self.play(curve4.animate.scale([-1,1,1]))

        self.play(FadeOut(ghostCurve4) , run_time = 0.1)
        self.play(TransformMatchingTex(functionText4 , functionText5) , ReplacementTransform(curve4 , curve5) , FadeOut(check , cross2) , cornerText1.animate.set_color(WHITE) , cornerText2.animate.set_color(WHITE))
        self.add(ghostCurve5)
        self.play(cornerText1.animate.set_color(YELLOW))
        self.play(Rotate(curve5 , PI , about_point=ORIGIN))
        self.play(cornerText1.animate.set_color(GREEN) , FadeIn(check))
        self.play(cornerText2.animate.set_color(YELLOW))
        self.play(curve5.animate.scale([-1,1,1]))
        self.play(cornerText2.animate.set_color(GREEN) , FadeIn(check2))
        

        self.play(FadeOut(ghostCurve5) , run_time = 0.1)
        self.play(TransformMatchingTex(functionText5 , functionText6) , FadeTransform(curve5 , curve6) , FadeOut(check , check2) , cornerText1.animate.set_color(WHITE) , cornerText2.animate.set_color(WHITE))
        self.add(ghostCurve6)
        self.play(cornerText1.animate.set_color(YELLOW))
        self.play(Rotate(curve6 , PI , about_point=ORIGIN))
        self.play(cornerText1.animate.set_color(RED) , FadeIn(cross))
        self.play(Rotate(curve6 , -PI , about_point=ORIGIN))
        self.play(cornerText2.animate.set_color(YELLOW))
        self.play(curve6.animate.scale([-1,1,1]))
        self.play(cornerText2.animate.set_color(RED) , FadeIn(cross2))
        self.play(curve6.animate.scale([-1,1,1]))
        

        text = Tex("Example: ")
        equation = MathTex(r"f(" , r"x" , r") = " , r"x" , r"^3 - " , r"x" , color=OUTPUT_COLOR)
        equation[1].set_color(INPUT_COLOR)
        equation[3].set_color(INPUT_COLOR)
        equation[5].set_color(INPUT_COLOR)
        endtext = VGroup(text , equation).arrange(RIGHT)

        self.play(FadeOut(cornerText1 , cornerText2 , functionText6 , curve6 , ghostCurve6 , cross , cross2 , number_plane) , Write(endtext))

        self.wait()


class Scene5(MovingCameraScene):
    def construct(self):
        text = Tex("Example: ")
        equation = MathTex(r"f(" , r"x" , r") = " , r"x" , r"^3" , r"-" , r"x" , color=OUTPUT_COLOR)
        equation[1].set_color(INPUT_COLOR)
        equation[3].set_color(INPUT_COLOR)
        equation[6].set_color(INPUT_COLOR)
        exampleFunction = VGroup(text , equation).arrange(RIGHT)


        equation2 = MathTex(r"f(" , r"-x" , r")" , r"=" , r"(" , r"-x" , r")^3" ,  r"-" , r"(" , r"-x" , r")", color=OUTPUT_COLOR).scale(0.9).shift(UP * 0.4)
        equation2[1].set_color(INPUT_COLOR)
        equation2[5].set_color(INPUT_COLOR)
        equation2[9].set_color(INPUT_COLOR)
        
        equation3 = MathTex(r"f(" , r"-x" , r")" , r"=" , r"-(" , r"x" , r")^3" ,  r"+" , r"x", color=OUTPUT_COLOR).scale(0.9).next_to(equation2 , DOWN).align_to(equation2 , LEFT)
        equation3[1].set_color(INPUT_COLOR)
        equation3[5].set_color(INPUT_COLOR)
        equation3[8].set_color(INPUT_COLOR)
        
        equation4 = MathTex(r"f(" , r"-x" , r")" , r"=" , r"-(" , r"x" , r"^3" ,  r"-" , r"x" , r")", color=OUTPUT_COLOR).scale(0.9).next_to(equation3 , DOWN).align_to(equation2 , LEFT)
        equation4[1].set_color(INPUT_COLOR)
        equation4[5].set_color(INPUT_COLOR)
        equation4[8].set_color(INPUT_COLOR)
        
        equation5 = MathTex(r"f(" , r"-x" , r")" , r"=" , r"-f(" , r"x" , r")" , color=OUTPUT_COLOR).scale(0.9).next_to(equation4 , DOWN).align_to(equation2 , LEFT)
        equation5[1].set_color(INPUT_COLOR)
        equation5[5].set_color(INPUT_COLOR)
        
        equation6 = MathTex(r"f(" , r"x" , r")" , r"=" , r"x" , r"^4 - 2" , r"x" , r"^2 + 1" , color=OUTPUT_COLOR).move_to(equation).shift(UP * 2).align_to(equation , LEFT)
        equation6[1].set_color(INPUT_COLOR)
        equation6[4].set_color(INPUT_COLOR)
        equation6[6].set_color(INPUT_COLOR)
        
        equation7 = MathTex(r"f(" , r"-x" , r")" , r"=" , r"(" , r"-x" , r")^4" , r"- 2(" , r"-x" , r")^2 " , r"+ 1" , color=OUTPUT_COLOR).scale(0.9).move_to(equation2).align_to(equation2 , LEFT)
        equation7[1].set_color(INPUT_COLOR)
        equation7[5].set_color(INPUT_COLOR)
        equation7[8].set_color(INPUT_COLOR)

        equation8 = MathTex(r"f(" , r"-x" , r")" , r"=" , r"x" , r"^4" , r"- 2" , r"x" , r"^2" , r"+ 1" , color=OUTPUT_COLOR).scale(0.9).move_to(equation3).align_to(equation3 , LEFT)
        equation8[1].set_color(INPUT_COLOR)
        equation8[4].set_color(INPUT_COLOR)
        equation8[7].set_color(INPUT_COLOR)

        equation9 = MathTex(r"f(" , r"-x" , r")" , r"=" , r"f(" , r"x" , r")" , color=OUTPUT_COLOR).scale(0.9).move_to(equation4).align_to(equation4 , LEFT)
        equation9[1].set_color(INPUT_COLOR)
        equation9[5].set_color(INPUT_COLOR)

        oddIf = Tex("Odd Function" , " if: " , r"$f(-x) = -f(x)$")
        evenIf = Tex("Even Function" , " if: " , r"$f(-x) = f(x)$")

        oddIf[0].set_color(YELLOW)
        evenIf[0].set_color(YELLOW)

        endtexts = VGroup(oddIf , evenIf).arrange(DOWN)

        number_plane1 = NumberPlane(
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
        number_plane1.set_stroke(opacity=0.35) 
        number_plane1.scale(0.5)

        number_plane2 = number_plane1.copy()

        curve1 = number_plane1.plot(lambda x : (x**3) - (3*x) , x_range=[-2.35,2.35] , stroke_width = 2 , color=OUTPUT_COLOR)
        ghostCurve1 = curve1.copy()
        ghostCurve1.set_stroke(opacity=0.3)

        curve2 = number_plane2.plot(lambda x : (x**4) - (2*x*x) - 1 , x_range=[-1.95,1.95] , stroke_width = 2 , color=OUTPUT_COLOR)
        ghostCurve2 = curve2.copy()
        ghostCurve2.set_stroke(opacity = 0.3)

        topGraph = VGroup(number_plane1 , curve1 , ghostCurve1)
        bottomGraph = VGroup(number_plane2 , curve2 , ghostCurve2)

        VGroup(topGraph , bottomGraph).arrange(DOWN , buff=0).shift(LEFT * config.frame_width/4)
        topGraph.scale(0.9)
        bottomGraph.scale(0.9)

        box1 = Rectangle(height=topGraph.height , width=topGraph.width , stroke_color = YELLOW , stroke_opacity = 1 , stroke_width = 3 , fill_opacity = 0).move_to(topGraph)
        box2 = Rectangle(height=bottomGraph.height , width=bottomGraph.width , stroke_color = YELLOW , stroke_opacity = 1 , stroke_width = 3  , fill_opacity = 0).move_to(bottomGraph)
        topGraph.add(box1)
        bottomGraph.add(box2)

        arrow = DoubleArrow(start = ORIGIN , end = RIGHT*2 , tip_length=0.2 , stroke_width = 3).shift(LEFT * 0.2)


        self.add(exampleFunction)
        self.wait(0.5)
        self.play(exampleFunction.animate.shift(UP * 2) , Write(equation2[0:3]))
        self.wait(0.5)
        self.play(AnimationGroup(*[
            Write(equation2[3]),
            TransformMatchingFromCopy(equation[3:5] , equation2[4:7]),
            Write(equation2[7]),
            TransformMatchingFromCopy(equation[6] , equation2[8:11])
        ] , lag_ratio=0.3))

        self.play(AnimationGroup(*[
            Write(equation3[3]),
            TransformMatchingFromCopy(equation2[4:7] , equation3[4:7]),
            TransformMatchingFromCopy(equation2[8:11] , equation3[7:9])
        ] , lag_ratio=0.3))

        transformAnimations = [
            TransformMatchingFromCopy(equation3[5] , equation4[5]),
            TransformMatchingFromCopy(equation3[6][1] , equation4[6]),
            TransformMatchingFromCopy(equation3[8] , equation4[8]),
            Write(equation4[7]),
            TransformMatchingFromCopy(equation3[4][0] , equation4[4][0]),
            TransformMatchingFromCopy(equation3[4][1] , equation4[4][1]),
            TransformMatchingFromCopy(equation3[6][0] , equation4[9])
        ]

        self.play(AnimationGroup(*[
            Write(equation4[3]),
            AnimationGroup(*transformAnimations , lag_ratio=0)
        ] , lag_ratio=0.3))

        self.play(Write(equation5[3:]))
        self.play(Circumscribe(equation , stroke_width=2))

        self.play(Unwrite(equation[3:]) , Unwrite(equation2) , Unwrite(equation3[3:]) , Unwrite(equation4[3:]) , Unwrite(equation5[3:]) , run_time = 1)

        self.play(Write(equation6[4:]))
        self.play(Write(equation7))
        self.play(
            TransformMatchingFromCopy(equation7[3] , equation8[3]),
            TransformMatchingFromCopy(equation7[4:7] , equation8[4:6]),
            TransformMatchingFromCopy(equation7[7:10] , equation8[6:9]),
            TransformMatchingFromCopy(equation7[10] , equation8[9])
        )

        self.play(Write(equation9[3:]))
        self.play(Circumscribe(equation6 , stroke_width=2))

        self.play(*[FadeOut(mob)for mob in self.mobjects])

        self.play(Write(oddIf[0:2]))
        self.play(Write(oddIf[2:]))
        self.play(Write(evenIf[0:2]))
        self.play(Write(evenIf[2:]))

        self.play(endtexts.animate.scale(0.5).shift(RIGHT * config.frame_width/4) , FadeIn(number_plane1 , curve1 , ghostCurve1 , number_plane2 , curve2 , ghostCurve2 , box1 , box2))
        self.wait(0.5)
        self.play(Rotate(curve1 , PI) , curve2.animate.scale([-1,1,1]))
        self.wait(0.5)
        self.play(Rotate(curve1 , -PI) , curve2.animate.scale([-1,1,1]))
        self.wait(0.5)
        self.play(Rotate(curve1 , PI) , curve2.animate.scale([-1,1,1]) , FadeIn(arrow))
        self.wait(0.5)
        self.play(Rotate(curve1 , -PI) , curve2.animate.scale([-1,1,1]))


        title_text_1 = Text("Symmetry", color=BLUE, stroke_color=BLUE)
        title_text_2 = Text("Transformation", color=BLUE, stroke_color=BLUE)
        title_texts = VGroup(title_text_1, title_text_2).arrange(RIGHT, buff=3).scale(0.585).shift(RIGHT * 0.2).shift(DOWN * config.frame_height)
        title_text_1.scale(1.4).set_color(YELLOW)

        functionText = MathTex(r"f(" , r"x" , r") = " , r"x" , r"^2" , color=OUTPUT_COLOR).scale(0.8).to_corner(UL)
        functionText[1].set_color(INPUT_COLOR)
        functionText[3].set_color(INPUT_COLOR)

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
        functionText.shift(DOWN * config.frame_height)
        number_plane.shift(DOWN * config.frame_height)


        self.add(title_texts)
        self.play(self.camera.frame.animate.shift(DOWN * config.frame_height))
        self.play(title_text_1.animate.scale(1/1.4).set_color(BLUE) , title_text_2.animate.scale(1.4).set_color(YELLOW))
        self.play(FadeOut(title_texts) , Create(number_plane) , Write(functionText))

        self.wait()

class Scene6(Scene):
    def construct(self):
        functionText = MathTex(r"f(" , r"x" , r") = " , r"x" , r"^2" , r"-2" , color=OUTPUT_COLOR).scale(0.8).to_corner(UL)
        functionText[1].set_color(INPUT_COLOR)
        functionText[3].set_color(INPUT_COLOR)

        modification1 = MathTex(r"f(" , r"x" , r") =" , r"(" , r"x" , r"+1)^2" , r"-2" , color=OUTPUT_COLOR).scale(0.8).to_corner(UL)
        modification1[1].set_color(INPUT_COLOR)
        modification1[4].set_color(INPUT_COLOR)

        modification2 = MathTex(r"f(" , r"x" , r") =" , r"-" , r"(" , r"x" , r"+1)^2" , r"-2" , color=OUTPUT_COLOR).scale(0.8).to_corner(UL)
        modification2[1].set_color(INPUT_COLOR)
        modification2[5].set_color(INPUT_COLOR)

        modification3 = MathTex(r"f(" , r"x" , r") =" , r"x" , r"^2" , color=OUTPUT_COLOR).scale(0.8).move_to(modification2).align_to(modification2 , LEFT)
        modification3[1].set_color(INPUT_COLOR)
        modification3[3].set_color(INPUT_COLOR)

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


        curveMini = number_plane.plot(lambda x : x*x , [-2.8 , 2.8] , color=OUTPUT_COLOR , stroke_width = 3)
        curve = number_plane.plot(lambda x : x*x , [-5 , 5] , color=OUTPUT_COLOR , stroke_width = 3)

        t_value = ValueTracker(-PI/2)

        def point(t):
            x = (sin(t) + 1) * cos(t) 
            y = (sin(t) + 1) * sin(t) * (1-0.3 * sin(t))
            return [x,-y]
        
        def curveDrawer(t):            
            c = number_plane.plot(lambda x : x*x , [-5 , 5] , color=OUTPUT_COLOR , stroke_width = 3).shift(number_plane.c2p(point(t)[0] , point(t)[1]))
            return c

        redrawingCurve = always_redraw(lambda : curveDrawer(t_value.get_value()))

        doubleArrowCross = always_redraw(lambda :  VGroup(
            DoubleArrow(start = UP , end = DOWN , tip_length = 0.2),
            DoubleArrow(start = LEFT , end = RIGHT , tip_length = 0.2)
        ).shift(UP).shift(number_plane.c2p( point(t_value.get_value())[0] , point(t_value.get_value())[1] )))

        arrow1 = Arrow(start = ORIGIN , end = RIGHT , buff=0.2).scale(1.2).shift(UP + RIGHT*0.2)
        arrow2 = Arrow(start = ORIGIN , end = LEFT , buff=0.2).scale(1.2).shift(UP + LEFT*0.2)

        arrow3 = Arrow(start = ORIGIN , end = RIGHT , buff=0.2).scale([-1.2 , 1.2 , 1.2]).shift(UP + RIGHT*0.2)
        arrow4 = Arrow(start = ORIGIN , end = LEFT , buff=0.2).scale([-1.2 , 1.2 , 1.2]).shift(UP + LEFT*0.2)

        arrow5 = DoubleArrow(start = RIGHT*0.5 , end = LEFT * 0.5 , tip_length = 0.4 , stroke_width = 2).shift(UP)

        transformationText1 = Tex("Translation / Shifting").shift(UP * 1.5).align_to(functionText , LEFT)
        transformationText2 = Tex("Stretching or Compressing").scale(0.9).shift(UP * 1.5).align_to(functionText , LEFT)
        transformationText3 = Tex("Reflecting").shift(UP * 1.5).align_to(functionText , LEFT)

        self.add(functionText[:5] , number_plane)
        self.wait(0.3)
        self.play(Create(curveMini))
        self.add(curve)
        self.play(FadeOut(curveMini) , run_time = 0.1)
        self.play(FadeIn(functionText[5] , shift=DOWN * 0.1) , curve.animate.shift(DOWN * (number_plane.c2p(0,2)[1])))
        self.play(TransformMatchingShapes(functionText[3:5] , modification1[3:6]) , functionText[5].animate.move_to(modification1[6]) , curve.animate.shift(LEFT * number_plane.c2p(1,0)[0]))
        self.play(Write(modification2[3]) , modification1[3:6].animate.move_to(modification2[4:7]) , functionText[5].animate.move_to(modification2[7]) , Rotate(curve , PI , RIGHT , number_plane.c2p(-1,-2)))
        self.play(curve.animate.scale([1,-1,1]).shift(number_plane.c2p(1,27)) , FadeIn(modification3[-1]) , FadeOut(modification2[3] , functionText[5] , modification1[3] , modification1[5]) , modification1[4].animate.move_to(modification3[3]))
        self.play(FadeIn(doubleArrowCross) , Write(transformationText1) , run_time = 1)
        self.add(redrawingCurve)
        self.play(FadeOut(curve) , run_time = 0.1)
        self.play(t_value.animate.set_value((3 * PI)/2) , rate_func = linear , run_time = 2)
        self.play(TransformMatchingTex(transformationText1 , transformationText2) , FadeOut(doubleArrowCross))
        
        self.add(curve)
        self.play(FadeOut(redrawingCurve) , run_time = 0.1)
        self.play(FadeInAndOutDirectional(arrow1 , RIGHT * 0.3) , FadeInAndOutDirectional(arrow2 , LEFT * 0.3), curve.animate.scale([1.4,1,1]) , run_time = 1)
        self.play(FadeInAndOutDirectional(arrow3 , LEFT * 0.3) , FadeInAndOutDirectional(arrow4 , RIGHT * 0.3), curve.animate.scale([0.4,1,1]) , run_time = 1)
        self.play(TransformMatchingTex(transformationText2 , transformationText3))
        self.play(curve.animate.scale([-1,1,1]) , FadeInAndOutDirectional(arrow5 , ORIGIN , run_time = 1))

        self.play(FadeOut(curve , functionText[:3] , modification1[4] , transformationText3 , modification3[-1]))

        functionText2 = MathTex(r"f(" , r"x" , r") = " , r"x" , r"^{\frac{2}{3}}" , color=OUTPUT_COLOR).to_corner(UL , buff=0.3)
        functionText2[1].set_color(INPUT_COLOR)
        functionText2[3].set_color(INPUT_COLOR)

        curve2_1 = number_plane.plot(lambda x: pow(x*x , 1/3) , [-10,0] , color=OUTPUT_COLOR , stroke_width = 3)
        curve2_2 = number_plane.plot(lambda x: pow(x*x , 1/3) , [0,10] , color=OUTPUT_COLOR , stroke_width = 3)

        self.play(Write(functionText2) , Create(VGroup(curve2_1 , curve2_2)))

        self.wait()

class Scene7(Scene):
    def construct(self):
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

        functionText = MathTex(r"f(" , r"x" , r") = " , r"x" , r"^{\frac{2}{3}}" , color=OUTPUT_COLOR).to_corner(UL , buff=0.3)
        functionText[1].set_color(INPUT_COLOR)
        functionText[3].set_color(INPUT_COLOR)

        curve_p1 = number_plane.plot(lambda x: pow(x*x , 1/3) , [-10,0] , color=OUTPUT_COLOR , stroke_width = 3)
        curve_p2 = number_plane.plot(lambda x: pow(x*x , 1/3) , [0,10] , color=OUTPUT_COLOR , stroke_width = 3)
        curve = VGroup(curve_p1 , curve_p2)

        x_value = ValueTracker(3)
        pointOnCurve = always_redraw(lambda : Dot(number_plane.c2p(x_value.get_value() , pow(x_value.get_value()**2 , 1/3)) , radius = 0.05 , color=YELLOW) )
        
        def xlinesGiver(x):
            lines = number_plane.get_lines_to_point(number_plane.c2p(x , pow(x**2 , 1/3)))[0]
            lines.set_color(INPUT_COLOR)

            x_text = MathTex(r"x" , color=INPUT_COLOR).scale(0.5).next_to(lines , UP , buff=0.1)
            
            return VGroup(lines , x_text)
        xLine = always_redraw(lambda : xlinesGiver(x_value.get_value()))
        
        def ylinesGiver(x):
            lines = number_plane.get_lines_to_point(number_plane.c2p(x , pow(x**2 , 1/3)))[1]
            lines.set_color(OUTPUT_COLOR)

            fx_text = MathTex(r"f(" , r"x" , r")" , color=OUTPUT_COLOR).scale(0.5).rotate(PI/2).next_to(lines , RIGHT , buff=0.1)
            fx_text[1].set_color(INPUT_COLOR)

            return VGroup(lines , fx_text)
        yLine = always_redraw(lambda : ylinesGiver(x_value.get_value()))

        hLine1 = Line(start=number_plane.c2p(0,0) , end = number_plane.c2p(-8,0) , color=WHITE , stroke_width = 2)
        hLine2 = Line(start=number_plane.c2p(0,4) , end = number_plane.c2p(-8,4) , color=WHITE , stroke_width = 2)

        self.add(number_plane , functionText , curve)

        self.wait(0.5)
        self.play(FadeIn(pointOnCurve) , FocusOn(pointOnCurve , run_time = 0.8))
        self.play(FadeIn(xLine))
        self.play(FadeIn(yLine))
        self.play(x_value.animate.set_value(8))
        self.play(x_value.animate.set_value(-8) , run_time = 2)
        self.play(FadeOut(xLine , yLine , pointOnCurve))
        self.wait()

class Scene8(Scene):
    def construct(self):
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

        functionF = MathTex(r"f(" , r"x" , r") = " , r"x" , r"^{\frac{2}{3}}" , color=OUTPUT_COLOR).to_corner(UL , buff=0.3)
        functionF[1].set_color(INPUT_COLOR)
        functionF[3].set_color(INPUT_COLOR)

        functionFNext = MathTex(r"f(" , r"x" , r") = " , r"x" , r"^2" , color=OUTPUT_COLOR).move_to(functionF).align_to(functionF , DL)
        functionFNext[1].set_color(INPUT_COLOR)
        functionFNext[3].set_color(INPUT_COLOR)

        functionG = MathTex(r"g(" , r"x" , r") = " , r"f(" , r"x" , r")" , r"- 2" , color=GREEN).scale(0.9).to_edge(LEFT , buff=0.3).shift(DOWN)
        functionG[1].set_color(INPUT_COLOR)
        functionG[4].set_color(INPUT_COLOR)
        functionG[3].set_color(OUTPUT_COLOR)
        functionG[5].set_color(OUTPUT_COLOR)
                                            
        functionG_next = MathTex(r"g(" , r"x" , r") = " , r"x" , r"^\frac{2}{3}" , r"- 2" , color=GREEN).scale(0.9).move_to(functionG).align_to(functionG , LEFT).shift(UP * 0.05)
        functionG_next[1].set_color(INPUT_COLOR)
        functionG_next[3].set_color(INPUT_COLOR)
        functionG_next[4].set_color(OUTPUT_COLOR)

        functionG2 = MathTex(r"g(" , r"x" , r") = " , r"f(" , r"x" , r")" , r"+ 1" , color=GREEN).scale(0.9).to_edge(LEFT , buff=0.3).shift(DOWN)
        functionG2[1].set_color(INPUT_COLOR)
        functionG2[4].set_color(INPUT_COLOR)
        functionG2[3].set_color(OUTPUT_COLOR)
        functionG2[5].set_color(OUTPUT_COLOR)

        functionGWithA = MathTex(r"g(" , r"x" , r") = " , r"f(" , r"x" , r")" , r"+ a" , color=GREEN).scale(0.9).to_edge(LEFT , buff=0.3).shift(DOWN)
        functionGWithA[1].set_color(INPUT_COLOR)
        functionGWithA[4].set_color(INPUT_COLOR)
        functionGWithA[3].set_color(OUTPUT_COLOR)
        functionGWithA[5].set_color(OUTPUT_COLOR)

        aValueTracker = ValueTracker(1)

        curve_p1 = number_plane.plot(lambda x: pow(x*x , 1/3) , [-10,0] , color=OUTPUT_COLOR , stroke_width = 3)
        curve_p2 = number_plane.plot(lambda x: pow(x*x , 1/3) , [0,10] , color=OUTPUT_COLOR , stroke_width = 3)
        curve = VGroup(curve_p1 , curve_p2)
        curveCopy = curve.copy()

        nextCurve = curve.copy().shift(number_plane.c2p(0,-2))
        nextCurve[0].set_color(GREEN)
        nextCurve[1].set_color(GREEN)

        def nextCurveGiver():
            c = curve.copy().shift(number_plane.c2p(0 , aValueTracker.get_value()))
            c[0].set_color(GREEN)
            c[1].set_color(GREEN)

            return c

        nextCurve2 = always_redraw(nextCurveGiver)

        parabolap1 = number_plane.plot(lambda x: x*x , [-2.45,0] , color=OUTPUT_COLOR , stroke_width = 3)
        parabolap2 = number_plane.plot(lambda x: x*x , [0,2.45] , color=OUTPUT_COLOR , stroke_width = 3)
        parabola = VGroup(parabolap1 , parabolap2)

        parabolaGreenp1 = number_plane.plot(lambda x: (x*x)-2 , [-2.85,0] , color=GREEN , stroke_width = 3)
        parabolaGreenp2 = number_plane.plot(lambda x: (x*x)-2 , [0,2.85] , color=GREEN , stroke_width = 3)
        parabolaGreen = VGroup(parabolaGreenp1 , parabolaGreenp2)

        points = VGroup()
        points_on_curve = VGroup()
        lines = VGroup()

        nextPoints = VGroup()
        nextLines = VGroup()

        n = 101
        for i in range(n):
            x = (i * (20/(n-1))) - 10
            y = pow(x*x , 1/3)

            #bad variable names example:
            d = Dot(number_plane.c2p(x , 0) , color=YELLOW , radius=0.025)
            p = Dot(number_plane.c2p(x , y) , color=OUTPUT_COLOR , radius=0.035)
            l = Line(start=d.get_center() , end = p.get_center() , color=WHITE , stroke_width = 1.5)

            np = Dot(number_plane.c2p(x , y-2) , color=GREEN , radius=0.035)
            nl = Line(start=d.get_center() , end = np.get_center() , color=WHITE , stroke_width = 1.5)
             

            points.add(d)
            points_on_curve.add(p)
            lines.add(l)

            nextPoints.add(np)
            nextLines.add(nl)
        
        aValueText = MathTex(r"a:" , color=GREEN).scale(0.67).next_to(functionGWithA , DOWN , buff=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER * 1.5).align_to(functionGWithA , LEFT)
        
        def aSliderGiver():
            s = Slider(
                x_min=-3,
                x_max=3,
                x=1,
                length=4.5,
                dot_config={
                    "color": BLUE,
                    "radius": 0.03,
                },
                line_config={
                    "include_numbers": True,
                    "font_size": 20
                }
            ).next_to(aValueText , RIGHT)

            return s
            
        aValueSlider = aSliderGiver()


        self.add(number_plane , functionF , curve)
        self.wait(0.5)
        self.play(Write(functionG))

        self.play(Wiggle(functionG[3:6]))
        self.play(Indicate(functionG[1]))
        self.play(TransformMatchingFromCopy(functionG[1] , functionG[4]))
        self.play(Circumscribe(functionG[6] , shape=Circle , stroke_width = 1.8))
        self.play(Circumscribe(functionF , stroke_width = 1.8))
        self.play(TransformMatchingFromCopy(functionF[3:] , functionG_next[3:5]) , FadeOut(functionG[3:6]) , TransformMatchingShapes(functionG[6] , functionG_next[-1]) , TransformMatchingShapes(functionG[:3] , functionG_next[:3]))
        self.play(TransformMatchingTex(functionG_next , functionG))

        points_fadeIn = [FadeIn(point , scale=5 , run_time = 0.3) for point in points]
        lines_create = [Create(line) for line in lines]
        pointsOnCurve_fadeIn = [FadeIn(point , shift = UP * point.get_y()) for point in points_on_curve]

        self.play(AnimationGroup(*points_fadeIn , lag_ratio=0.03))
        self.play(AnimationGroup(*lines_create) , AnimationGroup(*pointsOnCurve_fadeIn))

        self.play(Transform(points_on_curve , nextPoints) , Transform(lines , nextLines))
        self.play(Create(nextCurve))
        self.play(FadeOut(points , points_on_curve , lines))
        self.play(TransformMatchingShapes(functionF[-1] , functionFNext[-1]) , ReplacementTransform(curve[0] , parabola[0]) , ReplacementTransform(curve[1] , parabola[1]) , FadeOut(nextCurve) )
        self.play(TransformFromCopy(parabola.copy() , parabolaGreen))
        self.play(Circumscribe(functionG , stroke_width=1.8))

        self.play(TransformMatchingShapes(functionFNext[-1] , functionF[-1]) , ReplacementTransform(parabola , curveCopy) , FadeOut(parabolaGreen))
        self.play(TransformMatchingTex(functionG , functionG2) , FocusOn(functionG2[-1] , opacity=0.5))
        self.play(TransformFromCopy(curveCopy , nextCurve2))

        self.play(TransformMatchingTex(functionG2 , functionGWithA) , Write(aValueText) , FadeIn(aValueSlider) )
        self.play(aValueTracker.animate.set_value(3) , aValueSlider.animate.set_value(3))
        self.play(aValueTracker.animate.set_value(-3) , aValueSlider.animate.set_value(-3) , run_time = 2)

        self.play(FadeOut(functionGWithA , aValueText , aValueSlider , nextCurve2))

        self.wait()


class Scene9(Scene):
    def construct(self):
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

        aValueTracker = ValueTracker(-1)

        functionF = MathTex(r"f(" , r"x" , r") = " , r"x" , r"^{\frac{2}{3}}" , color=OUTPUT_COLOR).to_corner(UL , buff=0.3)
        functionF[1].set_color(INPUT_COLOR)
        functionF[3].set_color(INPUT_COLOR)

        functionG = MathTex(r"g(" , r"x" , r") = f(" , r"x" , r"-1" , r")" , color=GREEN).scale(0.9).to_edge(LEFT , buff=0.3).shift(DOWN)
        functionG[1].set_color(INPUT_COLOR)
        functionG[3].set_color(INPUT_COLOR)
        functionG[2][2].set_color(OUTPUT_COLOR)

        functionGNext = MathTex(r"g(" , r"x" , r") = f(" , r"x" , r"+1" , r")" , color=GREEN).scale(0.9).to_edge(LEFT , buff=0.3).shift(DOWN)
        functionGNext[1].set_color(INPUT_COLOR)
        functionGNext[3].set_color(INPUT_COLOR)
        functionGNext[2][2].set_color(OUTPUT_COLOR)

        functionGNext2 = MathTex(r"g(" , r"x" , r") = f(" , r"x" , r"+a" , r")" , color=GREEN).scale(0.9).to_edge(LEFT , buff=0.3).shift(DOWN)
        functionGNext2[1].set_color(INPUT_COLOR)
        functionGNext2[3].set_color(INPUT_COLOR)
        functionGNext2[2][2].set_color(OUTPUT_COLOR)


        exampleFunctionG = MathTex(r"g(" , r"3" , r")" , r"= f(" , r"3" , r"-1" , r")" , color=GREEN).scale(0.9).next_to(functionG , DOWN , buff=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER * 2).align_to(functionG , LEFT)
        exampleFunctionG[1].set_color(INPUT_COLOR)
        exampleFunctionG[4].set_color(INPUT_COLOR)
        exampleFunctionG[3][1].set_color(OUTPUT_COLOR)

        exampleFunctionG2 = MathTex(r"g(" , r"3" , r")" , r"= f(" , r"2" , r")" , color=GREEN).scale(0.9).next_to(functionG , DOWN , buff=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER * 2).align_to(functionG , LEFT)
        exampleFunctionG2[1].set_color(INPUT_COLOR)
        exampleFunctionG2[4].set_color(INPUT_COLOR)
        exampleFunctionG2[3][1].set_color(OUTPUT_COLOR)

        rightPoint = Dot(number_plane.c2p(3,0) , radius=0.03 , color=YELLOW)
        leftPoint = Dot(number_plane.c2p(2,0) , radius=0.03 , color=YELLOW)
        arrow = Arrow(rightPoint.get_center() , leftPoint.get_center() , buff=0 , color=BLUE , max_tip_length_to_length_ratio=0.2)
        
        outputLine = Line(start=leftPoint.get_center() , end = number_plane.c2p(2 , pow(4,1/3)) , color=WHITE , stroke_width = 1.8)
        outputPoint = Dot(number_plane.c2p(2,pow(4,1/3)) , radius=0.03 , color=RED)
        outputPoint2 = Dot(number_plane.c2p(3,pow(4,1/3)) , radius=0.03 , color=GREEN)


        curve_p1 = number_plane.plot(lambda x: pow(x*x , 1/3) , [-15,0] , color=OUTPUT_COLOR , stroke_width = 3)
        curve_p2 = number_plane.plot(lambda x: pow(x*x , 1/3) , [0,15] , color=OUTPUT_COLOR , stroke_width = 3)
        curve = VGroup(curve_p1 , curve_p2)

        greenCurve = always_redraw(lambda : curve.copy().set_color(GREEN).shift(number_plane.c2p(-aValueTracker.get_value() , 0)))
        aValueText = MathTex(r"a:" , color=GREEN).scale(0.67).next_to(functionGNext2 , DOWN , buff=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER * 1.8).align_to(functionGNext2 , LEFT)
        
        def aSliderGiver():
            s = Slider(
                x_min=-3,
                x_max=3,
                x=1,
                length=4.5,
                dot_config={
                    "color": BLUE,
                    "radius": 0.03,
                },
                line_config={
                    "include_numbers": True,
                    "font_size": 20
                }
            ).next_to(aValueText , RIGHT)

            return s
        aValueSlider = aSliderGiver()


        self.add(functionF , number_plane , curve)
        self.wait(0.3)
        self.play(Write(functionG))
        self.play(Circumscribe(functionG[1] , stroke_width=2) , Circumscribe(functionG[3:5] , stroke_width=2))
        self.play(FadeIn(rightPoint , scale = 7 , run_time = 0.7))
        self.play(Write(exampleFunctionG))

        self.play(GrowArrow(arrow) , TransformFromCopy(rightPoint , leftPoint) , TransformMatchingShapes(exampleFunctionG[:3] , exampleFunctionG2[:3]) , TransformMatchingShapes(exampleFunctionG[3:] , exampleFunctionG2[3:]))
        self.play(Circumscribe(rightPoint , Circle , fade_out=True , stroke_width=1))
        self.play(Circumscribe(leftPoint , Circle , fade_out=True , stroke_width=1))

        self.play(Create(outputLine) , FadeIn(outputPoint , shift = number_plane.c2p(0,1.58 , 0)))
        self.play(outputLine.animate.shift(number_plane.c2p(1,0,0)) , Transform(outputPoint , outputPoint2))
        
        self.play(FadeOut(exampleFunctionG2 , arrow , leftPoint , outputLine , rightPoint))

        self.play(TransformFromCopy(curve , greenCurve))
        self.play(FadeOut(outputPoint))

        self.play(TransformMatchingTex(functionG , functionGNext) , FocusOn(functionGNext[4]))
        self.play(aValueTracker.animate.set_value(1))
        self.play(TransformMatchingTex(functionGNext , functionGNext2) , Write(aValueText) , FadeIn(aValueSlider))
        self.play(aValueTracker.animate.set_value(3) , aValueSlider.animate.set_value(3))
        self.play(aValueTracker.animate.set_value(-3) , aValueSlider.animate.set_value(-3))

        self.play(FadeOutAllExcept(self , number_plane))

        self.wait()

class Scene10(Scene):
    def construct(self):
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

        functionF = MathTex(r"f(" , r"x" , r") = -" , r"x" , r"^2" , color=OUTPUT_COLOR).to_corner(UL , buff=0.3)
        functionF[1].set_color(INPUT_COLOR)
        functionF[3].set_color(INPUT_COLOR)

        functionG = MathTex(r"g(" , r"x" , r")", r" = " , r"f" , r"(" , r"x" , r"-2)" , r"+3" , color=GREEN).next_to(functionF , DOWN , buff=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER * 2).align_to(functionF , LEFT)
        functionG[1].set_color(INPUT_COLOR)
        functionG[6].set_color(INPUT_COLOR)
        functionG[4].set_color(OUTPUT_COLOR)

        functionG2 = MathTex(r" = " , r"-" , r"(" , r"x" , r"-2)" , r"^2" , r"+3" , color=GREEN).next_to(functionG , DOWN , buff=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER * 1.7).align_to(functionG[3] , LEFT)
        functionG2[3].set_color(INPUT_COLOR)

        curve = number_plane.plot(lambda x: -x*x , [-3,3] , color=OUTPUT_COLOR , stroke_width = 3)
        curve_faded = curve.copy().set_stroke(opacity=0.3)

        curveGreen = number_plane.plot(lambda x: -x*x , [-3,3] , color=GREEN , stroke_width = 3).shift(number_plane.c2p(2,0))

        self.add(number_plane)
        self.wait(0.4)
        self.play(Write(functionF) , Create(curve) , Create(curve_faded))
        self.play(FocusOn(ORIGIN))
        self.play(curve_faded.animate.shift(number_plane.c2p(2,3)))
        self.play(FadeOut(curve_faded))
        curve_faded.shift(number_plane.c2p(-2,-3))
        self.add(curve_faded)
        self.play(Write(functionG[:3]))
        self.play(curve_faded.animate.shift(number_plane.c2p(2,0)))
        self.play(curve_faded.animate.shift(number_plane.c2p(0,3)))
        
        self.play(FadeOut(curve_faded))

        self.play(Write(functionG[3:8]))
        self.play(TransformFromCopy(curve , curveGreen))
        self.play(Write(functionG[8:]))
        self.play(curveGreen.animate.shift(number_plane.c2p(0,3)))

        self.play(Circumscribe(functionG[4:8] , stroke_width=2 , fade_out=True))
        self.play(Indicate(functionF[1]))
        self.play(functionF[2][2].animate.scale(1.1).set_color(YELLOW) , run_time = 0.5)
        self.play(functionF[3].animate.scale(1.1).set_color(YELLOW) , run_time = 0.5)
        self.play(functionF[4].animate.scale(1.1).set_color(YELLOW) , run_time = 0.5)

        self.play(functionF[2][2].animate.scale(1/1.1).set_color(OUTPUT_COLOR) , functionF[3].animate.scale(1/1.1).set_color(INPUT_COLOR) , functionF[4].animate.scale(1/1.1).set_color(OUTPUT_COLOR))
        self.play(Write(functionG2[0]))
        self.play(FadeIn(functionG2[1] , scale=1.4) , run_time = 0.5)
        self.play(FadeIn(functionG2[2:5] , scale=1.4) , run_time = 0.5)
        self.play(FadeIn(functionG2[5] , scale=1.4) , run_time = 0.5)
        self.play(Write(functionG2[6]))
        self.play(Circumscribe(functionG[4:] , stroke_width=2 , fade_out=True))
        self.play(Circumscribe(functionG2[1:] , stroke_width=2 , fade_out=True))

        self.play(FadeOutAllExcept(self , number_plane))

        self.wait()

class Scene11(Scene):
    def construct(self):
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

        functionF = MathTex(r"f(" , r"x" , r") = " , r"x" , r" + 2\cos(" , r"x" , r")" , color=OUTPUT_COLOR).to_corner(UL , buff=0.3)
        functionF[1].set_color(INPUT_COLOR)
        functionF[3].set_color(INPUT_COLOR)
        functionF[5].set_color(INPUT_COLOR)

        functionG = MathTex(r"g(" , r"x" , r")" , r" = " , r"2" , r"f" , r"(" , r"x" , r")" , color=GREEN).scale(0.95).next_to(functionF , DOWN , buff=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER * 2).align_to(functionF , LEFT)
        functionG[1].set_color(INPUT_COLOR)
        functionG[7].set_color(INPUT_COLOR)
        functionG[5].set_color(OUTPUT_COLOR)
        functionG.z_index=1000

        functionG2 = MathTex(r"g(" , r"x" , r")" , r" = " , r"a" , r"f" , r"(" , r"x" , r")" , color=GREEN).scale(0.95).next_to(functionF , DOWN , buff=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER * 2).align_to(functionF , LEFT)
        functionG2[1].set_color(INPUT_COLOR)
        functionG2[7].set_color(INPUT_COLOR)
        functionG2[5].set_color(OUTPUT_COLOR)

        aValueText = MathTex(r"a: " , color=GREEN).scale(0.8).next_to(functionG2 , DOWN).align_to(functionG2 , LEFT)

        aValueSlider = Slider(
            x=2,
            length=3.5,
            dot_config={
                "color": BLUE,
                "radius": 0.03,
            },
            line_config={
                "include_numbers": True,
                "font_size": 15
            }
        ).next_to(aValueText , RIGHT)

        # dynamicFunctionG = VGroup(functionG2 , aValueText , aValueSlider)
        # dynamicFunctionG.add_background_rectangle()

        curve = number_plane.plot(lambda x : x + 2 * cos(x) , [-8 , 8] , color=OUTPUT_COLOR , stroke_width = 3)
        curveG = number_plane.plot(lambda x : x + 2 * cos(x) , [-10 , 10] , color=OUTPUT_COLOR , stroke_width = 3)

        scaleValue = ValueTracker(2)
        opacityValue = ValueTracker(1)
        dynamicCurveG = always_redraw(lambda : number_plane.plot(lambda x : x + 2 * cos(x) , [-10 , 10] , color=GREEN , stroke_width = 3).scale([1 , scaleValue.get_value() , 1] , about_point = ORIGIN).set_stroke(opacity=opacityValue.get_value()))

        points = VGroup()
        xValues = [-1.02987]

        for xValue in xValues:
            dot = Dot(number_plane.c2p(xValue , 0) , radius=0.03 , color=YELLOW)
            points.add(dot)



        self.add(number_plane)
        self.wait(0.5)
        # self.play(FadeInAndOutDirectional(arrow1 , UP) , FadeInAndOutDirectional(arrow2 , UP) , FadeInAndOutDirectional(arrow3 , DOWN) , FadeInAndOutDirectional(arrow4 , DOWN))
        self.play(number_plane.animate.scale([1,1.5,1]) , run_time = 0.5)
        self.play(number_plane.animate.scale([1,1/1.5,1]) , run_time = 0.5)
        self.wait(0.5)

        self.play(number_plane.animate.scale([1.5,1,1]) , run_time = 0.5)
        self.play(number_plane.animate.scale([1/1.5,1,1]) , run_time = 0.5)

        self.play(Write(functionF))
        self.play(Create(curve) , Create(curveG))
        self.play(Write(functionG[:3]))
        self.play(Write(functionG[3:]))

        self.play(curveG.animate.scale([1,2,1] , about_point = ORIGIN).set_color(GREEN))

        xValueTracker = ValueTracker(2.6)
        xLine = always_redraw(lambda : Line(start=number_plane.c2p(xValueTracker.get_value() , 0) , end = number_plane.c2p(xValueTracker.get_value() , (2 * (xValueTracker.get_value() + 2 * cos(xValueTracker.get_value())) ) ) , stroke_width = 2 , color=WHITE))
        movingPoints = always_redraw(lambda : 
            VGroup(
                Dot(number_plane.c2p(xValueTracker.get_value() , (xValueTracker.get_value() + 2 * cos(xValueTracker.get_value())) ) , radius = 0.04 , color=YELLOW),
                Dot(number_plane.c2p(xValueTracker.get_value() , (2 * (xValueTracker.get_value() + 2 * cos(xValueTracker.get_value())) ) ) , radius = 0.04 , color=YELLOW),
            )                             
        )

        self.play(FadeIn(xLine , movingPoints))
        self.play(xValueTracker.animate.set_value(0) , run_time = 1.5 )
        self.play(xValueTracker.animate.set_value(-2) , run_time = 1.5 )

        self.play(FadeOut(xLine , movingPoints))

        self.play(curveG.animate.set_stroke(opacity=0.217))

        points_fadeIn = [FadeIn(point , scale=6 , run_time = 1) for point in points]
        self.play(AnimationGroup(*points_fadeIn , lag_ratio=0.2))
        self.play(curveG.animate.set_stroke(opacity=1) , FadeOut(points))

        self.play(Circumscribe(functionG , stroke_width = 2))

        backgroundRectangles = VGroup(
            BackgroundRectangle(functionG2),
            BackgroundRectangle(aValueText),
            BackgroundRectangle(aValueSlider)
        )
        backgroundRectangles.set_z_index(-1000)
        functionG.set_z_index(1000)
        number_plane.set_z_index(-10000)

        self.play(FadeIn(backgroundRectangles , run_time = 0.5) , TransformMatchingTex(functionG , functionG2 , run_time = 0.6) , Write(aValueText) , FadeIn(aValueSlider))
        self.add(dynamicCurveG)
        self.play(FadeOut(curveG , run_time = 0.1))
        
        self.play(scaleValue.animate.set_value(3) , aValueSlider.animate.set_value(3))
        self.play(scaleValue.animate.set_value(0.5) , aValueSlider.animate.set_value(0.5))
        self.play(scaleValue.animate.set_value(-1) , aValueSlider.animate.set_value(-1))

        point = Dot(number_plane.c2p(3,0) , radius=0.03 , color=YELLOW)
        verticalLine = Line(start=number_plane.c2p(3,0) , end=number_plane.c2p(3 , 1.02) , stroke_width = 2)
        pointOnCurve = Dot(number_plane.c2p(3,1.02) , radius=0.045 , color=RED)

        newCurve = number_plane.plot(lambda x : x + 2 * cos(x) , [-10 , 10] , color=OUTPUT_COLOR , stroke_width = 3)

        self.play(FadeIn(point , scale=6 , run_time = 1) , opacityValue.animate.set_value(0.25))
        self.play(Create(verticalLine) , TransformFromCopy(point , pointOnCurve))
        self.play(Rotate(verticalLine , PI , RIGHT , about_point=number_plane.c2p(3,0) , rate_func = linear) , pointOnCurve.animate(rate_func = ease_in_out_sine).shift(number_plane.c2p(0 , 1.02 * -2)).set_color(GREEN))
        self.play(FadeOut(pointOnCurve , point , verticalLine))
        self.add(newCurve)
        self.play(newCurve.animate.scale([1,-1,1]  , about_point = ORIGIN).set_stroke(color=GREEN))
        self.wait(0.3)
        self.play(opacityValue.animate.set_value(1) , run_time = 0.1)
        self.play(FadeOut(newCurve) , run_time = 0.1)
        self.play(scaleValue.animate.set_value(-2) , aValueSlider.animate.set_value(-2))
        self.wait(0.3)
        self.play(opacityValue.animate.set_value(0))

        newCurve = number_plane.plot(lambda x : x + 2 * cos(x) , [-10 , 10] , color=OUTPUT_COLOR , stroke_width = 3)
        self.add(newCurve)
        self.play(newCurve.animate.scale([1,2,1]  , about_point = ORIGIN).set_stroke(color=GREEN))
        self.wait(0.3)
        self.play(newCurve.animate.scale([1,-1,1]  , about_point = ORIGIN))
        self.wait(0.3)

        self.play(opacityValue.animate.set_value(1) , run_time = 0.1)
        self.wait(0.3)
        self.play(FadeOut(newCurve) , run_time = 0.1)

        self.wait(0.3)
        self.play(scaleValue.animate.set_value(-0.5) , aValueSlider.animate.set_value(-0.5))
        self.wait(0.3)
        self.play(opacityValue.animate.set_value(0))
        self.wait(0.3)

        newCurve = number_plane.plot(lambda x : x + 2 * cos(x) , [-10 , 10] , color=OUTPUT_COLOR , stroke_width = 3)
        self.add(newCurve)
        self.play(newCurve.animate.scale([1,0.5,1]  , about_point = ORIGIN).set_stroke(color=GREEN))
        self.wait(0.3)
        self.play(newCurve.animate.scale([1,-1,1]  , about_point = ORIGIN))
        self.wait(0.3)

        self.play(opacityValue.animate.set_value(1) , run_time = 0.1)
        self.wait(0.3)
        self.play(FadeOut(newCurve) , run_time = 0.1)


        self.wait()

        self.play(FadeOutAllExcept(self , number_plane , functionF , curve))
        self.wait()


class Scene12(Scene):
    def construct(self):
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
        
        functionF = MathTex(r"f(" , r"x" , r") = " , r"x" , r"+2\cos(" , r"x" , r")" , color=OUTPUT_COLOR).to_corner(UL , buff=0.3)
        functionF[1].set_color(INPUT_COLOR)
        functionF[3].set_color(INPUT_COLOR)
        functionF[5].set_color(INPUT_COLOR)

        functionG = MathTex(r"g(" , r"x" , r") = " , r"f" , r"(3" , r"x" , r")" , color=GREEN).scale(0.95).next_to(functionF , DOWN , buff=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER * 2).align_to(functionF , LEFT)
        functionG[1].set_color(INPUT_COLOR)
        functionG[5].set_color(INPUT_COLOR)
        functionG[3].set_color(OUTPUT_COLOR)

        functionG2 = MathTex(r"g(" , r"x" , r") = " , r"f" , r"\left(\frac{x}{3}\right)" , color=GREEN).scale(0.95).next_to(functionF , DOWN , buff=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER * 2).align_to(functionF , LEFT)
        functionG2[1].set_color(INPUT_COLOR)
        functionG2[4][1].set_color(INPUT_COLOR)
        functionG2[3].set_color(OUTPUT_COLOR)

        functionG3 = MathTex(r"g(" , r"x" , r") = " , r"f" , r"\left(-\frac{x}{3}\right)" , color=GREEN).scale(0.95).next_to(functionF , DOWN , buff=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER * 2).align_to(functionF , LEFT)
        functionG3[1].set_color(INPUT_COLOR)
        functionG3[4][2].set_color(INPUT_COLOR)
        functionG3[3].set_color(OUTPUT_COLOR)

        functionG4 = MathTex(r"g(" , r"x" , r") = " , r"f" , r"(ax)" , color=GREEN).scale(0.95).next_to(functionF , DOWN , buff=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER * 2).align_to(functionF , LEFT)
        functionG4[1].set_color(INPUT_COLOR)
        functionG4[4][2].set_color(INPUT_COLOR)
        functionG4[3].set_color(OUTPUT_COLOR)

        aValueText = MathTex(r"a: " , color=GREEN).scale(0.8).next_to(functionG4 , DOWN).align_to(functionG4 , LEFT)

        aValueSlider = Slider(
            x=-1/3,
            length=3.5,
            dot_config={
                "color": BLUE,
                "radius": 0.03,
            },
            line_config={
                "include_numbers": True,
                "font_size": 15
            }
        ).next_to(aValueText , RIGHT)


        curve = number_plane.plot(lambda x : x + 2 * cos(x) , [-10 , 10] , color=OUTPUT_COLOR , stroke_width = 3)
        rightCurveG = number_plane.plot(lambda x : (3*x) + 2 * cos(3 * x) , x_range=[1 , 10] , color=GREEN , stroke_width = 3)
        
        scaleValue = ValueTracker(1/3)
        curveG = always_redraw(lambda : number_plane.plot(lambda x : (x) + 2 * cos(x) , x_range=[-10 , 10] , color=GREEN , stroke_width = 3).scale([scaleValue.get_value() , 1 , 1] , about_point = ORIGIN) )

        xValue = ValueTracker(1)

        exampleInputg = always_redraw(lambda : Dot(number_plane.c2p(xValue.get_value(),0) , radius=0.04 , color=YELLOW))
        exampleInputf = always_redraw(lambda : Dot(number_plane.c2p(xValue.get_value() * 3,0) , radius=0.04 , color=YELLOW))
        arrow = always_redraw(lambda : Arrow(exampleInputg.get_center() , exampleInputf.get_center() , buff=0 , color=BLUE , max_tip_length_to_length_ratio=0.15 , max_stroke_width_to_length_ratio=3))
        pointg = always_redraw(lambda : Dot(number_plane.c2p(xValue.get_value(), 3 * xValue.get_value() + 2*cos(3 * xValue.get_value())) , radius=0.04 , color=GREEN))
        pointf = always_redraw(lambda : Dot(number_plane.c2p(3 * xValue.get_value(), 3*xValue.get_value() + 2*cos(3 * xValue.get_value())) , radius=0.04 , color=OUTPUT_COLOR))
        linef = always_redraw(lambda : Line(exampleInputf.get_center() , pointf.get_center() , stroke_width = 2))
        lineg = always_redraw(lambda : Line(exampleInputg.get_center() , pointg.get_center() , stroke_width = 2))
        partialCurveg = always_redraw(lambda : number_plane.plot(lambda x : (3*x) + 2 * cos(3 * x) , x_range=([1 , xValue.get_value()] if xValue.get_value() >=1 else [xValue.get_value() , 1]) , color=GREEN , stroke_width = 3))

        self.add(number_plane , functionF , curve)
        self.wait(0.5)
        self.play(Write(functionG))
        self.play(FadeIn(exampleInputg , scale = 6))
        self.play(Circumscribe(VGroup(functionG[4][1] , functionG[5]) , Rectangle , stroke_width=2))
        self.play(TransformFromCopy(exampleInputg , exampleInputf) , GrowArrow(arrow))
        self.play(Circumscribe(exampleInputg , Circle , stroke_width=2))
        self.play(Circumscribe(exampleInputf , Circle , stroke_width=2))

        self.play(Create(linef) , TransformFromCopy(exampleInputf , pointf))
        self.play(TransformFromCopy(linef , lineg) , TransformFromCopy(pointf , pointg))
        self.add(partialCurveg)
        self.wait()

        self.play(Flash(exampleInputg.get_center() , line_length=0.18 , num_lines=11 , line_stroke_width=2 , time_width=0.45))
        self.play(Flash(pointg.get_center() , line_length=0.18 , num_lines=11 , line_stroke_width=2 , time_width=0.45))

        lineCopy = Line(exampleInputg.get_center() , pointg.get_center() , stroke_width = 4 , color=YELLOW)
        self.play(ShowPassingFlash(lineCopy , time_width=0.35))

        lineCopy = Line(exampleInputf.get_center() , pointf.get_center() , stroke_width = 4 , color=YELLOW)
        self.play(ShowPassingFlash(lineCopy , time_width=0.35))

        lineCopy = Line(ORIGIN , exampleInputf.get_center() , stroke_width = 4 , color=YELLOW)
        self.play(ShowPassingFlash(lineCopy , time_width=0.35))

        lineCopy = Line(ORIGIN , exampleInputg.get_center() , stroke_width = 4 , color=YELLOW)
        self.play(ShowPassingFlash(lineCopy , time_width=0.35))
        

        self.play(xValue.animate.set_value(1.72) , run_time = 2)
        self.add(rightCurveG)
        self.play(xValue.animate.set_value(-2.41) , run_time = 4.5 , rate_func = smootherstep)
        self.add(curveG)
        self.play(FadeOut(partialCurveg , rightCurveG) , run_time = 0.1)
        self.play(FadeOut(arrow , pointf , pointg , linef , lineg , exampleInputf , exampleInputg))

        yintercept = Dot(number_plane.c2p(0 , 2) , radius=0.05 , color=YELLOW)
        self.play(FadeIn(yintercept , run_time=1))

        explainerEquation = MathTex(r"(" , r"0" , r",g(" , r"0" , r"))" , color=GREEN).scale(0.75).next_to(functionG , DOWN).align_to(functionG , LEFT)
        explainerEquation[1].set_color(INPUT_COLOR)
        explainerEquation[3].set_color(INPUT_COLOR)

        explainerEquation2 = MathTex(r"(" , r"0" , r",f(" , r"3 \cdot 0" , r"))" , color=GREEN).scale(0.75).next_to(functionG , DOWN).align_to(functionG , LEFT)
        explainerEquation2[1].set_color(INPUT_COLOR)
        explainerEquation2[2][1].set_color(OUTPUT_COLOR)
        explainerEquation2[3].set_color(INPUT_COLOR)

        explainerEquation3 = MathTex(r"(" , r"0" , r",f(" , r"0" , r"))" , color=GREEN).scale(0.75).next_to(functionG , DOWN).align_to(functionG , LEFT)
        explainerEquation3[1].set_color(INPUT_COLOR)
        explainerEquation3[2][1].set_color(OUTPUT_COLOR)
        explainerEquation3[3].set_color(INPUT_COLOR)


        self.play(Write(explainerEquation))
        self.play(Circumscribe(functionG , stroke_width=2))
        self.play(
            TransformMatchingShapes(explainerEquation[:2] , explainerEquation2[:2]),
            TransformMatchingShapes(explainerEquation[2] , explainerEquation2[2]),
            TransformMatchingShapes(explainerEquation[3] , explainerEquation2[3]),
            TransformMatchingShapes(explainerEquation[4] , explainerEquation2[4]),
        )
        self.play(
            TransformMatchingShapes(explainerEquation2[:2] , explainerEquation3[:2]),
            TransformMatchingShapes(explainerEquation2[2] , explainerEquation3[2]),
            ReplacementTransform(explainerEquation2[3] , explainerEquation3[3]),
            TransformMatchingShapes(explainerEquation2[4] , explainerEquation3[4]),
        )

        self.play(FadeOut(yintercept , explainerEquation3))
        self.play(
            TransformMatchingShapes(functionG[:4] , functionG2[:4]),
            TransformMatchingShapes(functionG[4:] , functionG2[4:]),
        )
        self.play(scaleValue.animate.set_value(3))
      
        self.play(
            TransformMatchingShapes(functionG2[:4] , functionG3[:4]),
            TransformMatchingShapes(functionG2[4:] , functionG3[4:]),
        )

        self.play(scaleValue.animate.set_value(-3))
      
        self.play(
            TransformMatchingShapes(functionG3[:4] , functionG4[:4]),
            TransformMatchingShapes(functionG3[4:] , functionG4[4:]),
            Write(aValueText),
            FadeIn(aValueSlider)
        )

        self.play(aValueSlider.animate.set_value(-1) , scaleValue.animate.set_value(-1))
        self.wait(0.5)
        self.play(aValueSlider.animate.set_value(2) , scaleValue.animate.set_value(1/2))
        

        self.wait()

        self.play(FadeOutAllExcept(self , number_plane))
        self.wait()


class Scene13(Scene):
    def construct(self):
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

        def function(x):
            if(x==0):
                return 0
            
            return (1.36 * x * log(abs(0.25894 * x))) * pow(2 , -0.37493 * x)
        
        aValue = ValueTracker(1)
        bValue = ValueTracker(1)
        cValue = ValueTracker(0)
        dValue = ValueTracker(0)

        
        # Fancy Stuff that I totally understand.
        # And all this for what? Just to make the speed of the creation constant.
        # I thought it would look better (It doesn't). 

        # Step 1: Sample the curve
        x_vals = np.linspace(-5, 10, 1000)
        y_vals = np.array([function(x) for x in x_vals])

        # Step 2: Compute arc length differentials
        dx = np.gradient(x_vals)
        dy = np.gradient(y_vals)
        ds = np.sqrt(dx**2 + dy**2)
        s_vals = np.concatenate(([0], np.cumsum(ds[:-1])))

        # Step 3: Normalize s and build interpolators
        s_normalized = s_vals / s_vals[-1]
        interp_x = interp1d(s_normalized, x_vals)
        interp_y = interp1d(s_normalized, y_vals)

        # Step 4: Define the parametric function
        def gamma(t):
            return np.array([interp_x(t), interp_y(t), 0.0])

        # Step 5: Plot the parametric curve
        curve = number_plane.plot_parametric_curve(
            gamma,
            t_range=[0, 1],
            color=OUTPUT_COLOR,
            stroke_width = 3
        )

        curveG = always_redraw(lambda : number_plane.plot(lambda x : aValue.get_value() * function(bValue.get_value()*x + cValue.get_value()) + dValue.get_value() , [-10 , 10] , stroke_width = 3 , color= GREEN))


        functionF = MathTex(r"f(x)" , color = RED).scale(0.6).move_to(number_plane.c2p(8.5 , 1.5))
        functionF[0][2].set_color(INPUT_COLOR)

        functionG = MathTex(r"g(x) = af(bx + c) + d" , color=GREEN).scale(0.9).to_corner(UL , buff=0.25)
        functionG[0][2].set_color(INPUT_COLOR)
        functionG[0][9].set_color(INPUT_COLOR)
        functionG[0][6].set_color(OUTPUT_COLOR)

        aText = MathTex(r"a:" , color=GREEN).scale(0.7).next_to(functionG , DOWN , buff=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER * 1.5).align_to(functionG , LEFT)
        bText = MathTex(r"b:" , color=GREEN).scale(0.7).next_to(aText , DOWN , buff=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER * 1.5).align_to(functionG , LEFT)
        cText = MathTex(r"c:" , color=GREEN).scale(0.7).next_to(bText , DOWN , buff=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER * 1.5).align_to(functionG , LEFT)
        dText = MathTex(r"d:" , color=GREEN).scale(0.7).next_to(cText , DOWN , buff=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER * 1.5).align_to(functionG , LEFT)

        aSlider = Slider(
            x=1,
            length=3.5,
            dot_config={
                "color": BLUE,
                "radius": 0.026,
            },
            line_config={
                "include_numbers": True,
                "font_size": 15,
                "line_to_number_buff" : 0.18
            }
        ).next_to(aText , RIGHT)

        bSlider = Slider(
            x=1,
            length=3.5,
            dot_config={
                "color": BLUE,
                "radius": 0.026,
            },
            line_config={
                "include_numbers": True,
                "font_size": 15,
                "line_to_number_buff" : 0.18
            }
        ).next_to(bText , RIGHT)

        cSlider = Slider(
            x=0,
            length=3.5,
            dot_config={
                "color": BLUE,
                "radius": 0.026,
            },
            line_config={
                "include_numbers": True,
                "font_size": 15,
                "line_to_number_buff" : 0.18
            }
        ).next_to(cText , RIGHT)

        dSlider = Slider(
            x=0,
            length=3.5,
            dot_config={
                "color": BLUE,
                "radius": 0.026,
            },
            line_config={
                "include_numbers": True,
                "font_size": 15,
                "line_to_number_buff" : 0.18
            }
        ).next_to(dText , RIGHT)

        self.add(number_plane)
        self.wait(0.5)

        self.play(Create(curve) , rate_func = linear , run_time = 1.5)
        self.play(Write(functionF))

        self.play(Write(functionG))

        self.play(
            Write(aText),
            Write(bText),
            Write(cText),
            Write(dText),
            FadeIn(aSlider),
            FadeIn(bSlider),
            FadeIn(cSlider),
            FadeIn(dSlider)
        )

        self.play(VGroup(cText , cSlider , dText , dSlider).animate.to_corner(UR))

        self.play(Create(curveG) , rate_func = linear , run_time = 2)

        self.play(dSlider.animate.set_value(1) , dValue.animate.set_value(1) , run_time = 1.25)
        self.play(dSlider.animate.set_value(2) , dValue.animate.set_value(2) , run_time = 1.25)

        self.play(dSlider.animate.set_value(-2) , dValue.animate.set_value(-2) , run_time = 1.25)

        self.play(dSlider.animate.set_value(0) , dValue.animate.set_value(0) , run_time = 1)

        self.play(cSlider.animate.set_value(2) , cValue.animate.set_value(2) , run_time = 1)
        self.play(cSlider.animate.set_value(-2) , cValue.animate.set_value(-2) , run_time = 1)
        
        self.play(dSlider.animate.set_value(-3) , dValue.animate.set_value(-3) , run_time = 1)

        self.play(dSlider.animate.set_value(0) , dValue.animate.set_value(0) , cSlider.animate.set_value(0) , cValue.animate.set_value(0) , run_time = 1)
        
        self.play(aSlider.animate.set_value(2) , aValue.animate.set_value(2) , run_time = 1)
        self.play(aSlider.animate.set_value(0.5) , aValue.animate.set_value(0.5) , run_time = 1)
 
        self.play(aSlider.animate.set_value(0) , aValue.animate.set_value(0) , run_time = 1)
        self.wait(0.5)
        self.play(aSlider.animate.set_value(-2) , aValue.animate.set_value(-2) , run_time = 1)
        
        self.play(aSlider.animate.set_value(1) , aValue.animate.set_value(1) , run_time = 1)
        
        self.play(bSlider.animate.set_value(2) , bValue.animate.set_value(2) , run_time = 1)
        self.play(bSlider.animate.set_value(1/2) , bValue.animate.set_value(1/2) , run_time = 1)
        
        self.play(bSlider.animate.set_value(-2) , bValue.animate.set_value(-2) , run_time = 1)
        self.play(bSlider.animate.set_value(1) , bValue.animate.set_value(1) , run_time = 1)

        self.play(aSlider.animate.set_value(1.5) , bSlider.animate.set_value(2) , cSlider.animate.set_value(3) , dSlider.animate.set_value(-1))
        

        self.wait()

        def demoFunction(x):
            return (-4*x)/((x ** 2) + 1)

        parabola = number_plane.plot(demoFunction , [-10 , 10] , color=BLUE , stroke_width = 3)
        parabola2 = number_plane.plot(demoFunction , [-10 , 10] , color=RED , stroke_width = 3)


        self.play(FadeOutAllExcept(self , number_plane) , FadeIn(parabola , parabola2) , run_time = 0.8)

        self.play(parabola.animate.scale([1,2,1] , about_point = ORIGIN))
        self.play(parabola.animate.shift(number_plane.c2p(0,2)))

        self.play(parabola2.animate.shift(number_plane.c2p(0,2)))
        self.play(parabola2.animate.scale([1,2,1] , about_point = ORIGIN))
        
        self.play(FadeOutAllExcept(self , number_plane) , FadeIn(curve , curveG , functionG , functionF , aSlider , aText , bSlider , bText , cSlider , cText , dSlider , dText) , run_time = 0.8)

        self.play(Circumscribe(functionG[0][2] , Circle , fade_out=True , stroke_width=2) , Circumscribe(functionG[0][9] , Circle , fade_out=True , stroke_width=2))
        self.play(Indicate(functionG[0][8]))
        self.play(Indicate(functionG[0][11]))
        self.play(Indicate(functionG[0][5]))
        self.play(Indicate(functionG[0][14]))

        self.wait(0.5)
        self.play(Indicate(functionG[0][11]))
        self.play(Indicate(functionG[0][8]))
        self.play(Indicate(functionG[0][5]))
        self.play(Indicate(functionG[0][14]))

        self.play(cValue.animate.set_value(3))
        self.play(Circumscribe(cSlider.dot , Circle , stroke_width = 2.5))

        tip = ComplexValueTracker(1-1.4j)
        base = ComplexValueTracker(2-3j)

        arrow = always_redraw(lambda : Arrow(number_plane.c2p(base.points) , number_plane.c2p(tip.points) , color=BLUE , buff=SMALL_BUFF , max_tip_length_to_length_ratio=0.15 , max_stroke_width_to_length_ratio=3.5) )

        self.play(GrowArrow(arrow))

        self.play(tip.animate.set_value(-2-1.4j) , base.animate.set_value(-3-3j))
        self.play(tip.animate.set_value(-2+3j) , base.animate.set_value(4j))
        self.play(tip.animate.set_value(-5+3j) , base.animate.set_value(-3+4j))
        self.play(tip.animate.set_value(0) , base.animate.set_value(-1.5+1.2j))
        self.play(tip.animate.set_value(-3))

        self.play(FadeOut(arrow , scale = 0))

        self.play(bValue.animate.set_value(2))

        self.play(aValue.animate.set_value(1.5))
        self.play(dValue.animate.set_value(-1))

        self.wait()
        self.play(FadeOutAllExcept(self , number_plane))
        self.wait()


class Scene14(Scene):
    def construct(self):
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

        functionF = MathTex(r"f(x) = e^x" , color=RED).scale(0.95).to_corner(UL)
        functionF[0][2].set_color(INPUT_COLOR)
        functionF[0][6].set_color(INPUT_COLOR)

        functionG = MathTex(r"g(x) = \frac{1}{e^{2x+1}}-1" , color=GREEN).scale(0.95).next_to(functionF , DOWN).align_to(functionF , LEFT)
        functionG[0][2].set_color(INPUT_COLOR)
        functionG[0][9].set_color(INPUT_COLOR)

        curve = number_plane.plot(lambda x : exp(x) , [-10 , 1.8] , stroke_width = 3 , color = OUTPUT_COLOR)



        self.add(number_plane)
        self.wait(0.5)

        self.play(Write(functionF[0][:4]))
        self.play(Write(functionF[0][4:]))
        self.play(Create(curve))

        self.play(Write(functionG))

        self.play(functionF[0][2].animate.scale(1.2).set_color(YELLOW) , run_time = 0.5)
        self.play(functionF[0][5].animate.scale(1.2).set_color(YELLOW) , run_time = 0.5)
        self.play(functionF[0][6].animate.scale(1.2).set_color(YELLOW) , run_time = 0.5)

        self.play(Circumscribe(functionG[0][7:12] , Rectangle , stroke_width=2))

        self.wait()
