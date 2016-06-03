#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
	#程序进入点，指向配置文件
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "QinggangManageSys.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
