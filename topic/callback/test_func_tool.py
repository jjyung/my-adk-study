import google.adk.tools as adk_tools
from inspect import signature

try:
    print("FunctionTool signature:", signature(adk_tools.FunctionTool.__init__))
except Exception as e:
    print("Error getting signature:", e)
