"""Provider clients for benchmark requests."""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any, Protocol
from urllib.parse import urlencode

import requests
from openai import OpenAI

from multi_llm_speed_comparison.config import TEMPERATURE, ModelConfig


DEFAULT_TIMEOUT_SECONDS = 120


@dataclass(frozen=True)
class ModelResponse:
    text: str
    output_tokens: int | None


class ModelClient(Protocol):
    def complete(self, prompt: str) -> ModelResponse:
        """Send a prompt and return the response text plus token usage."""


def build_client(config: ModelConfig) -> ModelClient:
    if config.provider == "azure_openai":
        return AzureOpenAIClient(config)
    if config.provider == "azure_foundry_openai":
        return AzureFoundryOpenAIClient(config)
    if config.provider == "azure_foundry":
        return AzureFoundryClient(config)
    if config.provider == "openai_compatible":
        return OpenAICompatibleClient(config)
    if config.provider == "openai_compatible_responses":
        return OpenAICompatibleResponsesClient(config)

    msg = f"Unsupported provider '{config.provider}' for {config.display_name}."
    raise ValueError(msg)


class BaseRequestsClient:
    def __init__(self, config: ModelConfig) -> None:
        self.config = config
        self.endpoint = _env(config.endpoint_env).rstrip("/")
        self.api_key = _env(config.api_key_env)
        self.model = _env(config.model_env)
        self.api_version = (
            _env(config.api_version_env) if config.api_version_env else None
        )

    def _post(
        self, url: str, headers: dict[str, str], payload: dict[str, Any]
    ) -> ModelResponse:
        response = requests.post(
            url,
            headers=headers,
            json=payload,
            timeout=DEFAULT_TIMEOUT_SECONDS,
        )
        response.raise_for_status()
        data = response.json()
        # print(f"Request url: {url}")
        # print(f"Received response data: {data}")
        return ModelResponse(
            text=_extract_text(data),
            output_tokens=_extract_output_tokens(data),
        )


class AzureOpenAIClient(BaseRequestsClient):
    """Azure OpenAI chat completions endpoint using a deployment name."""

    def complete(self, prompt: str) -> ModelResponse:
        query = urlencode({"api-version": self.api_version})
        url = (
            f"{self.endpoint}/openai/deployments/{self.model}/chat/completions?{query}"
        )
        # print(f"AzureOpenAIClient url: {url}, api_key: {self.api_key}")
        return self._post(
            url=url,
            headers={"api-key": self.api_key, "Content-Type": "application/json"},
            payload=_chat_payload(prompt, temperature=TEMPERATURE),
        )


class AzureFoundryClient(BaseRequestsClient):
    """Azure AI Foundry model inference chat completions endpoint."""

    def complete(self, prompt: str) -> ModelResponse:
        query = urlencode({"api-version": self.api_version}) if self.api_version else ""
        suffix = f"?{query}" if query else ""
        url = f"{self.endpoint}/chat/completions{suffix}"
        payload = _chat_payload(prompt, temperature=TEMPERATURE)
        payload["model"] = self.model
        return self._post(
            url=url,
            headers={"api-key": self.api_key, "Content-Type": "application/json"},
            payload=payload,
        )


class AzureFoundryOpenAIClient(BaseRequestsClient):
    """Azure AI Foundry OpenAI Responses API endpoint."""

    def complete(self, prompt: str) -> ModelResponse:
        query = urlencode({"api-version": self.api_version})
        url = f"{self.endpoint}/openai/responses?{query}"
        return self._post(
            url=url,
            headers={"api-key": self.api_key, "Content-Type": "application/json"},
            payload=_responses_payload(
                model=self.model,
                prompt=prompt,
                temperature=TEMPERATURE,
            ),
        )


class OpenAICompatibleClient(BaseRequestsClient):
    """OpenAI-compatible chat completions client, used by Alibaba Cloud DashScope."""

    def complete(self, prompt: str) -> ModelResponse:
        payload = _chat_payload(prompt, temperature=TEMPERATURE)
        payload["model"] = self.model
        return self._post(
            url=f"{self.endpoint}/chat/completions",
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            payload=payload,
        )


class OpenAICompatibleResponsesClient:
    """OpenAI-compatible Responses API client using the OpenAI SDK."""

    def __init__(self, config: ModelConfig) -> None:
        self.config = config
        self.model = _env(config.model_env)
        self._client = OpenAI(
            base_url=_env(config.endpoint_env).rstrip("/"),
            api_key=_build_openai_api_key(config),
            timeout=DEFAULT_TIMEOUT_SECONDS,
        )

    def complete(self, prompt: str) -> ModelResponse:
        response = self._client.responses.create(
            model=self.model,
            input=prompt,
        )
        data = response.model_dump()
        return ModelResponse(
            text=_extract_text(data),
            output_tokens=_extract_output_tokens(data),
        )


def _chat_payload(prompt: str, temperature: float) -> dict[str, Any]:
    return {
        "messages": [
            {
                "role": "user",
                "content": prompt,
            }
        ],
        "temperature": temperature,
        # "reasoning_effort": "low",  
    }


def _responses_payload(model: str, prompt: str, temperature: float) -> dict[str, Any]:
    return {
        "model": model,
        "input": prompt,
        "temperature": temperature,
    }


def _build_openai_api_key(config: ModelConfig) -> str | Any:
    api_key = _env(config.api_key_env)
    if api_key.lower() == "azure_default_credential":
        from azure.identity import DefaultAzureCredential, get_bearer_token_provider

        return get_bearer_token_provider(
            DefaultAzureCredential(),
            "https://ai.azure.com/.default",
        )
    return api_key


def _env(name: str | None) -> str:
    if not name:
        msg = "Internal error: env var name is missing."
        raise ValueError(msg)
    value = os.getenv(name)
    if not value:
        msg = f"Missing required environment variable: {name}"
        raise RuntimeError(msg)
    return value


def _extract_text(data: dict[str, Any]) -> str:
    output_text = data.get("output_text")
    if isinstance(output_text, str):
        return output_text

    output = data.get("output")
    if isinstance(output, list):
        extracted_parts: list[str] = []
        for item in output:
            if not isinstance(item, dict):
                continue
            content = item.get("content")
            if not isinstance(content, list):
                continue
            extracted_parts.extend(_extract_content_parts(content))
        if extracted_parts:
            return "".join(extracted_parts)

    choices = data.get("choices") or []
    if not choices:
        return ""

    first_choice = choices[0]
    message = first_choice.get("message") or {}
    content = message.get("content")
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return "".join(_extract_content_parts(content))
    return str(content or "")


def _extract_content_parts(content: list[Any]) -> list[str]:
    parts: list[str] = []
    for part in content:
        if not isinstance(part, dict):
            continue
        text = part.get("text")
        if isinstance(text, str):
            parts.append(text)
    return parts


def _extract_output_tokens(data: dict[str, Any]) -> int | None:
    usage = data.get("usage") or {}
    for key in ("completion_tokens", "output_tokens", "generated_tokens"):
        value = usage.get(key)
        if isinstance(value, int):
            return value
    return None
