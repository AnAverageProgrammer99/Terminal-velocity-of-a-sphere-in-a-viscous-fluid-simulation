import numpy as np
import matplotlib.pyplot as plt
import pygame as pg
import time

pf_water = 997
u_water = 0.001
pf_oliveoil = 900
u_oliveoil = 0.084
pf_goldensyrup = 1430
u_golensyrup = 210
pf_ketchup = 1092
u_ketchup = 50
pb_aluminium = 2730
pb_steel = 9870
pb_rubber = 1350
pb_platinum = 21450

fluid_material = int(input('''
1-Water
2-Olive Oil
3-Golden Syrup
4-Ketchup
'''))
while fluid_material not in (1, 2, 3,4):
    fluid_material = int(input('''
1-Water
2-Olive Oil
3-Golden Syrup
4-Ketchup
'''))

sphere_material = int(input('''
1-Steel
2-Aluminium
3-Rubber
4-Platinum
'''))
while sphere_material not in (1, 2, 3, 4):
    sphere_material = int(input('''
1-Steel
2-Aluminium
3-Rubber
4-Platinum
'''))

screen = pg.display.set_mode(size=(500, 870))
pg.display.init()
pg.font.init()
screen.fill((255, 255, 255))
fluid = pg.Rect(0, 100, 500, 770)
left = pg.Rect(0, 90, 5, 780)
right = pg.Rect(495, 90, 5, 780)
bottom = pg.Rect(0, 863, 500, 7)
v_myfont = pg.font.SysFont("monospace", 20)  # font of text on screen
s_myfont = pg.font.SysFont("monospace", 25)  # font of text on screen
dt_myfont = pg.font.SysFont("monospace", 20)
db_myfont = pg.font.SysFont("monospace", 15)
vs_myfont = pg.font.SysFont("monospace", 15)
sc_myfont = pg.font.SysFont("monospace", 15)

if fluid_material == 1:
    pf = pf_water
    u = u_water
    fluid_colour = (0, 255, 255,)
elif fluid_material == 2:
    pf = pf_oliveoil
    u = u_oliveoil
    fluid_colour = (223, 216, 85)
elif fluid_material == 3:
    pf = pf_goldensyrup
    u = u_golensyrup
    fluid_colour = (230, 180, 0)
elif fluid_material == 4:
    pf = pf_ketchup
    u = u_ketchup
    fluid_colour = (187, 43, 27)
if sphere_material == 1:
    ps = pb_steel
elif sphere_material == 2:
    ps = pb_aluminium
elif sphere_material == 3:
    ps = pb_rubber
elif sphere_material == 4:
    ps = pb_platinum

g = 9.81  # acceleration due to gravity (m/s*2)
# pf: density of liquid (kg/m^3)
# ps: density of sphere (kg/m^3)
# u: viscosity of liquid (Pa s)

# customizable
db = 0.08  # diameter of sphere (m)
total_time = 2.5  # seconds
TP = 0.001  # amount of time between each measurement being taken
vis_speed = 1
scale = 0.008  # 1 pixel = n metres

K = db *((g*pf*(ps-pf))/u**2)**(1/3) # K value
if 43.3 < K < 2360:
    pass
else: 
    print("K value out of range") # printing an error and stopping the program if the K value is out of range
    quit()

db_label = db_myfont.render("Ball Diameter: "+str(db)+"m", 1, (0, 0, 0))
screen.blit(db_label, (0, 0))
vs_label = vs_myfont.render("Visualization Speed: "+str(vis_speed)+"x", 1, (0, 0, 0))
screen.blit(vs_label, (0, 20))
sc_label = sc_myfont.render("Scale: 1 pixel = "+str(scale)+"m", 1, (0, 0, 0))
screen.blit(sc_label, (0, 40))

t_distance = round(770 * scale, 5)
iterations = total_time / TP
iterations = int(iterations)
delay = TP / vis_speed

s_text = str(t_distance)
s_label = s_myfont.render("Fluid Depth: "+s_text+"m", 1, (0, 0, 0))

radius = (db/2) / scale  # radius of the sphere in pixels on screen

vList = []
tList = []
aList = []
dList = []

t = 0  # time elapsed
v = 0  # velocity
d = 0  # distance travelled

r = 0.5 * db  # radius of sphere
vol = (4 / 3) * np.pi * (r ** 3)  # volume of sphere
A = np.pi * (r ** 2)  # cross-sectional area of sphere

m = vol * ps  # mass
Fu = pf * vol * g  # upthrust

for i in range(iterations):  # initializing the loop - number in brackets is the number of iterations
    by = d / scale  # number of pixels the sphere has travelled

    pg.draw.rect(screen, fluid_colour, fluid)
    screen.blit(s_label, (10, 830))
    pg.draw.rect(screen, (0, 0, 0), left)
    pg.draw.rect(screen, (0, 0, 0), right)
    pg.draw.rect(screen, (0, 0, 0), bottom)
    round_v = round(v, 5)  # round velocity to 5 d.p for visualization
    tv = str(round_v)  # convert velocity from a float to a string so it can be shown on screen

    if len(tv) < 7:
        tv = tv+"0"
    v_text = tv + "m/s"

    v_label = v_myfont.render(v_text, 1, (0, 0, 0))
    screen.blit(v_label, (275, 100+by))  # showing the velocity of the sphere on screen in real time

    pg.draw.circle(screen, (0, 0, 0), (250, 100+radius+by), radius)  # drawing the sphere's position every iteration

    pg.display.update()

    Fd = 0.5 * 0.44 * A * pf * (v ** 2)  # Drag | 0.44 is the approximate drag coefficient of a sphere
    # This means the program only works for K values between 43.3 and 2360
    a = ((m * g) - Fu - Fd) / m  # rearranged F = ma
    v = v + (a * TP)  # v = u + at
    s = v * TP - 0.5 * a * TP ** 2
    d = d + s  # total distance travelled
    t = t + TP  # incrementing the time by the time period every iteration so the graph can be plotted against time
    tList.append(t)
    vList.append(v)
    aList.append(a)
    # print(round(t,5),"s","|  Acceleration: ",round(a,5),"| Velocity: ",round(v,5),"| Distance: ",round(d,5))

    time.sleep(delay)

d_text = str(round(d, 5))
t_text = str(total_time)
dt_label = dt_myfont.render("Sphere travelled "+d_text+"m in "+t_text+"s", 1, (0, 0, 0))
screen.blit(dt_label, (50, 75 + by - radius))
pg.display.update()

print("Terminal Velocity:\n", v, "m/s")  # Final answer

plt.xlabel("Time (s)")  # x axis
plt.ylabel("Blue:Velocity(m/s) | Orange:Acceleration(m/s^2)")  # y axis
plt.plot(tList, vList, linewidth=0.75)
plt.plot(tList, aList, linewidth=0.75)

plt.grid()
plt.show()
