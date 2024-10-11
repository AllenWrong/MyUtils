import subprocess
from loguru import logger


oss_cp_prefix = 'ossutils64 cp -f'


def exec(cmd_prefix, *args):
    if cmd_prefix[-1] != " ":
        cmd_prefix += " "

    cmd = f"{cmd_prefix}{' '.join(map(str, args))}"
    logger.info(cmd)

    process = subprocess.Popen(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True
    )
    output, error = process.communicate()
    if error:
        raise IOError(error)
    else:
        return output


exec(oss_cp_prefix, "name", "file")
