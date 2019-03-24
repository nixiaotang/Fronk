from pygame import *

init()
mixer.init()
mixer.music.load('music.mp3')
mixer.music.play(-1)
screen = display.set_mode((970, 600))
w, h = display.get_surface().get_size()

scene = "Menu"
running = True
page = 0

inventories = []
monster = [0, 0, 0, 0]  # brain, eyeball, hand, foot
selected = 0

endtrans = [0, 0]

oneClick = [False, False, False, False]

collected = [2, 0, 0, 0, 0, 0]
# 0 = uncollected, 1 = collected

items = [
   image.load("brain.png"),
   image.load("eyeball.png"),
   image.load("frozen.png"),
   image.load("hand.png"),
   image.load("key.png"),
   image.load("foot.png")
]


def collect(ID, w, h, x, y):
   itSiz = Rect(x, y, w, h)
   items[ID] = transform.scale(items[ID], (w, h))
   screen.blit(items[ID], (x, y))

   if itSiz.collidepoint(mx, my) and mp:
       inventories.append(ID)
       collected[ID] = 1


def arrow(x, y, direc, nextScene):
   global scene

   if direc == 'right':
       arw = image.load("arrow-right.png")
       arw = transform.scale(arw, (50, 100))
       rects = [Rect(x, y, 10, 100), Rect(x + 10, y + 10, 10, 80), Rect(x + 20, y + 20, 10, 60),
                Rect(x + 30, y + 30, 10, 40), Rect(x + 40, y + 40, 10, 20)]
   elif direc == 'left':
       arw = image.load("arrow-left.png")
       arw = transform.scale(arw, (50, 100))
       rects = [Rect(x + 40, y, 10, 100), Rect(x + 30, y + 10, 10, 80), Rect(x + 20, y + 20, 10, 60),
                Rect(x + 10, y + 30, 10, 40), Rect(x, y + 40, 10, 20)]
   elif direc == 'up':
       arw = image.load("arrow-up.png")
       arw = transform.scale(arw, (100, 50))
       rects = [Rect(x, y + 40, 100, 10), Rect(x + 10, y + 30, 80, 10), Rect(x + 20, y + 20, 60, 10),
                Rect(x + 30, y + 10, 40, 10), Rect(x + 40, y, 20, 10)]
   elif direc == 'down':
       arw = image.load("arrow-down.png")
       arw = transform.scale(arw, (100, 50))
       rects = [Rect(x, y, 100, 10), Rect(x + 10, y + 10, 80, 10), Rect(x + 20, y + 20, 60, 10),
                Rect(x + 30, y + 30, 40, 10), Rect(x + 40, y + 40, 20, 10)]

   hi = False;
   for i in range(len(rects)):
       if rects[i].collidepoint(mx, my):
           hi = True

   if hi:
       screen.blit(arw, (x, y))
       if mp:
           scene = nextScene


def menu():
   global scene
   screen.fill((255, 255, 0))
   fronk = image.load("menu.png")
   fronk = transform.scale(fronk, (1100, 600))
   screen.blit(fronk, (0, 0))

   button = Rect(278, 492, 526, 61)
   if button.collidepoint(mx, my) and mp:
       scene = "Bedroom"


def bedroom():
   global scene

   # backgroundcabDoor
   bkg = image.load("bedroom.png")
   bkg2 = image.load("bedroom2.png")
   bkg = transform.scale(bkg, (800, 600))
   bkg2 = transform.scale(bkg2, (800, 600))
   screen.blit(bkg2, (0, 0))

   if oneClick[0] and collected[3] == 0:
       collect(3, 50, 60, 330, 130)

   # painting
   pnt = Rect(250, 100, 250, 100)
   if not oneClick[0]:
       screen.blit(bkg, (0, 0))
       if pnt.collidepoint(mx, my) and mp:
           crash_sound = mixer.Sound("Breaking.ogg")
           crash_sound.play()
           oneClick[0] = True

   # key
   if collected[4] == 0:
       collect(4, 130, 130, 50, 500)

   arrow(740, 230, 'right', "Kitchen")
   arrow(350, 540, 'down', "Bathroom")


def bathroom():
   global scene

   bkg = image.load("bathroom.png")
   bkg = transform.scale(bkg, (800, 600))
   screen.blit(bkg, (0, 0))

   if collected[5] == 0:
       collect(5, 80, 60, 650, 310)

   arrow(350, 10, 'up', "Bedroom")


