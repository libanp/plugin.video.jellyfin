# -*- coding: utf-8 -*-

#################################################################################################

import logging
import os
import sys

import xbmc
import xbmcvfs
import xbmcaddon

#################################################################################################

__addon__ = xbmcaddon.Addon(id='plugin.video.emby')
__base__ = xbmc.translatePath(os.path.join(__addon__.getAddonInfo('path'), 'resources', 'lib')).decode('utf-8')
__pcache__ = xbmc.translatePath(os.path.join(__addon__.getAddonInfo('profile'), 'emby')).decode('utf-8')
__cache__ = xbmc.translatePath('special://temp/emby').decode('utf-8')

if not xbmcvfs.exists(__pcache__ + '/'):
    from resources.lib.helper.utils import copytree

    copytree(os.path.join(__base__, 'objects'), os.path.join(__pcache__, 'objects'))

sys.path.insert(0, __cache__)
sys.path.insert(0, __pcache__)
sys.path.append(__base__)

#################################################################################################

from entrypoint import Service
from helper import settings
from emby import Emby

#################################################################################################

LOG = logging.getLogger("EMBY.service")
DELAY = int(settings('startupDelay') or 0)

#################################################################################################


if __name__ == "__main__":

    LOG.warn("-->[ service ]")
    LOG.warn("Delay startup by %s seconds.", DELAY)

    while True:

        try:
            session = Service()

            try:
                if DELAY and xbmc.Monitor().waitForAbort(DELAY):
                    raise Exception("Aborted during startup delay")

                session.service()
            except Exception as error: # TODO, build exceptions

                LOG.exception(error)
                session.shutdown()

                if 'RestartService' in error:
                    continue

        except Exception as error:
            ''' Issue initializing the service.
            '''
            LOG.exception(error)

            break

        break

    LOG.warn("--<[ service ]")
