def classFactory(iface):
    from .qnet import QNet
    return QNet(iface)
    