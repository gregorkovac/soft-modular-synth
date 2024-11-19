from pyo import *
import pygame

from modules.ModuleBase import ModuleBase
from modules.VCO import VCO
from modules.MasterOut import MasterOut
from misc.pallete import *

class MasterSynth:
    def __init__(self):
        pygame.init()
        pygame.font.init()

        self.screen = pygame.display.set_mode((720,720))
        self.clock = pygame.time.Clock()

        self.server = Server().boot()
        self.server.start()
        # self.master_out = Mixer(outs=1, chnls=1).out()
        self.connection_A = None
        self.modules = []
        self.connections = []
        self.hangingConnection = None
        self.movingModule = None

    # def on_click(self, event):
    #     if event.button is MouseButton.LEFT:
    #         self.ax.scatter(event.xdata, event.ydata, s=10, color="red")
    #         plt.draw()

    # def update_graphics(self, n):
    #     scat, = plt.scatter(0, 0, s = 50, color = "blue")
    #     return scat, 

    def draw_connection(self, start_pos, end_pos, color):
        pygame.draw.line(self.screen, color, start_pos, end_pos, width = 10)
        pygame.draw.circle(self.screen, color, start_pos, 10)
        pygame.draw.circle(self.screen, color, end_pos, 10)

    def start(self):

        self.modules.append(VCO(pos = (100, 100)))
        self.modules.append(MasterOut(pos = (400, 400)))
        # m = ModuleBase()
        # m.draw()

        # self.connect(pin = m.outputs[0], mixer = None)
        # self.connect(pin = 0, mixer = self.master_out)

        while True:
            ## EVENT HANDLING
            click = False
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    click = True
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    raise SystemExit

            ## LOGIC
            if click:
                click_pos = pygame.mouse.get_pos()
                print("Click")
                click_success = False
                for i in range(len(self.modules)):
                    clicked_pin = self.modules[i].check_clicks(click_pos)
                    if clicked_pin != None:
                        click_success = True

                        idx = None
                        for j in range(len(self.connections)):
                            if self.connections[j][0] == clicked_pin or self.connections[j][1] == clicked_pin:
                                idx = j
                                break
                        
                        if idx != None:
                            self.connections[idx][1].disconnect()
                            self.connections.pop(idx)

                        # self.connect(pin = ret[0], mixer = None)
                        if self.hangingConnection == None:
                            self.hangingConnection = clicked_pin
                            print(f"Hanging: {self.hangingConnection}")
                        else:
                            # self.visualConnections.append((self.hangingConnection, ret[1]))
                            self.connect(clicked_pin)
                            print("Connected")
                        break

                    if self.modules[i].check_move(click_pos) and self.movingModule == None:
                        click_success = True
                        self.movingModule = (i, self.modules[i].get_relative_pos(click_pos))
                        print("Clicked on module")

                if not click_success:
                    self.hangingConnection = None
                    self.movingModule = None
                    print("Not hanging anymore")

            if self.movingModule != None:
                mouse_pos = pygame.mouse.get_pos()
                self.modules[self.movingModule[0]].pos = (mouse_pos[0] - self.movingModule[1][0], mouse_pos[1] - self.movingModule[1][1])

            ## VISUALS
            self.screen.fill(BACKGROUND_COLOR)  

            for i in range(len(self.modules)):
                self.modules[i].draw(self.screen)

            for i in range(len(self.connections)):
                self.draw_connection(self.connections[i][0].get_global_pos(), self.connections[i][1].get_global_pos(), self.connections[i][2])

            # print(self.hangingConnection)
            if self.hangingConnection != None:
                self.draw_connection(self.hangingConnection.get_global_pos(), pygame.mouse.get_pos(), color = (235, 192, 52))


            pygame.display.flip()
            self.clock.tick(30)

    def stop(self):
        self.server.stop()

    def connect(self, pin2):
        if pin2.dir == self.hangingConnection.dir:
            return
        
        if pin2.dir == "in":
            pin_in = pin2
            pin_out = self.hangingConnection
        else:
            pin_out = pin2
            pin_in = self.hangingConnection

        self.connections.append((pin_out, pin_in, (235, 192, 52)))
        
        pin_in.connect(pin_out)

        self.hangingConnection = None
