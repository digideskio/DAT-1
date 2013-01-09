"""Interface with VisTrails packages.

This is the only module that VisTrails packages need to import. It provides
the classes and methods necessary to define plot types and variable loaders.

You might want to maintain compatibility with VisTrails, like so:
try:
    import dat.packages
    from dat.gui import translate # Optional; you might want to use it if you
        # want to internationalize your strings
except ImportError:
    pass # This happens if the package was imported from VisTrails, not from
        # DAT
        # In that case, don't define plots or variable loaders.
else:
    _ = translate('packages.MyPackage') # Create a translator (optional)

    _plots = [
        Plot(...),
    ]

    class MyLoader(dat.packages.CustomVariableLoader):
        ...

    _variable_loaders = [
        MyLoader: _("My new loader"),
    ]
"""

from PyQt4 import QtGui

from dat import DEFAULT_VARIABLE_NAME

from vistrails.core.modules.vistrails_module import Module


class Plot(object):
    def __init__(self, name, **kwargs):
        self.name = name
        self.description = kwargs.get('description')

        # Build plot from a subworkflow
        self.subworkflow = kwargs['subworkflow']
        self.ports = kwargs['ports']


class Port(object):
    def __init__(self, name, type=Module, optional=False):
        self.name = name
        self.type = type
        self.optional = optional


class ModuleWrapper(object):
    """Object representing a VisTrails module in a DAT variable pipeline.

    This is a wrapper returned by Variable#add_module. It is used by VisTrails
    packages to build a pipeline for a new variable.
    """
    def add_function(self, inputport_name, vt_type, value):
        # TODO : Add a function with a specific type and value for a port of
        # this module
        pass

    def connect_outputport_to(self, outputport_name, other_module, inputport_name):
        # TODO : Connect the given output port of this module to the given
        # input port of another module
        # The modules must be ModuleWrapper's for the same Variable
        pass


class Variable(object):
    """Object representing a DAT variable.

    This is a wrapper used by VisTrails packages to build a pipeline for a new
    variable. This variable is then stored in the Manager.
    Wrapper objects are restored from the Vistrail file easily: they are
    children versions of the version tagged 'dat-vars', and have a tag
    'dat-var-name' where 'name' is the name of that specific DAT variable.
    """
    def __init__(self, type=None):
        # TODO : create or get the version tagged 'dat-vars'
        # This is the base version of all DAT variables. It consists of a
        # single OutputPort module with name 'value'
        self.type = type

    def add_module(self, module_type):
        # TODO : add a new module to the pipeline and return a wrapper for it
        return ModuleWrapper()

    def select_output_port(self, module, outputport_name):
        # TODO : connect the output port with the given name of the given
        # wrapped module to the OutputPort module (added at version 'dat-vars')
        # Check that the port is compatible to self.type
        pass


class _BaseVariableLoader(object):
    def __init__(self):
        self.default_variable_name_observer = None

    def reset(self):
        """Resets the widget so it can be used again.

        Implement this in subclasses to reset the widget.
        """
        pass

    def get_default_variable_name(self):
        """Default name for the variable that will be loaded.

        You should re-implement this to return a sensible default name for the
        variable that will be loaded. The user can edit it if need be.
        You don't need to worry about already taken names, this default will be
        made unique if need be.
        """
        DEFAULT_VARIABLE_NAME

    def default_variable_name_changed(self, new_default_name):
        """Call this function to signal that the default variable name changed.

        This can happen if the user selected a different file, ...
        """
        if self.default_variable_name_observer is not None:
            self.default_variable_name_observer(self, new_default_name)


class CustomVariableLoader(QtGui.QWidget, _BaseVariableLoader):
    """Custom variable loading tab.

    These loaders show up in a tab of their own, allowing to load any kind of
    data from any source.

    It is a widget that the user will use to choose the data he wants to load.
    load() will be called when the user confirms to actually create a Variable
    object.
    reset() is called to reset the widget to its original settings, so that it
    can be reused to load something else.
    get_default_variable_name() should return a sensible variable name for the
    variable that will be loaded; the user can edit it if need be.
    If the default variable name changes because of the user changing its
    selection, default_variable_name_changed() can be called to update it.
    """
    def load(self):
        """Load the variable and return it.

        Implement this in subclasses to load whatever data the user selected as
        a Variable object.
        """
        raise NotImplementedError


class FileVariableLoader(QtGui.QWidget, _BaseVariableLoader):
    """A loader that gets a variable from a file.

    Subclasses do not get a tab of their own, but appear on the "File" tab if
    they indicate they are able to load the selected file.
    """
    @classmethod
    def can_load(cls, filename):
        """Indicates whether this loader can read the given file.

        If true, it will be selectable by the user.
        You have to implement this in subclasses.

        Do not actually load the data here, you should only do quick checks
        (like file extension or magic number).
        """
        return False

    def __init__(self):
        """Constructor.

        filename is the file that we want to load. Do not keep the file open
        while this object exists, it could interfere with other loaders.
        """
        super(FileVariableLoader, self).__init__()

    def load(self):
        """Load the variable and return it.

        Implement this in subclasses to do the actual loading of the variable
        from the filename that was given to the constructor, using the desired
        parameters.
        """
        raise NotImplementedError
