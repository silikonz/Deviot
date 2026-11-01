#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import sublime_plugin

from os import path
from threading import Thread

from ..api import deviot
from ..libraries.syntax import Syntax
from ..libraries.thread_progress import ThreadProgress


class DeviotCheckRequirementsCommand(sublime_plugin.WindowCommand):
    """Startup check

    PlatformIO is expected to be installed (see PIO_PATH in api/deviot.py),
    so only the syntax files and the list of boards are prepared.
    """
    def run(self):
        thread = Thread(target=self.check)
        thread.start()
        ThreadProgress(thread, 'processing', '')

    def check(self):
        Syntax()

        if(not path.exists(deviot.boards_file_path())):
            deviot.save_board_list()
