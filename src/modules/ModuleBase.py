from pyo import *
import matplotlib.pyplot as plt
import pygame
from misc.pallete import *
import numpy as np

def pixels_to_small_float(val):
    """
    pixel_to_small_float converts pixel to a float in [0, 1];
        used for potentiometers

    args
        val (int) - pixel value

    returns
        val (float) - the small float
    """
    val = val / 100.0
    if val < 0:
        val = 0
    if val > 1:
        val = 1

    return val

class Pin:
    """
    Pin is a class used for all module pins
    """
    def __init__(self, name, module, direction, position, parent, in_channel = 0):
        # Name of the pin
        self.name = name

        # Parent module
        self.module = module

        # Pin direction 
        # Either "in" for input, "out" for output or "pass" for processing (like the filter)
        self.dir = direction

        # Pin position relative to the module
        self.pos = position

        # Parent module object
        self.parent = parent

        # Input channel
        self.in_channel = in_channel

        # Another pin that it is connected to
        self.connected_to = None

    def draw(self, surface, font):
        """
        draw draws the pin

        args
            surface (Surface) - the main drawing surface
            font (Font) - font object for drawing text
        """

        pos = self.get_global_pos()
        pygame.draw.circle(surface, MODULE_PIN_COLOR, pos, 20)
        pygame.draw.circle(surface, MODULE_PIN_COLOR_INSIDE, pos, 10)
        text_surface = font.render(self.name, False, TEXT_COLOR)
        surface.blit(text_surface, (pos[0] - 20, pos[1] + 20))

    def connect(self, pin):
        """
        connect connects this pin to another pin

        args
            pin (Pin) - other pin
        """

        # Don't allow the custom connection
        if isinstance(pin.module, CustomConnection):
            return

        # If the other pin has "pass" direction, connect from that side (due to Pyo specifications)
        if pin.dir == "pass":
            pin.connect(self)
        elif self.dir == "pass":
            # Connect the other pin's output to this pin's module's input
            self.module.setInput(pin.module)
        else:
            # Reset connections
            self.disconnect()

            # Add the other pin as an input
            self.module.addInput(self.in_channel, pin.module)

            # Set the amplitude to 1
            self.module.setAmp(self.in_channel, 0, 1)

        # Log the connection
        self.connected_to = pin
    
    def disconnect(self):
        """
        disconnect disconnects a connection
        """
    
        if self.connected_to == None:
            return

        if self.dir == "in":
            # Delete an input
            self.module.delInput(self.in_channel)
        elif self.dir == "out" and self.connected_to != None:
            # Call disconnect on other pin
            self.connected_to.disconnect()
            self.connected_to = None
        elif self.dir == "pass":
            # Set a dummy sine wave with amplitude 0 as input
            self.module.setInput(Sine(0, 0))

    def get_global_pos(self):
        """
        get_global_pos returns the pin's global position

        returns
            (int) - global position relative to the parent module
        """
        return (self.pos[0] + self.parent.pos[0], self.pos[1] + self.parent.pos[1])
    
class PinModifier(Pin):
    """
    PinModifier is a child class of Pin that is used for modifying attributes
    """

    def __init__(self, name, module, direction, position, parent, attribute, in_channel = 0):
        super().__init__(name, module, direction, position, parent, in_channel)

        # The module attribute we are modifying
        self.attr = attribute

        # The old attribute value
        self.oldVal = getattr(self.module, self.attr.split("_")[0])

    def connect(self, pin):
        """
        connect connects a this pin to another pin

        args
            pin (Pin) - other pin
        """

        if isinstance(pin.module, CustomConnection):
            self.connected_to = pin
            return
        
        if isinstance(self.module, CustomConnection):
            pin.connect(self)
            return

        # Save the old value
        self.oldVal = getattr(self.module, self.attr.split("_")[0])

        # Handle different value ranges
        if self.attr == "mul":
            pin.module.mul = 1
            pin.module.add = 0
        elif self.attr == "freq":
            pin.module.mul = 100
            pin.module.add = 0
        elif self.attr == "freq_filt":
            pin.module.mul = 1000
            pin.module.add = 400
        
        # Set the attribute
        setattr(self.module, self.attr.split("_")[0], pin.module)

        # Log the connection
        self.connected_to = pin

    def disconnect(self):   
        """
        disconnect disconnects a connection
        """

        # Reset attribute value
        setattr(self.module, self.attr.split("_")[0], self.oldVal)

        # Disconnect the other pin
        if self.connected_to != None:
            self.connected_to.disconnect()
            self.connected_to = None

