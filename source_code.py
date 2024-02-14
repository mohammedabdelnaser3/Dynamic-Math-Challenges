import random
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

timeout_called = False
score = 0
end = 1
Equation = ""
answer = ""
Time = 30

operations = ["+", "-", "*", "/"]

def numberOfOperations():
    global score
    return random.choice(range(1, min(8, score + 2)))

def generateOperator():
    return random.choice(operations)

def generateNumber(end):
    return random.choice(range(1, end))

def generateEquation():
    global score, end
    end = 5 ** ((score // 5) + 1)
    size = numberOfOperations()
    equation = str(generateNumber(end))
    # 5
    # 5 + 4 - 3
    for idx in range(size):
        equation += " " + generateOperator() + " " + str(generateNumber(end))

    return equation

def solveEquation(Equation):
    Equation = Equation.split()
    # 4 + 6 + 5

    updatedEquation = []

    idx = 0

    while idx < len(Equation):
        if Equation[idx] == '*':
            x = float(updatedEquation.pop())
            y = float(Equation[idx + 1])
            updatedEquation.append(str(x * y))
            idx += 2
        elif Equation[idx] == '/':
            x = float(updatedEquation.pop())
            y = float(Equation[idx + 1])
            updatedEquation.append(str(x / y))
            idx += 2
        else:
            updatedEquation.append(Equation[idx])
            idx += 1

    res = float(updatedEquation[0])

    for idx in range(len(updatedEquation)):
        if updatedEquation[idx] == '+':
            res += float(updatedEquation[idx + 1])
        elif updatedEquation[idx] == '-':
            res -= float(updatedEquation[idx + 1])

    return res

def checkAnswer():
    global Equation, answer, passed, score, Time
    Time = -1
    answer = answerEntry.get("1.0", tk.END)
    answerEntry.delete("1.0", tk.END)
    correctAnswer = solveEquation(Equation)

    if answer == "":
        messagebox.showinfo("Result", "You failed to solve the equation in time or you didn't enter an answer.\nCorrect answer is {:.1f}".format(correctAnswer))
        messagebox.showinfo("Status", "You solved " + str(score) + " equations!")
        root.destroy()
        return
    elif abs(correctAnswer - float(answer)) > 0.1:
        messagebox.showinfo("Result", "Your answer is wrong.\nCorrect answer is {:.1f}".format(correctAnswer))
        messagebox.showinfo("Status", "You solved " + str(score) + " equations!")
        passed = 0
        root.destroy()
        return
    else:
        score += 1
        main()
        scoreLabel["text"] = "Score: \t{}".format(score)

def update_timer():
    global Time, answer, timeout_called
    timer["text"] = f"Time remaining: {Time}s"

    if answer != "":
        return
    elif Time > 0:
        Time -= 1
        root.after(1000 * (score + 1),update_timer)
    elif Time == 0:
        timeout()

def main():
    global Equation, equationLabel, answer, Time
    Equation = generateEquation()
    equationLabel["text"] = Equation
    answer = ""
    Time = 30
    update_timer()

def timeout():
    global timeout_called
    if timeout_called == False:
        timeout_called = True
        messagebox.showinfo("Result", "Time's up! You didn't enter an answer in time.\nCorrect answer is {:.1f}".format(solveEquation(Equation)))
        messagebox.showinfo("Status", "You solved " + str(score) + " equations!")
        root.destroy()
        return

root = tk.Tk()
root.geometry("850x400")
root.title("Dynamic Math Challenges")

image = Image.open("mathbackground.png")
background = ImageTk.PhotoImage(image)
background_label = tk.Label(root, image=background)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

scoreLabel = tk.Label(root, text= "Score: \t 0", font=("Arial", 10))
scoreLabel.place(x = 150, y = 95)

equationLabel = tk.Label(root, text=Equation, font=("Arial", 20))
equationLabel.pack(padx=80, pady=100)

timer = tk.Label(root, text="Time remaining: 30s", font=("Arial", 10))
timer.pack(padx = 200, pady = 0)

text = tk.Label(root, text="Your Answer: ", font=("Arial", 10))
text.pack()


answerEntry = tk.Text(root, height="1", width="20")
answerEntry.pack()

button = tk.Button(root, text="Check Answer", font=("Arial", 10), width="12", height="1", command=checkAnswer)
button.pack(padx=10, pady=10)


main()

root.mainloop()
