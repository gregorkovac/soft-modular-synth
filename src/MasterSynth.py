from pyo import *
import pygame

from modules.ModuleBase import Pin, Potentiometer
from modules.VCO import VCO
from modules.MasterOut import MasterOut
from modules.Mixer import Mix
from modules.LFO import LFOModule
from modules.VCF import VCF
from modules.Sequencer import Sequencer

from Menu import Menu, Tooltip

from misc.pallete import *
from misc.settings import *

class MasterSynth:
    """
    Master synth contains all code for the application.
    """
    def __init__(self):
        # Initialize pygame
        pygame.init()
        pygame.font.init()

        # Initialize screem
        self.screen = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))

        # Initialize clock
        self.clock = pygame.time.Clock()

        # Start the PYO server
        self.server = Server().boot()
        self.server.start()
        
        # Initialize list of modules
        self.modules = []

        # Initialize list of connection
        self.connections = []

        # Initialize the hanging connection (after we click on one pin and are connecting)
        self.hangingConnection = None

        # Initialize the module we are currently moving
        self.movingModule = None

        # Initialize the potentiometer we are currently chaning
        self.selected_pot = None

        # Initialize menu
        self.menu = Menu(WINDOW_WIDTH, WINDOW_HEIGHT)

        # Initialize the mouse tooltip
        self.tooltip = Tooltip()

    def draw_connection(self, start_pos, end_pos, color):
        """
        draw_connection draws a connection cable between two points

        args
            start_pos (tuple) - first point
            end_pos (tuple) - second point
            color (tuple) - cable color
        """
        pygame.draw.line(self.screen, color, start_pos, end_pos, width = 10)
        pygame.draw.circle(self.screen, color, start_pos, 10)
        pygame.draw.circle(self.screen, color, end_pos, 10)

    def start(self):
        """
        start starts running the application
        """

        # Add master output to the list of modules
        self.modules.append(MasterOut(pos = (WINDOW_WIDTH - 320, 100)))

        # Main loop
        while True:
            # Handle inputs
            click = self.handle_input()

            ## Handle logic
            self.logic(click)

            ## Render
            self.render()

            # Tick
            pygame.display.flip()
            self.clock.tick(FPS)


    def handle_input(self):
        """
        handle_input handles all user inputs

        returns
            click (bool) - if a click event was detected
        """

        click = False

        # Iterate over PyGame events
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True
            elif event.type == pygame.KEYDOWN:
                # Handle module deletion
                if event.key == pygame.K_BACKSPACE and self.movingModule != None and self.movingModule[0] != 0:
                        pins_to_disconnect = []

                        # Find the index of the module we are moving
                        idx = self.movingModule[0]

                        # Disconnect pins
                        for i in range(len(self.modules[idx].pins)):
                            self.modules[idx].pins[i].disconnect()
                            pins_to_disconnect.append(self.modules[idx].pins[i])

                        # Remove connections
                        to_remove = []
                        for i in range(len(self.connections)):
                            if self.connections[i][0] in pins_to_disconnect or self.connections[i][1] in pins_to_disconnect:
                                to_remove.append(i)
                        for r in to_remove:
                            self.connections.pop(r)

                        # Remove the module
                        self.modules.pop(idx)
                        self.movingModule = None
            elif event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            
        return click

    def logic(self, click):
        """
        logic handles all application logic

        args
            click (bool) - if a click was detected or not
        """
        if click:
            # Get click position
            click_pos = pygame.mouse.get_pos()

            # If we successfuly clicked on an interactible object
            click_success = False

            # Iterate over modules
            for i in range(len(self.modules)):
                # Check for click on all objects
                clicked_obj = self.modules[i].check_clicks(click_pos)

                # If we clicked on a pin
                if clicked_obj != None and isinstance(clicked_obj, Pin):
                    click_success = True
                    self.selected_pot = None

                    # Iterate over connections
                    idx = None
                    for j in range(len(self.connections)):
                        # Check if connection to the pin exists
                        if self.connections[j][0] == clicked_obj or self.connections[j][1] == clicked_obj:
                            idx = j
                            break
                        
                    # Disconnect if a connection exists
                    if idx != None:
                        self.connections[idx][1].disconnect()
                        self.connections.pop(idx)

                    if self.hangingConnection == None:
                        # Create a hanging connection
                        self.hangingConnection = clicked_obj
                    else:
                        # Connect
                        try:
                            self.connect(clicked_obj)
                        except:
                            self.hangingConnection = None
                    break
                # If we click on a potentiometer
                elif clicked_obj != None and isinstance(clicked_obj, Potentiometer) and self.selected_pot == None:
                    click_success = True

                    # Save the selected potentiometer and the y mouse coordinate
                    self.selected_pot = (clicked_obj, pygame.mouse.get_pos()[1])
                    break
                elif self.selected_pot != None:
                    # Unselect the potentiometer
                    click_success = True
                    self.selected_pot = None
                    break

                # Check for clicks on module for moving
                if self.modules[i].check_move(click_pos) and self.movingModule == None:
                    click_success = True
                    self.movingModule = (i, self.modules[i].get_relative_pos(click_pos))

            # Check for clicks on the menu
            menu_click = self.menu.click(click_pos)
            if menu_click != "":
                click_success = True
                
                # Spawn a new module
                self.spawn_module_at_pointer(menu_click, click_pos)

            # If no click was detected, reset everything
            if not click_success:
                self.hangingConnection = None
                self.movingModule = None
                self.selected_pot = None

        if self.movingModule != None:
            # Move the selected module
            mouse_pos = pygame.mouse.get_pos()
            self.modules[self.movingModule[0]].pos = (mouse_pos[0] - self.movingModule[1][0], mouse_pos[1] - self.movingModule[1][1])

        if self.selected_pot != None:
            # Move the selected potentiometer
            mouse_pos = pygame.mouse.get_pos()
            self.selected_pot[0].move(mouse_pos[1],self.selected_pot[1])


    def render(self):
        """
        render handles all drawing
        """

        # Fill the background
        self.screen.fill(BACKGROUND_COLOR)  

        # Draw modules
        for i in range(len(self.modules)):
            self.modules[i].update()
            self.modules[i].draw(self.screen)

            if self.selected_pot == None:
                # Draw hover tooltip
                h = self.modules[i].check_hover(pygame.mouse.get_pos())
                if h != None:
                    self.tooltip.draw(self.screen, pygame.mouse.get_pos(), h)

        # Draw connections
        for i in range(len(self.connections)):
            self.draw_connection(self.connections[i][0].get_global_pos(), self.connections[i][1].get_global_pos(), self.connections[i][2])

        # Draw hanging connections
        if self.hangingConnection != None:
            self.draw_connection(self.hangingConnection.get_global_pos(), pygame.mouse.get_pos(), color = CONNECTION_COLOR)

        # Draw the tooltip
        if self.selected_pot != None:
            self.tooltip.draw(self.screen, pygame.mouse.get_pos(), self.selected_pot[0].get_tooltip_val())

        # Draw the menu
        h = self.menu.draw(self.screen)
        if h != None:
            self.tooltip.draw(self.screen, pygame.mouse.get_pos(), h)

        self.tooltip.draw(self.screen, (10, WINDOW_HEIGHT - 200), "Interact with buttons, pins, potentiometers by clicking/double clicking. Connect pins. Have fun!")

    def stop(self):
        """
        stop stops the Pyo server
        """
        self.server.stop()

    def connect(self, pin2):
        """
        connect connects the hanging pin and the newly selected pin

        args
            pin2 (Pin) - the newly selected pin
        """

        # Don't allow input to input and output to output connections
        if pin2.dir == self.hangingConnection.dir:
            return
        
        # Check the directions of the pins
        if pin2.dir == "in" or pin2.dir == "pass":
            pin_in = pin2
            pin_out = self.hangingConnection
        else:
            pin_out = pin2
            pin_in = self.hangingConnection

        # Add the new connection
        self.connections.append((pin_out, pin_in, CONNECTION_COLOR))

        # Connect the pins
        pin_in.connect(pin_out)

        # Reset the hanging connection
        self.hangingConnection = None

    def spawn_module_at_pointer(self, name, click_pos):
        """
            spawn_module_at_pointer creates a new module at the mouse position

            args
                name (str) - the module name
                click_pos (tuple) - position of the click
        """
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
        elif name == "Sequencer":
            self.modules.append(Sequencer(pos = pygame.mouse.get_pos()))
            self.movingModule = (len(self.modules) - 1, self.modules[len(self.modules) - 1].get_relative_pos(click_pos))