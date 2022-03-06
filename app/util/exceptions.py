class ModsAlreadyInstalled(Exception):
    """This exception is raised when an attempt is made to install mods without
    uninstalling previously installed mods.
    """

    pass


class NoModsInstalled(Exception):
    """This exception is raised when an attempt is made to uninstall mods when
    no mods are installed.
    """

    pass


class InvalidModpack(Exception):
    """This exception is raised when a zip file is missing a modimporter script
    or a Mods folder.
    """

    pass


class InvalidModimporter(Exception):
    """This exception is raised when a modimporter is not in the
    legal_modimporters list.
    """

    pass


class PathNotSelected(Exception):
    """This exception is raised when trying to install or uninstall a modpack when
    no path has been selected for Hades or the Modpack folder.
    """

    pass


class UnknownHadesPath(Exception):
    """This exception is raised when the Hades path is incorrect and the correct path
    cannot be inferred.
    """

    pass


class NoConfigFound(Exception):
    """This exception is raised when no config.ini file is found, or it is malformed"""

    pass
