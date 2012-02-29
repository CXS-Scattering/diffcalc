from diffcalc.help import create_command_decorator

_commands = []
command = create_command_decorator(_commands)


def getNameFromScannableOrString(o):
        try:  # it may be a scannable
            return o.getName()
        except AttributeError:
            return str(o)


class MapperCommands(object):

    def __init__(self, geometry, hardware, sector_selector):
        self._geometry = geometry
        self._hardware = hardware
        self._sectorSelector = sector_selector

    @property
    def commands(self):
        return _commands

    @command
    def mapper(self):
        """mapper  --- Shows state of angle-mapper sector/transform, limits for auto sector and angle cuts""" #@IgnorePep8
        print self._sectorSelector.__repr__()
        print self._hardware.reprSectorLimitsAndCuts()

    @command
    def transforma(self, *args):
        """transforma {on|off|auto|manual} -- configure transform A application
        """
        self._transform('transforma', 'a', args)

    @command
    def transformb(self, *args):
        """transformb {on|off|auto|manual} -- configure transform B application
        """
        self._transform('transformb', 'b', args)

    @command
    def transformc(self, *args):
        """transformc {on|off|auto|manual} -- configure transform C application
        """

        self._transform('transformc', 'c', args)

    def _transform(self, commandName, transformName, args):
        if len(args) == 0:
            print self._sectorSelector.__repr__()
            return
        # get name
        if len(args) != 1:
            raise TypeError()
        if type(args[0]) is not str:
            raise TypeError()

        ss = self._sectorSelector
        if args[0] == 'on':
            ss.addTransorm(transformName)
        elif args[0] == 'off':
            ss.removeTransorm(transformName)
        elif args[0] == 'auto':
            ss.addAutoTransorm(transformName)
        elif args[0] == 'manual':
            ss.removeAutoTransform(transformName)
        else:
            raise TypeError()
        print self._sectorSelector.__repr__()

    @command
    def sector(self, sector=None):
        """sector {0-7} -- Select or display sector (a la Spec)
        """
        if sector is None:
            print self._sectorSelector.__repr__()
        else:
            if type(sector) is not int and not (0 <= sector <= 7):
                raise TypeError()
            self._sectorSelector.setSector(sector)
            print self._sectorSelector.__repr__()

    @command
    def autosector(self, *args):
        """autosector [None] [0-7] [0-7]... -- Set sectors that might be automatically applied""" #@IgnorePep8
        if len(args) == 0:
            print self._sectorSelector.__repr__()
        elif len(args) == 1 and args[0] is None:
            self._sectorSelector.setAutoSectors([])
            print self._sectorSelector.__repr__()
        else:
            sectorList = []
            for arg in args:
                if type(arg) is not int:
                    raise TypeError()
                sectorList.append(arg)
            self._sectorSelector.setAutoSectors(sectorList)
            print self._sectorSelector.__repr__()

    @command
    def setcut(self, scannable_or_string=None, val=None):
        """setcut {axis_scannable {val}} -- sets cut angle
        setcut {name {val}} -- sets cut angle
        """
        if scannable_or_string is None and val is None:
            print self._hardware.reprSectorLimitsAndCuts()
        else:
            name = getNameFromScannableOrString(scannable_or_string)
            if val is None:
                print '%s: %f' % (name, self._hardware.getCuts()[name])
            else:
                oldcut = self._hardware.getCuts()[name]
                self._hardware.setCut(name, float(val))
                newcut = self._hardware.getCuts()[name]
                print '%s: %f --> %f' % (name, oldcut, newcut)

    @command
    def setmin(self, name=None, val=None):
        """setmin {axis {val}} -- set lower limits used by auto sector code (None to clear)""" #@IgnorePep8
        self._setMinOrMax(name, val, self._hardware.setLowerLimit)

    @command
    def setmax(self, name=None, val=None):
        """setmax {name {val}} -- sets upper limits used by auto sector code (None to clear)""" #@IgnorePep8
        self._setMinOrMax(name, val, self._hardware.setUpperLimit)

    def _setMinOrMax(self, name, val, setMethod):
        if name is None:
            print self._hardware.reprSectorLimitsAndCuts()
        else:
            name = getNameFromScannableOrString(name)
            if val is None:
                print self.reprSectorLimitsAndCuts(name)
            else:
                setMethod(name, float(val))
