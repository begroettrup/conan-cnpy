from conans import ConanFile, CMake, tools
import os

class CNpyConan(ConanFile):
    name = "cnpy"
    version = "1.0.0"
    license = "MIT"
    _source_subfolder = "cnpy"
    scm = {
        "type": "git",
        "subfolder": _source_subfolder,
        "url": "https://github.com/rogersce/cnpy.git",
        "revision": "4e8810b1a8637695171ed346ce68f6984e585ef4"
    }
    url = "https://github.com/bleenco/conan-libssh"
    description = "library to read/write .npy and .npz files"
    topics = ("npy" )
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = {"shared": False}
    generators = "cmake"
    requires = "zlib/1.2.11"
    exports_sources = [ "cmakelists.patch" ]

    def source(self):
        tools.patch(base_path=self._source_subfolder, patch_file="cmakelists.patch" )

    def build(self):
        cmake = CMake(self)
        cmake.configure(source_folder=self._source_subfolder)
        if self.options.shared:
            target = "cnpy"
        else:
            target = "cnpy-static"
        cmake.build(target=target)

    def package(self):
        self.copy("*.h", dst="include")
        if self.options.shared:
            self.copy("*.so*", dst="lib", src="lib", symlinks=True)
            self.copy("*.dll*", dst="bin", keep_path=False)
        else:
            self.copy("*.lib*", dst="lib", src="lib")
            self.copy("*.a", dst="lib", src="lib")

    def package_info(self):
        self.cpp_info.libs = ["cnpy"]