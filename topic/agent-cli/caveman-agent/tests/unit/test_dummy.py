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
from app.agent import root_agent


def test_agent_config_is_caveman_compressor() -> None:
    """Keep this deterministic: validate config, not model output."""
    assert root_agent.name == "caveman_compressor"
    assert root_agent.tools == []
    assert "compress verbose input" in root_agent.instruction.lower()
