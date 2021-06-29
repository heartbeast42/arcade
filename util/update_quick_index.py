"""
Script used to create the quick index
"""
import re
from pathlib import Path

titles = {
    'arcade_types.py': 'Arcade Data Types',
    'application.py': 'Window and View Classes',
    'buffered_draw_commands.py': 'Buffered Draw Commands',
    'context.py': 'OpenGL Context',
    'drawing_support.py': 'Support for Drawing Commands',
    'draw_commands.py': 'Drawing Primitives',
    'earclip_module.py': 'Geometry Support',
    'emitter.py': 'Particle Emitter',
    'emitter_simple.py': 'Particle Emitter',
    'geometry.py': 'Geometry Support',
    'hitbox.py': 'Geometry Support',
    'isometric.py': 'Isometric Map Support (incomplete)',
    'joysticks.py': 'Game Controller Support',
    'particle.py': 'Particle',
    'paths.py': 'Pathfinding Support',
    'physics_engines.py': 'Simple Physics Engines',
    'pymunk_physics_engine.py': 'Pymunk Physics Engine',
    'sound.py': 'Sound Support',
    'sprite.py': 'Sprites',
    'sprite_list.py': 'Sprite Lists',
    'text.py': 'Draw Text',
    'texture.py': 'OpenGL Texture Management',
    'tilemap.py': 'Loading TMX (Tiled Map Editor) Maps',
    'utils.py': 'Misc Utility Functions',
    'version.py': 'Arcade Version Number',
    'window_commands.py': 'Window Commands',
    'texture_atlas.py': 'Texture Atlas',
    'scene.py': 'Sprite Scenes',

    'gui/core.py': 'GUI',
    'gui/manager.py': 'GUI',
    'gui/style.py': 'GUI',
    'gui/ui_style.py': 'GUI',
    'gui/utils.py': 'GUI',
    'gui/exceptions.py': 'GUI',
    'gui/text_utils.py': 'GUI',

    'gl/buffer.py': 'OpenGL Buffer',
    'gl/context.py': 'OpenGL Context',
    'gl/enums.py': 'OpenGL Enums',
    'gl/exceptions.py': 'OpenGL Exceptions',
    'gl/framebuffer.py': 'OpenGL FrameBuffer',
    'gl/geometry.py': 'OpenGL Geometry',
    'gl/program.py': 'OpenGL Program',
    'gl/glsl.py': 'OpenGL GLSL',
    'gl/types.py': 'OpenGL Types',
    'gl/uniform.py': 'OpenGL Uniform Data',
    'gl/utils.py': 'OpenGL Utils',
    'gl/query.py': 'OpenGL Query',
    'gl/texture.py': 'OpenGL Texture',
    'gl/vertex_array.py': 'OpenGL Vertex Array (VAO)',
}


def get_member_list(filepath):
    file_pointer = open(filepath)
    filename = filepath.name

    class_re = re.compile("^class ([A-Za-z0-9]+[^\(:]*)")
    function_re = re.compile("^def ([a-z][a-z0-9_]*)")
    type_re = re.compile("^([A-Za-z][A-Za-z0-9_]*) = ")

    class_list = []
    function_list = []
    type_list = []

    line_no = 0
    try:
        for line in file_pointer:
            line_no += 1

            class_names = class_re.findall(line)
            for class_name in class_names:
                class_list.append(class_name)

            function_names = function_re.findall(line)
            for method_name in function_names:
                function_list.append(method_name)

            type_names = type_re.findall(line)
            for type_name in type_names:
                if type_name not in ['LOG']:
                    type_list.append(type_name)

    except Exception as e:
        print(f"Exception processing {filename} on line {line_no}: {e}")

    class_list.sort()
    function_list.sort()
    type_list.sort()
    return type_list, class_list, function_list


def process_directory(directory, text_file):
    file_list = directory.glob('*.py')

    text_file.write(f"\n")

    if directory.name == "arcade":
        prepend = ""
    else:
        prepend = directory.name + "/"

    for path in file_list:
        if path.name == "__init__.py":
            break

        if "test" in path.name:
            break

        type_list, class_list, function_list = get_member_list(path)

        package = "arcade"
        if directory.name != "arcade":
            package += f".{directory.name}"
        path_name = prepend + path.name

        if path_name in titles and (len(type_list) > 0 or len(class_list) > 0 or len(function_list) > 0):

            # Print title
            title = titles[path_name]
        else:
            title = ""

        # Classes
        if len(class_list) > 0:
            for item in class_list:
                text_file.write(f"   * - :py:class:`{package}.{item}`\n")
                text_file.write(f"     - {title}\n")
                # text_file.write(f"     - Class\n")
                # text_file.write(f"     - {path_name}\n")

        # Functions
        if len(function_list) > 0:
            for item in function_list:
                text_file.write(f"   * - :py:func:`{package}.{item}`\n")
                text_file.write(f"     - {title}\n")
                # text_file.write(f"     - Func\n")
                # text_file.write(f"     - {path_name}\n")


def include_template(text_file):
    with open('template_quick_index.rst', 'r') as content_file:
        quick_index_content = content_file.read()

    text_file.write(quick_index_content)


def main():

    text_file = open("../doc/quick_index.rst", "w")
    include_template(text_file)

    # text_file.write(f"The ``arcade`` module\n")
    # text_file.write(f"---------------------\n\n")
    process_directory(Path("../arcade"), text_file)

    # text_file.write(f"The ``arcade.gl`` module\n")
    # text_file.write(f"-------------------------\n\n")
    # process_directory(Path("../arcade/gl"), text_file)

    # text_file.write(f"The ``arcade.gui`` module\n")
    # text_file.write(f"-------------------------\n\n")
    process_directory(Path("../arcade/gui"), text_file)

    text_file.close()
    print("Done creating quick_index.rst")


main()
