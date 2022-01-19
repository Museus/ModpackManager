from Modpack import Modpack


def get_modpack_from_path(modpack_path):
    return Modpack(modpack_path)


def is_valid_modpack(modpack_path):
    return Modpack.is_valid(modpack_path)
