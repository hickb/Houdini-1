
import os
import hrpyc
connection, hou = hrpyc.import_remote_module()


def read_file(file_name="scratch.py"):
    file_path = r"C:\Users\vshah\.PyCharmCE2018.1\config\scratches"
    file_to_read = os.path.join(file_path, file_name)
    file_handle = open(file_to_read)
    file_data = file_handle.readlines()
    return file_data[4:]


lines = read_file("scratch_1.py")
string_to_send = ''.join(lines)

if len(hou.selectedNodes()) > 0:
    selected_node = hou.selectedNodes()[0]
    attrib_name = "python"
    selected_node.setParms({'python': string_to_send})
