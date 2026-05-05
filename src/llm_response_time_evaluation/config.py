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


# Number of calls per model/task pair. The final Excel value is the average.
RUNS_PER_MODEL = 1

# Add more tasks here, for example:
# BenchmarkTask(name="1k", prompt="paste roughly 1k tokens here")
# BenchmarkTask(name="2k", prompt="paste roughly 2k tokens here")
BENCHMARK_TASKS = [
    BenchmarkTask(
        name="0.01k",
        prompt="0123456789",
    ),
]

MODEL_CONFIGS = [
    ModelConfig(
        display_name="Azure OpenAI GPT-4.1 (westus3 Global Stadard)",
        provider="azure_openai",
        endpoint_env="AZURE_OPENAI_ENDPOINT",
        api_key_env="AZURE_OPENAI_API_KEY",
        model_env="AZURE_OPENAI_GPT41_DEPLOYMENT",
        api_version_env="AZURE_OPENAI_API_VERSION",
    ),
    ModelConfig(
        display_name="Azure AI Foundry GPT-5.4 Mini (westus3 Global Stadard)",
        provider="azure_foundry_openai",
        endpoint_env="AZURE_FOUNDRY_ENDPOINT_OPENAI",
        api_key_env="AZURE_FOUNDRY_API_KEY",
        model_env="AZURE_FOUNDRY_GPT54_MINI_MODEL_OPENAI_5_1_mini",
        api_version_env="AZURE_FOUNDRY_API_VERSION_OPENAI",
    ),
    ModelConfig(
        display_name="Azure AI Foundry DeepSeek-V4-Flash (westus3 Global Stadard)",
        provider="azure_foundry",
        endpoint_env="AZURE_FOUNDRY_ENDPOINT",
        api_key_env="AZURE_FOUNDRY_API_KEY",
        model_env="AZURE_FOUNDRY_DEEPSEEK_V4_FLASH_MODEL",
        api_version_env="AZURE_FOUNDRY_API_VERSION",
    ),
    ModelConfig(
        display_name="Alibaba Cloud DeepSeek-V4-Flash (Germany)",
        provider="openai_compatible",
        endpoint_env="ALIBABA_CLOUD_COMPATIBLE_BASE_URL",
        api_key_env="ALIBABA_CLOUD_API_KEY",
        model_env="ALIBABA_DEEPSEEK_V4_FLASH_MODEL",
    ),
]
