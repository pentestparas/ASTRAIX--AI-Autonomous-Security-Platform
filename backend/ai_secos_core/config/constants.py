"""Platform-wide constants.

Pure values that have no dependency on environment configuration.
Avoid cross-module "magic numbers" by consolidating here.
"""

# --- HTTP / network timeouts ---
DEFAULT_HTTP_TIMEOUT_SECONDS: float = 30.0

# --- Plugin execution defaults ---
DEFAULT_PLUGIN_TIMEOUT_SECONDS: int = 300
DEFAULT_PLUGIN_CPU_QUOTA: float = 1.0          # cores
DEFAULT_PLUGIN_MEMORY_MB: int = 512            # MiB
DEFAULT_PLUGIN_MAX_OUTPUT_BYTES: int = 16 * 1024 * 1024  # 16 MiB

# --- Risk scoring bounds ---
DEFAULT_RISK_SCORE_MIN: int = 0
DEFAULT_RISK_SCORE_MAX: int = 100

# --- Finding Engine ---
DEFAULT_DEDUPE_HASH_BYTES: int = 32  # sha-256 -> 32 bytes

# --- AI Gateway ---
DEFAULT_AI_TIMEOUT_SECONDS: float = 60.0
DEFAULT_AI_MAX_TOKENS: int = 4096
DEFAULT_AI_RETRY_ATTEMPTS: int = 3
DEFAULT_AI_RETRY_BACKOFF_SECONDS: float = 1.0
