import inspect
import os, os.path


# Default variable name, if a variable loader can't provide a more specific one
DEFAULT_VARIABLE_NAME = "variable"

# MIME type of DAT variables
MIMETYPE_DAT_VARIABLE = 'X-Vistrails/DATVariable'

# MIME type of DAT plots
MIMETYPE_DAT_PLOT = 'X-Vistrails/DATPlot'


class DATRecipe(object):
    """Just a simple class holding a Plot its parameters.
    """
    def __init__(self, plot, variables):
        """__init__(plot: Plot, variables: dict of Variables)
        """
        self.plot = plot
        self.variables = dict(variables)
        self._hash = hash((
                self.plot,
                tuple((k, v.name) for k, v in self.variables.iteritems())))

    def __eq__(self, other):
        if not isinstance(other, DATRecipe):
            raise TypeError
        return (self.plot, self.variables) == (other.plot, other.variables)

    def __hash__(self):
        return self._hash
    
    def get_plot_modules(self, plot, pipeline):
        #TODO: implement
        return pipeline.module_list

class PipelineInformation(object):
    """A simple class holding enough information on a pipeline to locate it.
    """
    def __init__(self, version, recipe, port_map=None, var_map=None):
        self.version = version
        self.recipe = recipe
        self.port_map = port_map
        self.var_map = var_map # {param: [conn_id: int]}


class BaseVariableLoader(object):
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
        return DEFAULT_VARIABLE_NAME

    def default_variable_name_changed(self, new_default_name):
        """Call this function to signal that the default variable name changed.

        This can happen if the user selected a different file, ...
        """
        if self.default_variable_name_observer is not None:
            self.default_variable_name_observer(self, new_default_name)
