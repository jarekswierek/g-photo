# -*- coding: utf-8 -*-
import threading


def run_background_task(method):
    """Run background task.
    """
    t = threading.Thread(target=method)
    t.setDaemon(True)
    t.start()
