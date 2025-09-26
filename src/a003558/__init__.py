from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("a003558")
except PackageNotFoundError:
    __version__ = "0"

# Let op:
# We importeren viz niet automatisch.
# Gebruikers kunnen zelf importeren:
#   from a003558.viz import plot_basis
