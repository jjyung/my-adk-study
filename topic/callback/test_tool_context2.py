from google.adk.tools import ToolContext
from inspect import signature, getmembers
print([m[0] for m in getmembers(ToolContext)])
