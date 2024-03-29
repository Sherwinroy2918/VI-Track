import cx_Freeze

executables = [cx_Freeze.Executable("ui.py")]

cx_Freeze.setup(
    name="your_executable",
    version="1.0",
    description="A Python executable",
    executables=executables,
)

