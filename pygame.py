import turtle
import time
import random

delay = 0.1

# --- 1. ตั้งค่าหน้าจอ ---
wn = turtle.Screen()
wn.title("เกมงู (เวอร์ชั่นไม่ต้องลงโปรแกรมเพิ่ม)")
wn.bgcolor("black")
wn.setup(width=600, height=600)
wn.tracer(0) # ปิดการอนิเมชั่นเพื่อความลื่นไหล

# --- 2. ส่วนหัวของงู ---
head = turtle.Turtle()
head.speed(0)
head.shape("square")
head.color("green")
head.penup()
head.goto(0,0)
head.direction = "stop"

# --- 3. อาหาร ---
food = turtle.Turtle()
food.speed(0)
food.shape("circle")
food.color("red")
food.penup()
food.goto(0,100)

segments = []

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
    if head.direction == "up":
        y = head.ycor()
        head.sety(y + 20)

    if head.direction == "down":
        y = head.ycor()
        head.sety(y - 20)

    if head.direction == "left":
        x = head.xcor()
        head.setx(x - 20)

    if head.direction == "right":
        x = head.xcor()
        head.setx(x + 20)

# --- 5. การควบคุมคีย์บอร์ด ---
wn.listen()
wn.onkeypress(go_up, "w")
wn.onkeypress(go_down, "s")
wn.onkeypress(go_left, "a")
wn.onkeypress(go_right, "d")
# ใช้ปุ่มลูกศรด้วย
wn.onkeypress(go_up, "Up")
wn.onkeypress(go_down, "Down")
wn.onkeypress(go_left, "Left")
wn.onkeypress(go_right, "Right")

# --- 6. ลูปหลักของเกม ---
while True:
    wn.update()

    # ตรวจสอบการชนขอบจอ
    if head.xcor()>290 or head.xcor()<-290 or head.ycor()>290 or head.ycor()<-290:
        time.sleep(1)
        head.goto(0,0)
        head.direction = "stop"

        # ลบหางทิ้ง
        for segment in segments:
            segment.goto(1000, 1000)
        segments.clear()
        delay = 0.1

    # ตรวจสอบการกินอาหาร
    if head.distance(food) < 20:
        # ย้ายอาหารไปที่สุ่ม
        x = random.randint(-290, 290)
        y = random.randint(-290, 290)
        food.goto(x,y)

        # เพิ่มความยาวงู
        new_segment = turtle.Turtle()
        new_segment.speed(0)
        new_segment.shape("square")
        new_segment.color("lightgreen")
        new_segment.penup()
        segments.append(new_segment)
        
        # เพิ่มความเร็วเล็กน้อย
        delay -= 0.001

    # ย้ายหางตามหัว
    for index in range(len(segments)-1, 0, -1):
        x = segments[index-1].xcor()
        y = segments[index-1].ycor()
        segments[index].goto(x, y)

    if len(segments) > 0:
        x = head.xcor()
        y = head.ycor()
        segments[0].goto(x,y)

    move()

    # ตรวจสอบการชนตัวเอง
    for segment in segments:
        if segment.distance(head) < 20:
            time.sleep(1)
            head.goto(0,0)
            head.direction = "stop"
            
            for segment in segments:
                segment.goto(1000, 1000)
            segments.clear()
            delay = 0.1

    time.sleep(delay)

wn.mainloop()