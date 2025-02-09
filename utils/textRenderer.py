import freetype
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

import numpy as np
class TextRenderer:
    def __init__(self, font_path, font_size):
        self.face = freetype.Face(font_path)
        self.face.set_char_size(font_size * 64)
        self.list_base = glGenLists(128)
        self.texture_ids = []
        
        # Create display lists for first 128 ASCII characters
        for i in range(128):
            self.make_dlist(i)
    
    def make_dlist(self, char):
        # Generate texture for character
        self.face.load_char(chr(char))
        glyph = self.face.glyph
        
        # Generate texture
        tex_id = glGenTextures(1)
        self.texture_ids.append(tex_id)
        glBindTexture(GL_TEXTURE_2D, tex_id)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        
        # Create bitmap
        bitmap = glyph.bitmap
        width = bitmap.width
        height = bitmap.rows
        
        # Pad bitmap data if needed
        data = np.zeros((height, width), dtype=np.ubyte)
        for i in range(height):
            for j in range(width):
                data[i][j] = bitmap.buffer[i * width + j]
        
        glTexImage2D(GL_TEXTURE_2D, 0, GL_ALPHA, width, height, 0,
                    GL_ALPHA, GL_UNSIGNED_BYTE, data)
        
        # Create display list
        glNewList(self.list_base + char, GL_COMPILE)
        
        if width > 0 and height > 0:
            glBindTexture(GL_TEXTURE_2D, tex_id)
            glPushMatrix()
            
            # Account for glyph metrics
            glTranslate(glyph.bitmap_left, glyph.bitmap_top - height, 0)
            
            # Draw textured quad
            glBegin(GL_QUADS)
            glTexCoord2f(0, 0); glVertex2f(0, height)
            glTexCoord2f(0, 1); glVertex2f(0, 0)
            glTexCoord2f(1, 1); glVertex2f(width, 0)
            glTexCoord2f(1, 0); glVertex2f(width, height)
            glEnd()
            
            glPopMatrix()
            glTranslatef(glyph.advance.x >> 6, 0, 0)
        
        glEndList()
    
    def render_text(self, x, y, text):
        glPushMatrix()
        glLoadIdentity()
        glTranslate(x, y, 0)
        glListBase(self.list_base)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glEnable(GL_TEXTURE_2D)
        glCallLists([ord(c) for c in text])
        glDisable(GL_TEXTURE_2D)
        glDisable(GL_BLEND)
        glPopMatrix()
    
    def cleanup(self):
        glDeleteLists(self.list_base, 128)
        glDeleteTextures(self.texture_ids)