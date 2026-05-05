"""User-editable benchmark configuration.

Change the values in this file when you want to add models, add prompt sizes,
or run each model more than once before averaging the results.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class BenchmarkTask:
    name: str
    prompt: str


@dataclass(frozen=True)
class ModelConfig:
    display_name: str
    provider: str
    endpoint_env: str
    api_key_env: str
    model_env: str
    api_version_env: str | None = None

# Add more tasks here, for example:
# BenchmarkTask(name="1k", prompt="paste roughly 1k tokens here")
# BenchmarkTask(name="2k", prompt="paste roughly 2k tokens here")
BENCHMARK_TASKS = [
    # BenchmarkTask(
    #     name="0.01k",
    #     prompt="what model are you?",
    # ),
    BenchmarkTask(
        name="2576 words input",
        prompt="what model are you?",
    ),
]

# Number of calls per model/task pair. The final Excel value is the average.
RUNS_PER_MODEL = 1

# Sampling temperature used for all model calls.
TEMPERATURE = 0



MODEL_CONFIGS = [
    ModelConfig(
        display_name="GPT-4.1 - Azure OpenAI - westus3 Global Stadard",
        provider="azure_openai",
        endpoint_env="AZURE_OPENAI_ENDPOINT",
        api_key_env="AZURE_OPENAI_API_KEY",
        model_env="AZURE_OPENAI_GPT41_DEPLOYMENT",
        api_version_env="AZURE_OPENAI_API_VERSION",
    ),
    ModelConfig(
        display_name="GPT-5.4 Mini - Azure AI Foundry OpenAI - westus3 Global Stadard",
        provider="azure_foundry_openai",
        endpoint_env="AZURE_FOUNDRY_ENDPOINT_OPENAI",
        api_key_env="AZURE_FOUNDRY_API_KEY",
        model_env="AZURE_FOUNDRY_GPT54_MINI_MODEL_OPENAI",
        api_version_env="AZURE_FOUNDRY_API_VERSION_OPENAI",
    ),
    ModelConfig(
        display_name="GPT-5.4 Mini - Azure AI Foundry OpenAI - westus3 Global Stadard - Priority",
        provider="azure_foundry_openai",
        endpoint_env="AZURE_FOUNDRY_ENDPOINT_OPENAI",
        api_key_env="AZURE_FOUNDRY_API_KEY",
        model_env="AZURE_FOUNDRY_GPT54_MINI_MODEL_OPENAI_priority",
        api_version_env="AZURE_FOUNDRY_API_VERSION_OPENAI",
    ),
    ModelConfig(
        display_name="DeepSeek-V4-Flash - Azure AI Foundry - westus3 Global Stadard",
        provider="azure_foundry",
        endpoint_env="AZURE_FOUNDRY_ENDPOINT",
        api_key_env="AZURE_FOUNDRY_API_KEY",
        model_env="AZURE_FOUNDRY_DEEPSEEK_V4_FLASH_MODEL",
        api_version_env="AZURE_FOUNDRY_API_VERSION",
    ),
    ModelConfig(
        display_name="DeepSeek-V4-Flash - Azure AI Foundry - koreacentral Global Stadard",
        provider="azure_foundry",
        endpoint_env="AZURE_FOUNDRY_ENDPOINT_KOREA_CENTRAL",
        api_key_env="AZURE_FOUNDRY_API_KEY_KOREA_CENTRAL",
        model_env="AZURE_FOUNDRY_DEEPSEEK_V4_FLASH_MODEL_KOREA_CENTRAL",
        api_version_env="AZURE_FOUNDRY_API_VERSION_KOREA_CENTRAL",
    ),
    ModelConfig(
        display_name="DeepSeek-V4-Flash - Alibaba Cloud DeepSeek-V4-Flash - Germany",
        provider="openai_compatible",
        endpoint_env="ALIBABA_CLOUD_COMPATIBLE_BASE_URL",
        api_key_env="ALIBABA_CLOUD_API_KEY",
        model_env="ALIBABA_DEEPSEEK_V4_FLASH_MODEL",
    ),
    ModelConfig(
        display_name="DeepSeek-V4-Flash - Aliyun DeepSeek-V4-Flash - China",
        provider="openai_compatible",
        endpoint_env="ALIYUN_COMPATIBLE_BASE_URL",
        api_key_env="ALIYUN_API_KEY",
        model_env="ALIYUN_DEEPSEEK_V4_FLASH_MODEL",
    ),
]
