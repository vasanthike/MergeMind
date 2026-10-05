import os

from dotenv import load_dotenv

load_dotenv()


class Settings:

    github_token: str = os.getenv(
        "GITHUB_TOKEN",
        "",
    )

    github_webhook_secret: str = os.getenv(
        "GITHUB_WEBHOOK_SECRET",
        "",
    )

    aws_region: str = os.getenv(
        "AWS_REGION",
        "eu-central-1",
    )

    ai_model: str = os.getenv(
        "AI_MODEL",
        "",
    )


settings = Settings()
