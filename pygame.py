import turtle
import time
import random

delay = 0.08 # ปรับให้เร็วขึ้นเล็กน้อยเพื่อให้ดูลื่นไหล
score = 0
high_score = 0

# --- 1. ตั้งค่าสภาพแวดล้อม (Environment) ---
wn = turtle.Screen()
wn.title("Snake Game - Organic Edition")
# สีพื้นหลังเขียวเข้ม (Dark Forest Green) ให้เหมือนสนามหญ้า
wn.bgcolor("#1a3300") 
wn.setup(width=600, height=600)
wn.tracer(0)

# --- 2. ส่วนหัวของงู ---
head = turtle.Turtle()
head.speed(0)
# เปลี่ยนเป็นวงกลมเพื่อให้ดูเป็นสิ่งมีชีวิต
head.shape("circle") 
# สีหัวเข้มพิเศษ
head.color("#006600") 
head.shapesize(1.2, 1.2) 
head.penup()
head.goto(0,0)
head.direction = "stop"

# --- ตกแต่งตาของงู (เพื่อให้ดูมีชีวิต) ---
# นี่เป็นเทคนิคซ้อน Turtle อีกตัวไว้บนหัวเพื่อทำเป็นตา
eye = turtle.Turtle()
eye.speed(0)
eye.shape("circle")
eye.color("yellow")
eye.shapesize(0.3, 0.3) 
eye.penup()
eye.hideturtle() # ซ่อนไว้ก่อน จะแสดงตอนขยับ

# --- 3. อาหาร (ผลไม้) ---
food = turtle.Turtle()
food.speed(0)
food.shape("circle")
# สีแดงมะเขือเทศ
food.color("#ff4d4d")
food.shapesize(0.8, 0.8)
food.penup()
food.goto(0,100)

segments = []

# --- 3.5 ป้ายคะแนน ---
pen = turtle.Turtle()
pen.speed(0)
pen.shape("square")
pen.color("white")
pen.penup()
pen.hideturtle()
pen.goto(0, 260)
pen.write("Score: 0  High Score: 0", align="center", font=("Arial", 20, "bold"))


# --- 4. ฟังก์ชันควบคุมทิศทาง ---
def go_up():
    if head.direction != "down":
        head.direction = "up"

def go_down():
    if head.direction != "up":
        head.direction = "down"

def go_left():
    if head.direction != "right":
        head.direction = "left"

def go_right():
    if head.direction != "left":
        head.direction = "right"

def move():
    move_distance = 22 # ปรับระยะก้าวให้พอดีกับวงกลม
    if head.direction == "up":
        y = head.ycor()
        head.sety(y + move_distance)
    if head.direction == "down":
        y = head.ycor()
        head.sety(y - move_distance)
    if head.direction == "left":
        x = head.xcor()
        head.setx(x - move_distance)
    if head.direction == "right":
        x = head.xcor()
        head.setx(x + move_distance)
    
    # อัปเดตตำแหน่งตาให้ตามหัวงู
    if head.direction != "stop":
        eye.clear()
        eye.goto(head.xcor(), head.ycor())
        # วาดตาสองข้างเล็กๆ บนหัว
        eye.showturtle()
        # (ใน turtle แบบง่าย เราแปะตาไว้ตรงกลางหัวแทนเพราะหมุนตายาก)

# --- 5. การควบคุมคีย์บอร์ด ---
wn.listen()
wn.onkeypress(go_up, "w")
wn.onkeypress(go_down, "s")
wn.onkeypress(go_left, "a")
wn.onkeypress(go_right, "d")
wn.onkeypress(go_up, "Up")
wn.onkeypress(go_down, "Down")
wn.onkeypress(go_left, "Left")
wn.onkeypress(go_right, "Right")

def update_score():
    pen.clear()
    pen.write("Score: {}  High Score: {}".format(score, high_score), align="center", font=("Arial", 20, "bold"))

def reset_game():
    global score, delay
    time.sleep(1)
    head.goto(0,0)
    head.direction = "stop"
    eye.hideturtle() # ซ่อนตา

    for segment in segments:
        segment.goto(1000, 1000)
    segments.clear()
    
    score = 0
    delay = 0.08
    update_score()
    wn.bgcolor("#f19113f8") # รีเซ็ตสีพื้นหลัง

# --- 6. ลูปหลักของเกม ---
while True:
    wn.update()

    # ชนขอบจอ
    if head.xcor()>280 or head.xcor()<-280 or head.ycor()>280 or head.ycor()<-280:
        # เอฟเฟกต์จอแดงเมื่อตาย
        wn.bgcolor("#F10E0E")
        wn.update()
        reset_game()

    # กินอาหาร
    if head.distance(food) < 22:
        x = random.randint(-270, 270)
        y = random.randint(-270, 270)
        food.goto(x,y)

        # สร้างลำตัวใหม่
        new_segment = turtle.Turtle()
        new_segment.speed(0)
        new_segment.shape("circle") # ลำตัวกลม
        
        # --- เทคนิค Realism: สลับสีเกล็ดงู (Scales) ---
        # ถ้าเป็นท่อนคู่ให้สีอ่อน ท่อนคี่ให้สีเข้ม ดูมีมิติ
        if len(segments) % 2 == 0:
            new_segment.color("#2DF712") # เขียวสด
        else:
            new_segment.color("#096E16") # เขียวหม่นลงนิดหน่อย

        new_segment.penup()
        segments.append(new_segment)
        
        delay -= 0.001
        score += 10
        if score > high_score:
            high_score = score
        update_score()

    # ย้ายหาง
    for index in range(len(segments)-1, 0, -1):
        x = segments[index-1].xcor()
        y = segments[index-1].ycor()
        segments[index].goto(x, y)

    if len(segments) > 0:
        x = head.xcor()
        y = head.ycor()
        segments[0].goto(x,y)

    move()

    # ชนตัวเอง
    for segment in segments:
        if segment.distance(head) < 20:
            wn.bgcolor("#330000") # เอฟเฟกต์จอแดง
            wn.update()
            reset_game()

    time.sleep(delay)

wn.mainloop()