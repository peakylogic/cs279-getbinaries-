import subprocess


def run_command(command):
    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Command '{' '.join(command)}' failed with error: {e}")
        return None


def check_installed_version(package_name):

    output = run_command(["dpkg-query", "-W", "-f='${Version}'", package_name])
    if output:
        return output.replace("'", "")
    else:
        print(f"{package_name} is not installed.")
        return None


def install_or_revert_package(package_name, target_version):

    current_version = check_installed_version(package_name)
    if current_version and current_version.startswith(target_version):
        print(f"{package_name} is already at the desired version ({target_version}).")
        return True
    elif current_version:
        print(f"Current version of {package_name} is {current_version}. Reverting to {target_version}.")
    else:
        print(f"Installing {package_name} version {target_version}.")

    package_version = f"{package_name}={target_version}"
    if run_command(["sudo", "apt-get", "install", "-y", package_version]) is None:
        print(f"Failed to install/revert {package_version}.")
        return False

    print(f"{package_version} successfully installed.")
    return True


def find_binaries(package_name):

    output = run_command(["dpkg-query", "-L", package_name])
    if output is None:
        print(f"Failed to find binaries for {package_name}.")
        return []

    binaries = output.split('\n')
    return [binary for binary in binaries if binary.startswith('/usr/bin/') or binary.startswith('/bin/')]


package = "slurm-wlm"
version = "22.05.8"  

if install_or_revert_package(package, version):
    binaries = find_binaries(package)
    print("Binaries for the package:", binaries)
else:
    print("Installation or reversion failed.")
