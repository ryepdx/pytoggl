"""
This module contains code that is non-Toggl specific.
It is code that Good Code has deemed generally useful
and that I don't really dislike enough to remove.

However, because it is non-Toggl-specific, I've moved
it out to this module in order to simplify working with
the Toggl-specific code.

"""

class Dictionary(object):
    """Encapsulates a dict and allows its values to be accessed with dot
    notation. Encapsulates all of its values as well, recursively, so that
    any dictionaries passed as values also get the ability to be accessed
    using dot notation. Allowing access via dot notation aids IDEs in
    autocompletion and thus reduces the risk of mistyping a dictionary
    key name.

    """

    def __init__(self, **attribs):
        """Takes a list of keyword arugments and sets values accordingly.
        Also drills down into all collections passed in and wraps anything
        that looks like a dictionary.

        """
        for k, v in attribs.iteritems():
            if isinstance(v, list):
                # Wrap every dict in every list in a Dictionary.
                attribs[k] = [el if isinstance(el, Dictionary
                    ) else Dictionary(**el) for el in v]

            elif isinstance(v, dict):
                # Wrap a Dictionary around every dict passed in.
                attribs[k] = v if isinstance(v, Dictionary) else Dictionary(**v)

        # Set this object's attributes to now-wrapped values passed in.
        self.__dict__.update(attribs)

    @property
    def keys(self):
        """Pass-through for dict.keys()"""
        return self.__dict__.keys()

    def __unicode__(self):
        """Returns _unicode_value property if set
        Returns super().__unicode__() otherwise.

        """
        if hasattr(self, '_unicode_value'):
            if self._unicode_value is None:
                return '(none)'
            else:
                return self._unicode_value
        else:
            return super(Dictionary, self).__unicode__()

    def __str__(self):
        """Pass-through for __unicode__"""
        return unicode(self).encode('utf-8')

    def __contains__(self, key):
        """Pass-through for dict.__contains__()"""
        return key in self.__dict__


