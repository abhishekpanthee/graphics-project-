from OpenGL.GL import *


def load_shader(shader_path, shader_type):
    """Load and compile a shader from a file"""
    with open(shader_path, 'r') as file:
        shader_code = file.read()

    shader = glCreateShader(shader_type)
    glShaderSource(shader, shader_code)
    glCompileShader(shader)

    if glGetShaderiv(shader, GL_COMPILE_STATUS) != GL_TRUE:
        print(glGetShaderInfoLog(shader).decode())
        raise RuntimeError(f"Shader compilation failed: {shader_path}")
    
    return shader


def create_shader_program(vertex_shader_path, fragment_shader_path):
    """Create shader program using vertex and fragment shaders"""
    vertex_shader = load_shader(vertex_shader_path, GL_VERTEX_SHADER)
    fragment_shader = load_shader(fragment_shader_path, GL_FRAGMENT_SHADER)

    shader_program = glCreateProgram()
    glAttachShader(shader_program, vertex_shader)
    glAttachShader(shader_program, fragment_shader)
    glLinkProgram(shader_program)

    if glGetProgramiv(shader_program, GL_LINK_STATUS) != GL_TRUE:
        print(glGetProgramInfoLog(shader_program).decode())
        raise RuntimeError("Shader program linking failed.")

    glDeleteShader(vertex_shader)
    glDeleteShader(fragment_shader)

    return shader_program