def kitchen():
   global scene

   bkg = image.load("kitchen.png")
   bkg = transform.scale(bkg, (800, 600))
   screen.blit(bkg, (0, 0))

   if oneClick[2] and collected[2] == 0:
       collect(2, 130, 130, 140, 130)

   # fridge
   frig = Rect(90, 130, 230, 140)
   if not oneClick[2]:
       fridDoor = image.load("fridge-door.png")
       fridDoor = transform.scale(fridDoor, (240, 160))
       screen.blit(fridDoor, (90, 120))

       if frig.collidepoint(mx, my) and mp:
           oneClick[2] = True

   # cabinet
   cab = Rect(680, 100, 30, 50)
   if not oneClick[1]:
       cabDoor = image.load("cabinet.png")
       cabDoor = transform.scale(cabDoor, (130, 190))
       screen.blit(cabDoor, (610, 0))

       if len(inventories) > page * 3 + selected and cab.collidepoint(mx, my) and mp and inventories[page * 3 + selected] == 4:
           oneClick[1] = True
           inventories.remove(inventories[page * 3 + selected])
   else:
       if collected[1] == 0:
           collect(1, 90, 90, 640, 40)

   # oven
   if collected[0] == 0:
       collect(0, 130, 110, 420, 340)
   ovenCol = Rect(374, 346, 231, 120)
   if len(inventories) > page * 3 + selected and ovenCol.collidepoint(mx, my) and mp and inventories[page * 3 + selected] == 2:
       inventories.remove(inventories[page * 3 + selected])
       collected[0] = 0;


   arrow(10, 220, 'left', "Bedroom")
   arrow(330, 530, 'down', "Living Room")


def livingRoom():
   global scene

   # background
   bkg = image.load("living-room.png")
   bkg = transform.scale(bkg, (800, 600))
   screen.blit(bkg, (0, 0))

   # monster
   monstSiz = Rect(553, 86, 210, 465)
   if len(inventories) > page * 3 + selected and monstSiz.collidepoint(mx, my) and mp:
       if inventories[page * 3 + selected] == 0:
           monster[0] = True
           inventories.remove(inventories[page * 3 + selected])
       elif inventories[page * 3 + selected] == 1:
           monster[1] = True
           inventories.remove(inventories[page * 3 + selected])
       elif inventories[page * 3 + selected] == 3:
           monster[2] = True
           inventories.remove(inventories[page * 3 + selected])
       elif inventories[page * 3 + selected] == 5:
           monster[3] = True
           inventories.remove(inventories[page * 3 + selected])

   if monster[0]:
       screen.blit(items[0], (600, 100))
   if monster[1]:
       screen.blit(items[1], (630, 120))
   if monster[2]:
       screen.blit(items[3], (720, 370))
   if monster[3]:
       screen.blit(items[5], (680, 500))

   arrow(350, 10, 'up', "Kitchen")


def end():
   screen.fill((0, 0, 0))
   # background
   bkg = image.load("end.png")
   bkg2 = image.load("gameover.png")
   bkg = transform.scale(bkg, (800, 600))
   bkg2 = transform.scale(bkg2, (800, 600))
   screen.blit(bkg, (0, 0))

   endtrans[1] += 1

   if (endtrans[1] >= 50):
       screen.blit(bkg2, (0, 0))


while running:
   mp = False
    
   for e in event.get():
       if e.type == QUIT:
           running = False
       elif e.type == MOUSEBUTTONDOWN:
           if e.button == 1:
               mp = True

   screen.fill((0, 0, 0))
   mx, my = mouse.get_pos()

   if monster[0] == 1 and monster[1] == 1 and monster[2] == 1 and monster[3] == 1:
       endtrans[0] += 1

       if endtrans[0] == 30:
           scene = "End"

   # scenes
   if scene == 'Menu':
       menu()
   elif scene == 'Bedroom':
       bedroom()
   elif scene == 'Bathroom':
       bathroom()
   elif scene == 'Kitchen':
       kitchen()
   elif scene == 'Living Room':
       livingRoom()
   elif scene == 'End':
       end()

   # inventory
   if not scene == 'Menu' and not scene == 'End':
       inv = image.load("inventory.png")
       selec = image.load("selected.png")
       up = image.load("page-up.png")
       down = image.load("page-down.png")
       inv = transform.scale(inv, (170, 170))
       selec = transform.scale(selec, (170, 170))
       up = transform.scale(up, (170, 90))
       down = transform.scale(down, (170, 90))

       for i in range(3):
           if i == selected % 3:
               screen.blit(selec, (800, i * 170))
           else:
               screen.blit(inv, (800, i * 170))

       if not page:
           a = 3
           if len(inventories) < 3:
               a = len(inventories)
           for i in range(a):
               screen.blit(items[inventories[i]], (820, 20 + i * 170))

           screen.blit(down, (800, 510))
           if mp and mx > 800 and my > 510:
               page = True
       else:
           a = 0
           if len(inventories) > 3:
               a = 1
           for i in range(a):
               screen.blit(items[inventories[3 + i]], (820, 20 + i * 170))

           screen.blit(up, (800, 510))
           if mp and mx > 800 and my > 510:
               page = False

       if mp and mx >= 810:
           if my <= 160:
               selected = 0
           elif my < 320:
               selected = 1
           elif my < 480:
               selected = 2

   display.flip()

quit()

