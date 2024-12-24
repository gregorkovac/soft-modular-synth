from pyo import *
import pygame
import inspect

from modules.ModuleBase import ModuleBase, Pin, Potentiometer
from modules.VCO import VCO
from modules.MasterOut import MasterOut
from modules.Mixer import Mix
from modules.LFO import LFOModule
from modules.VCF import VCF

from Menu import Menu, Tooltip

from misc.pallete import *
from misc.settings import *

class MasterSynth:
    def __init__(self):
        pygame.init()
        pygame.font.init()

        self.screen = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()

        self.server = Server().boot()
        self.server.start()
        # self.master_out = Mixer(outs=1, chnls=1).out()
        self.connection_A = None
        self.modules = [VCF((100, 100))]
        self.connections = []
        self.hangingConnection = None
        self.movingModule = None
        self.selectedPot = None

        self.menu = Menu(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.tooltip = Tooltip()

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

        # self.modules.append(VCO(pos = (400, 100)))
        # self.modules.append(LFOModule(pos = (100, 100)))
        self.modules.append(MasterOut(pos = (500, 500)))
        # self.modules.append(Mix(pos = (100, 800)))
        # m = ModuleBase()
        # m.draw()

        # self.connect(pin = m.outputs[0], mixer = None)
        # self.connect(pin = 0, mixer = self.master_out)

        while True:
            ## EVENT HANDLING
            click = self.handle_input()

            ## LOGIC
            self.logic(click)

            ## VISUALS
            self.render()

            pygame.display.flip()
            self.clock.tick(30)


    def handle_input(self):
        click = False
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True
            elif event.type == pygame.KEYDOWN:
                if self.movingModule == None:
                    if event.key == pygame.K_1:
                        self.modules.append(VCO(pos = pygame.mouse.get_pos()))
                    elif event.key == pygame.K_2:
                        self.modules.append(Mix(pos = pygame.mouse.get_pos()))
                    elif event.key == pygame.K_3:
                        self.modules.append(LFOModule(pos = pygame.mouse.get_pos()))
                elif event.key == pygame.K_BACKSPACE and self.movingModule[0] != 0:
                        pins_to_disconnect = []
                        idx = self.movingModule[0]
                        for i in range(len(self.modules[idx].pins)):
                            self.modules[idx].pins[i].disconnect()
                            pins_to_disconnect.append(self.modules[idx].pins[i])

                        to_remove = []
                        print(self.movingModule)
                        for i in range(len(self.connections)):
                            print(f" ---> {self.connections[i]}")
                            if self.connections[i][0] in pins_to_disconnect or self.connections[i][1] in pins_to_disconnect:
                                to_remove.append(i)

                        for r in to_remove:
                            self.connections.pop(r)

                        self.modules.pop(idx)
                        self.movingModule = None
            elif event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            
        return click

    def logic(self, click):
        if click:
            click_pos = pygame.mouse.get_pos()
            print("Click")
            click_success = False
            for i in range(len(self.modules)):
                clicked_pin = self.modules[i].check_clicks(click_pos)
                if clicked_pin != None and isinstance(clicked_pin, Pin):
                    click_success = True
                    self.selectedPot = None

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
                elif clicked_pin != None and isinstance(clicked_pin, Potentiometer) and self.selectedPot == None:
                    click_success = True
                    self.selectedPot = (clicked_pin, pygame.mouse.get_pos()[1])
                    break
                elif self.selectedPot != None:
                    click_success = True
                    self.selectedPot = None
                    break

                if self.modules[i].check_move(click_pos) and self.movingModule == None:
                    click_success = True
                    self.movingModule = (i, self.modules[i].get_relative_pos(click_pos))
                    print("Clicked on module")

            menu_click = self.menu.click(click_pos)
            if menu_click != "":
                click_success = True
                self.spawn_module_at_pointer(menu_click, click_pos)

            if not click_success:
                self.hangingConnection = None
                self.movingModule = None
                self.selectedPot = None
                print("Not hanging anymore")

        if self.movingModule != None:
                mouse_pos = pygame.mouse.get_pos()
                self.modules[self.movingModule[0]].pos = (mouse_pos[0] - self.movingModule[1][0], mouse_pos[1] - self.movingModule[1][1])

        if self.selectedPot != None:
            mouse_pos = pygame.mouse.get_pos()
            self.selectedPot[0].move(mouse_pos[1],self.selectedPot[1])


    def render(self):
        self.screen.fill(BACKGROUND_COLOR)  

        for i in range(len(self.modules)):
            self.modules[i].update()
            self.modules[i].draw(self.screen)

        for i in range(len(self.connections)):
            self.draw_connection(self.connections[i][0].get_global_pos(), self.connections[i][1].get_global_pos(), self.connections[i][2])

        if self.hangingConnection != None:
            self.draw_connection(self.hangingConnection.get_global_pos(), pygame.mouse.get_pos(), color = CONNECTION_COLOR)

        if self.selectedPot != None:
            self.tooltip.draw(self.screen, pygame.mouse.get_pos(), self.selectedPot[0].val)

        self.menu.draw(self.screen)

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

    def spawn_module_at_pointer(self, name, click_pos):
        if name == "VCO":
            self.modules.append(VCO(pos = pygame.mouse.get_pos()))
            self.movingModule = (len(self.modules) - 1, self.modules[len(self.modules) - 1].get_relative_pos(click_pos))
        elif name == "LFO":
            self.modules.append(LFOModule(pos = pygame.mouse.get_pos()))
            self.movingModule = (len(self.modules) - 1, self.modules[len(self.modules) - 1].get_relative_pos(click_pos))
        elif name == "Mixer":
            self.modules.append(Mix(pos = pygame.mouse.get_pos()))
            self.movingModule = (len(self.modules) - 1, self.modules[len(self.modules) - 1].get_relative_pos(click_pos))
        elif name == "VCF":
            self.modules.append(VCF(pos = pygame.mouse.get_pos()))
            self.movingModule = (len(self.modules) - 1, self.modules[len(self.modules) - 1].get_relative_pos(click_pos))