import turtle

class LSystem:
    def __init__(self, axiom="F", rules=None, iterations=4, angle=25):
        if rules is None:
            rules = {"F": "F[+F]F[-F]F"}
        self.axiom = axiom
        self.rules = rules
        self.iterations = iterations
        self.angle = angle
        self.result = self.generate()

    def generate(self):
        result = self.axiom
        for _ in range(self.iterations):
            next_result = ""
            for char in result:
                next_result += self.rules.get(char, char)
            result = next_result
        return result

    def draw(self):
        stack = []
        turtle.speed(0)
        turtle.left(90)
        for char in self.result:
            if char == "F":
                turtle.forward(10)
            elif char == "+":
                turtle.right(self.angle)
            elif char == "-":
                turtle.left(self.angle)
            elif char == "[":
                stack.append((turtle.position(), turtle.heading()))
            elif char == "]":
                pos, head = stack.pop()
                turtle.penup()
                turtle.setposition(pos)
                turtle.setheading(head)
                turtle.pendown()

    def run(self):
        self.draw()
        turtle.done()
