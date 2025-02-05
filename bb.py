import pygame
import OpenGL.GL as gl

pygame.init()
pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION, 3)
pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION, 3)
pygame.display.set_mode((800, 600), pygame.OPENGL | pygame.DOUBLEBUF)

print("OpenGL Version:", gl.glGetString(gl.GL_VERSION).decode())

pygame.quit()
