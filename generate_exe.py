import os
import subprocess


def run_command(command, shell: bool = False) -> str | None:
    """
    Run a shell command
    """
    try:
        if shell:
            process = subprocess.call(command, shell=True)
            return
        process = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        stdout, stderr = process.communicate()
        output = stdout.decode("utf-8") + stderr.decode("utf-8")
        return output
    except Exception as e:
        print(f"An error occurred while running the command {command}")
        print(e)
        return


command = ["pip", "show", "customtkinter"]
output = run_command(command)

try:
    location = [line for line in output.split("\n") if line.startswith("Location")][0]
    location = location.split(" ", maxsplit=1)[1].strip()  # venv/lib/site-packages
    print(location)
except IndexError or AttributeError:
    print("An error occurred while getting the location of the customtkinter package")
    print(output)
    quit()

this_script_dir = os.path.dirname(os.path.abspath(__file__))
gui_script_fpath = os.path.join(this_script_dir, "gui.py")
output_dir = os.path.join(this_script_dir, "generated")
spec_path = os.path.join(output_dir, "spec")
dist_path = os.path.join(output_dir, "dist")
build_path = os.path.join(output_dir, "build")

command = [
    "pyinstaller",
    "--specpath",
    spec_path,
    "--distpath",
    dist_path,
    "--workpath",
    build_path,
    "--paths",
    location,
    "--noconfirm",
    "--onefile",
    "--windowed",
    "--add-data",
    f"{location}/customtkinter;customtkinter",
    gui_script_fpath,
]
run_command(command, shell=True)