class Potentiometer:
    """
    Potentiometer is used for manually controlling parameters
    """
    def __init__(self, name, position, parent, default_value, min_value = 0, max_value=1):

        # Name of the potentiometer
        self.name = name

        # Relative position to the parent module
        self.pos = position

        # Parent module
        self.parent = parent

        # Parameter value
        self.val = default_value

        # Minimum value
        self.min_val = min_value

        # Maximum value
        self.max_val = max_value

    def draw(self, surface, font):
        """
        draw draws the potentiometer

        args
            surface (Surface) - the main drawing surface
            font (Font) - font object for drawing text
        """

        pos = self.get_global_pos()

        # Draw the circle
        pygame.draw.circle(surface, MODULE_PIN_COLOR, pos, 30)

        # Compute the angle
        angle = np.interp(self.val, [self.min_val, self.max_val], [0, 3/2 * np.pi]) + 3 / 4 * np.pi

        # Draw the line
        line_length = 20
        end_x = pos[0] + line_length * np.cos(angle)
        end_y = pos[1] + line_length * np.sin(angle)
        pygame.draw.line(surface, (1, 1, 1), pos, (end_x, end_y), 2)

        # Draw the text
        text_surface = font.render(self.name, False, TEXT_COLOR)
        surface.blit(text_surface, (pos[0] - 20, pos[1] + 25))

    def get_global_pos(self):
        """
        get_global_pos returns the pin's global position

        returns
            (int) - global position relative to the parent module
        """

        return (self.pos[0] + self.parent.pos[0], self.pos[1] + self.parent.pos[1])

    def move(self, val, zero_val):
        """
        move moves the potentiometer based on the mouse y position

        args
            val (int) - the current pixel value
            zero_val (int) - the pixel value when we first click on the potentiometer
        """

        self.val = float(np.interp(pixels_to_small_float(zero_val - val), [0, 1], [self.min_val, self.max_val]))

class CustomConnection:
    """
    CustomConnection serves as a custom connection for when Pyo doesn't provide a connection of some sort
    """

    def __init__(self, initial_value=0):

        # The internal value of the connection
        self.value = initial_value

class Indicator:
    """
    Indicator LED for showing values
    """

    def __init__(self, pos, parent, min_val, max_val):
        self.pos = pos
        self.parent = parent
        self.val = min_val
        self.max_val = max_val
        self.min_val = min_val

    def draw(self, surface):
        """
        draw draws the potentiometer

        args
            surface (Surface) - the main drawing surface
            font (Font) - font object for drawing text
        """

        # Get position
        pos = self.get_global_pos()

        # Set LED intensity based on value
        p = np.interp(self.val, [self.min_val, self.max_val], [0, 1])
        color = (INDICATOR_ON_COLOR[0] * p + INDICATOR_OFF_COLOR[0] * (1 - p),
                 INDICATOR_ON_COLOR[1] * p + INDICATOR_OFF_COLOR[1] * (1 - p),
                 INDICATOR_ON_COLOR[2] * p + INDICATOR_OFF_COLOR[2] * (1 - p))

        # Draw the circle
        pygame.draw.circle(surface, color, pos, 10)


    def get_global_pos(self):
        """
        get_global_pos returns the pin's global position

        returns
            (int) - global position relative to the parent module
        """

        return (self.pos[0] + self.parent.pos[0], self.pos[1] + self.parent.pos[1])


class ModuleBase:
    """
    ModuleBase serves as a base for all modules
    """

    def __init__(self, pos, size):

        # Size in pixels as (width, height)
        self.size = size

        # Position in pixels as (x, y)
        self.pos = pos

        # Pins list
        self.pins = []

        # Potentiometers list
        self.potentiometers = []

        # Indicator list
        self.indicators = []

        # Name
        self.name = "Base Module"

        # Font
        self.font = pygame.font.SysFont('menlo', 24)

        # Small font
        self.font_small = pygame.font.SysFont('menlo', 20)
        
    def draw(self, surface):
        """
        draw draws the module

        args
            surface (Surface) - the main drawing surface
        """

        # Draw the rectangle
        pygame.draw.rect(surface, MODULE_BASE_COLOR, pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1]))
        
        # Draw the pins
        for i in range(len(self.pins)):
            self.pins[i].draw(surface, self.font_small)

        # Draw the potentiometers
        for i in range(len(self.potentiometers)):
            self.potentiometers[i].draw(surface, self.font)

        # Draw the indicators
        for i in range(len(self.indicators)):
            self.indicators[i].draw(surface)

    def check_clicks(self, pos):
        """
        check_clicks checks for clicks on pins and potentiometers

        args
            pos (tuple) - click position in pixels

        returns
            (Pin / Potentiometer / None) - the clicked object
        """

        # Iterate over pins
        for i in range(len(self.pins)):
            # Get pin position
            pinpos = self.pins[i].get_global_pos()

            # Check for clicks inside pin
            if np.abs(pos[0] - pinpos[0]) < 30 and np.abs(pos[1] - pinpos[1]) < 30:
                return self.pins[i]
            
        # Iterate over potentiometers
        for i in range(len(self.potentiometers)):
            # Get potentiometer position
            pinpos = self.potentiometers[i].get_global_pos()

            # Check for clicks inside potentiometer
            if np.abs(pos[0] - pinpos[0]) < 40 and np.abs(pos[1] - pinpos[1]) < 40:
                return self.potentiometers[i]

        # Return None if no click was found
        return None
    
    def check_move(self, pos):
        """
        check_move checks for clicks on module for moving

        args
            pos (tuple) - click position in pixels

        returns
            (bool) - if click was detected or not
        """

        # Check if clik is inside the module
        if self.pos[0] < pos[0] < self.pos[0] + self.size[0] and self.pos[1] < pos[1] < self.pos[1] + self.size[1]:
            return True
        return False
    
    def get_relative_pos(self, pos):
        """
        get_relative_pos returns relative position of mouse to the module

        args
            pos (tuple) - position in pixels
        """

        return (pos[0] - self.pos[0], pos[1] - self.pos[1])
    
    def update(self):
        """
        update is a template function for updating module parameters
        """
        pass

