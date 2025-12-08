# Copyright 2023 DeepMind Technologies Limited.
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


"""Language Model that uses OpenAI's GPT models."""

# import os
# import openai
# from concordia.language_model import language_model
# from concordia.utils import measurements as measurements_lib
# from concordia.language_model.base_gpt_model import BaseGPTModel
#
#
# class GptLanguageModel(BaseGPTModel):
#   """Language Model that uses OpenAI GPT models."""
#
#   def __init__(
#       self,
#       model_name: str,
#       *,
#       api_key: str | None = None,
#       measurements: measurements_lib.Measurements | None = None,
#       channel: str = language_model.DEFAULT_STATS_CHANNEL,
#   ):
#     """Initializes the instance.
#
#     Args:
#       model_name: The language model to use. For more details, see
#         https://platform.openai.com/docs/guides/text-generation/which-model-should-i-use.
#       api_key: The API key to use when accessing the OpenAI API. If None, will
#         use the OPENAI_API_KEY environment variable.
#       measurements: The measurements object to log usage statistics to.
#       channel: The channel to write the statistics to.
#     """
#     if api_key is None:
#         api_key = os.environ['OPENAI_API_KEY']
#     self._api_key = api_key
#     client = openai.OpenAI(api_key=self._api_key)
#     super().__init__(model_name=model_name,
#                      client=client,
#                      measurements=measurements,
#                      channel=channel)
import os
from openai import OpenAI  # 官方 OpenAI 客户端
from concordia.language_model import language_model
from concordia.utils import measurements as measurements_lib
from concordia.language_model.base_gpt_model import BaseGPTModel


class GptLanguageModel(BaseGPTModel):
    """Language Model that uses OpenAI GPT models via a custom proxy."""

    def __init__(
        self,
        model_name: str,
        *,
        api_key: str | None = None,
        base_url: str = "https://xiaoai.plus/v1",  # 中转接口地址
        measurements: measurements_lib.Measurements | None = None,
        channel: str = language_model.DEFAULT_STATS_CHANNEL,
    ):
        """Initializes the instance.

        Args:
          model_name: The language model to use. For example, "gpt-4o".
          api_key: The API key to use when accessing the proxy API. If None,
            will use the `OPENAI_API_KEY` environment variable.
          base_url: The base URL of the proxy API.
          measurements: The measurements object to log usage statistics to.
          channel: The channel to write the statistics to.
        """
        if api_key is None:
            api_key = os.environ['OPENAI_API_KEY']  # 从环境变量获取 API Key
        self._api_key = api_key
        self._base_url = base_url
        # 使用 OpenAI 客户端，并指定 base_url 和 api_key
        self._client = OpenAI(base_url=base_url, api_key=api_key)
        super().__init__(model_name=model_name,
                         client=self._client,  # 客户端传递给父类
                         measurements=measurements,
                         channel=channel)
