import os
import subprocess


def snake_to_camel(snake_str: str) -> str:
    components = snake_str.split('_')
    return ''.join(x.title() for x in components)


class CmakeGenerator:
    def __init__(
        self,
        original_python_file_name: str,
        pybind11_module_name: str,
        SIL_folder: str,
        root_path: str
    ):
        self.original_python_file_name = original_python_file_name
        self.pybind11_module_name = pybind11_module_name
        self.SIL_folder = SIL_folder
        self.folder_name = os.path.basename(os.path.normpath(self.SIL_folder))

        self.root_path = root_path

    @staticmethod
    def check_path_is_sample(path: str) -> str:

        path_folders = path.split('/')
        external_libraries_flag = False
        helper_file_flag = False

        for i, folder in enumerate(path_folders):
            if folder.lower() == "external_libraries":
                external_libraries_flag = True

            if (external_libraries_flag) and \
                ((folder.lower() == "sample") or
                 (folder.lower() == "test_sil") or
                    (folder.lower() == "test_vs")):
                helper_file_flag = True

        if external_libraries_flag and helper_file_flag:
            return ""
        else:
            return path

    @staticmethod
    def discover_source_include_dirs(root_path: str, src_exts: set = None) -> list:
        """Discover directories under root_path that contain source files.

        Returns a list of paths relative to root_path (using forward slashes).
        The function mirrors the behavior previously embedded in
        CmakeGenerator.generate_cmake_lists_txt: it detects files with
        extensions in src_exts, converts backslashes to forward slashes,
        uses '' for the root directory, and preserves discovery order while
        avoiding duplicates.
        """
        if src_exts is None:
            src_exts = {'.c', '.h', '.cpp', '.hpp'}

        include_dirs = []
        seen = set()

        # Normalize root_path
        root = os.path.abspath(root_path)

        for dirpath, dirnames, filenames in os.walk(root):
            for fn in filenames:
                _, ext = os.path.splitext(fn)
                if ext.lower() in src_exts:
                    # compute relative path from root
                    rel = os.path.relpath(dirpath, root)
                    # convert Windows backslashes to forward slashes for CMake
                    rel = rel.replace('\\', '/')
                    if rel == '.':
                        rel = ''

                    rel = CmakeGenerator.check_path_is_sample(rel)

                    if (rel not in seen) and (rel != ""):
                        seen.add(rel)
                        include_dirs.append(rel)
                    break

        return include_dirs

    def generate_cmake_lists_txt(self):
        SIL_cpp_file_name = self.folder_name + "_SIL"

        code_text = ""
        code_text += "cmake_minimum_required(VERSION 3.14)\n"
        code_text += "cmake_policy(SET CMP0148 NEW)\n\n"

        code_text += f"project({self.pybind11_module_name})\n\n"

        code_text += "set(CMAKE_CXX_STANDARD 11)\n"
        code_text += "set(CMAKE_CXX_STANDARD_REQUIRED ON)\n"
        code_text += "set(CMAKE_CXX_FLAGS_RELEASE \"-O2\")\n"
        code_text += "set(CMAKE_CXX_FLAGS_RELEASE \"${CMAKE_CXX_FLAGS_RELEASE} -flto=auto\")\n\n"

        code_text += "find_package(pybind11 REQUIRED)\n\n"

        code_text += f"pybind11_add_module({self.pybind11_module_name} " + \
            f"{self.original_python_file_name}.cpp)\n\n"

        code_text += f"target_compile_options({self.pybind11_module_name} PRIVATE -Werror)\n\n"

        code_text += f"target_include_directories({self.pybind11_module_name} PRIVATE\n"

        include_dirs = CmakeGenerator.discover_source_include_dirs(
            self.root_path)

        for d in include_dirs:
            if d != "":
                code_text += "    ${CMAKE_SOURCE_DIR}/" + d + "\n"

        code_text += ")\n\n"

        with open(os.path.join(self.SIL_folder, "CMakeLists.txt"), "w", encoding="utf-8") as f:
            f.write(code_text)


class SIL_Operator:
    def __init__(
        self,
        python_file_name_to_generate: str,
        SIL_folder: str
    ):
        if python_file_name_to_generate.endswith(".py"):
            python_file_name_to_generate = python_file_name_to_generate[:-3]
        else:
            raise ValueError(
                "The python_file_name_to_generate should end with .py")

        self.python_file_name_to_generate = python_file_name_to_generate
        self.generated_file_name = snake_to_camel(
            self.python_file_name_to_generate) + "SIL"

        self.SIL_folder = SIL_folder

        self.folder_name = os.path.basename(os.path.normpath(self.SIL_folder))

        self.this_file_path = os.path.abspath(__file__)
        dir_path = os.path.dirname(self.this_file_path)

        self.root_path = os.path.abspath(os.path.join(dir_path, "../../"))

    @staticmethod
    def find_file_path(
            file_name: str,
            root_path: str) -> str:
        for dirpath, dirnames, filenames in os.walk(root_path):
            if file_name in filenames:
                return os.path.join(dirpath, file_name)

        raise FileNotFoundError(f"{file_name} not found in {root_path}")

    def build_pybind11_code(self):

        build_folder = os.path.join(self.SIL_folder, "build")

        subprocess.run(f"rm -rf {build_folder}", shell=True)
        subprocess.run(f"mkdir -p {build_folder}", shell=True)
        subprocess.run(
            f"cmake -S {self.SIL_folder} -B {build_folder} -DCMAKE_BUILD_TYPE=Release",
            shell=True
        )
        subprocess.run(
            f"cmake --build {build_folder} --config Release", shell=True)

        subprocess.run(
            f"mv {build_folder}/{self.generated_file_name}.*so {self.SIL_folder}", shell=True)

    def build_SIL_code(self):

        python_file_name = self.python_file_name_to_generate + ".py"
        python_file_path = SIL_Operator.find_file_path(
            python_file_name, self.root_path)

        cpp_file_path_to_generate = python_file_path.split(".py")[0] + ".cpp"

        cmake_generator = CmakeGenerator(
            self.python_file_name_to_generate,
            self.generated_file_name,
            self.SIL_folder, self.root_path)
        cmake_generator.generate_cmake_lists_txt()

        self.build_pybind11_code()
