import subprocess
import logging


def runcmd(cmd, verbose=True):
    """run command and return output"""

    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        shell=True,
    )

    std_out, std_err = process.communicate()

    if verbose and std_out:
        logging.warning(f"std out :  {std_out.strip()}")

    if verbose and std_err:
        logging.warning(f"std err :  {std_err.strip()}")

    return std_out, std_err
