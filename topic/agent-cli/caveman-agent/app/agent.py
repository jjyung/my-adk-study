# ruff: noqa
# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from google.adk.agents import Agent
from google.adk.apps import App
from google.adk.models import Gemini
from google.genai import types

import google.auth
import os

_, project_id = google.auth.default()
os.environ["GOOGLE_CLOUD_PROJECT"] = project_id
os.environ["GOOGLE_CLOUD_LOCATION"] = "global"
os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "True"


root_agent = Agent(
    name="caveman_compressor",
    model=Gemini(
        model="gemini-flash-latest",
        retry_options=types.HttpRetryOptions(attempts=3),
    ),
    instruction=(
        "You compress verbose input into terse caveman-style technical output.\n"
        "Rules:\n"
        "1. Keep meaning, constraints, and technical accuracy.\n"
        "2. Use short, blunt phrases; drop filler.\n"
        "3. Prefer subject-verb-object fragments.\n"
        "4. Keep critical numbers, APIs, paths, and commands unchanged.\n"
        "5. Do not add new facts.\n"
        "6. Output only compressed text."
    ),
    tools=[],
)

app = App(
    root_agent=root_agent,
    name="app",
)
