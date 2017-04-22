#!/usr/bin/python
# Mancala.py
"""
    Copyright (C) 2011  Peter Hewitt

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

"""
import g,pygame,utils,gtk,sys,buttons,load_save
import manc

class Mancala:

    def __init__(self):
        self.journal=True # set to False if we come in via main()
        self.canvas=None # set to the pygame canvas if we come in via activity.py

    def display(self):
        g.screen.fill((0,255,255))
        utils.display_number(g.player,g.player_c,g.font3,utils.ORANGE)
        utils.display_number1(g.wizard,g.wizard_lc,g.font3,utils.ORANGE)
        img=g.xo_grey
        if g.state in (1,2,3): img=g.xo
        g.screen.blit(img,g.xo_xy)
        img=g.magician_grey
        if g.state in (4,5,6): img=g.magician
        g.screen.blit(img,g.magician_xy)
        buttons.draw()
        self.manc.draw()

    def do_click(self):
        if g.state==1: self.manc.click()
    
    def update(self):
        self.manc.do_anims()
        if g.state in (2,3):
            self.manc.player_update()
        elif g.state==4:
            pygame.time.delay(1000)
            dish=self.manc.wizard_move()
            if dish==0: g.state=1
            else: self.manc.wizard_click(dish)
        elif g.state in (5,6):
            self.manc.wizard_update()
        if g.state==1 and not self.manc.player_ok(): g.state=4
        elif g.state==4 and not self.manc.wizard_ok(): g.state=1
        
    def do_button(self,bu):
        if bu=='new': self.manc.setup()

    def do_key(self,key0):
        if key0==263 or key0==32: self.do_button('new'); return
        if g.state==1:
            for key in range(49,55):
                if key0==key:
                    self.manc.do_click(key-48); self.manc.set_mouse();return
            if key0 in (259,pygame.K_x): # cross,x
                self.manc.do_click(self.manc.dish_n); return
            if key0==262 or key0==275: #right
                self.manc.dish_n+=1
                if self.manc.dish_n==7: self.manc.dish_n=1
                self.manc.set_mouse()
                return
            if key0 in (260,276): #left
                self.manc.dish_n-=1
                if self.manc.dish_n==0: self.manc.dish_n=6
                self.manc.set_mouse()
                return

    def buttons_setup(self):
        buttons.Button('new',(g.sx(30),g.sy(2)))

    def run(self):
        g.init()
        if not self.journal: utils.load()
        self.manc=manc.Manc()
        self.manc.setup()
        load_save.retrieve()
        self.buttons_setup()
        going=True
        while going:
            # Pump GTK messages.
            while gtk.events_pending():
                gtk.main_iteration()

            # Pump PyGame messages.
            for event in pygame.event.get():
                if event.type==pygame.QUIT: # only in standalone version
                    if not self.journal: utils.save()
                    going=False
                elif event.type == pygame.MOUSEMOTION:
                    g.pos=event.pos
                    self.manc.check_mouse()
                    g.redraw=True
                    if self.canvas<>None: self.canvas.grab_focus()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    g.redraw=True
                    if event.button==2: # centre button
                        if not self.journal:
                            g.version_display=not g.version_display
                    if event.button==1:
                        bu=buttons.check()
                        if bu!='': self.do_button(bu)
                        else: self.do_click()
                elif event.type == pygame.KEYDOWN:
                    self.do_key(event.key); g.redraw=True
            if not going: break
            self.update()
            if g.redraw:
                self.display()
                if not self.journal: # not on XO
                    if g.version_display: utils.version_display()
                g.screen.blit(g.pointer,g.pos)
                pygame.display.flip()
                g.redraw=False
            g.clock.tick(40)

if __name__=="__main__":
    pygame.init()
    pygame.display.set_mode((800,600))
    game=Mancala()
    game.journal=False
    game.run()
    pygame.display.quit()
    pygame.quit()
    sys.exit(0)
