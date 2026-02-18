# Available at setup time due to pyproject.toml
from pybind11.setup_helpers import Pybind11Extension, build_ext
from setuptools import setup

__version__ = "1.0.1"

# The main interface is through Pybind11Extension.
# * You can add cxx_std=11/14/17, and then build_ext can be removed.
# * You can set include_pybind11=false to add the include directory yourself,
#   say from a submodule.
#
# Note:
#   Sort input source files if you glob sources to ensure bit-for-bit
#   reproducible builds (https://github.com/pybind/python_example/pull/53)

ext_modules = [
    Pybind11Extension(
        "PyORCHESTRA",
         ["src/pybindmain.cpp",
        "src/Calculator.cpp",
        "src/Expander.cpp",
        "src/ExpressionGraph.cpp",
        "src/ExpressionString.cpp",
        "src/FileBasket.cpp",
        "src/IO.cpp",
        "src/MemoryNode.cpp",
        "src/Node.cpp",
        "src/NodeIOObject.cpp",
        "src/NodeIOPair.cpp",
        "src/NodeIOVar.cpp",
        "src/NodeProcessor.cpp",
        "src/NodeType.cpp",
        "src/OObject.cpp",
        "src/OObjectBasket.cpp",
        "src/OObjectPieceOfText.cpp",
        "src/OrchestraReader.cpp",
        "src/ParameterList.cpp",
        "src/Parser.cpp",
        "src/ParserStringTokenizer.cpp",
        "src/StopFlag.cpp",
        "src/StringTokenizer.cpp",
        "src/UnEq.cpp",
        "src/UnEqGroup.cpp",
        "src/Var.cpp",
        "src/VarGroup.cpp",
        ],
        # Example: passing in the version to the compiled code
        define_macros=[("VERSION_INFO", __version__)],
    ),
]

setup(
    name="PyORCHESTRA",
    version=__version__,
    author="Hans Meeussen",
    author_email="hans@meeussen.nl",
    #url="https://github.com/pybind/python_example",
    description="A test project using pybind11",
    long_description="",
    ext_modules=ext_modules,
    #extras_require={"test": "pytest"},
    # Currently, build_ext only provides an optional "highest supported C++
    # level" feature, but in the future it may provide more features.
    cmdclass={"build_ext": build_ext},
    zip_safe=False,
    python_requires=">=3.9",
)
