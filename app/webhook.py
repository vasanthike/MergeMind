from fastapi import APIRouter, Header, HTTPException, Request

from app.config import settings
from app.review_service import review_pull_request

router = APIRouter()


@router.post("/webhook/github")
async def github_webhook(
    request: Request,
    x_hub_signature_256: str | None = Header(default=None),
    x_github_event: str | None = Header(default=None),
):
    """
    Receives GitHub webhook events.
    """

    payload = await request.json()

    print(f"Received GitHub event: {x_github_event}")

    # For now, only process Pull Request events
    if x_github_event != "pull_request":
        return {
            "status": "ignored",
            "event": x_github_event,
        }

    action = payload.get("action")

    print(f"Pull Request action: {action}")

    allowed_actions = {
        "opened",
        "synchronize",
        "reopened",
    }

    if action not in allowed_actions:
        return {
            "status": "ignored",
            "reason": f"PR action '{action}' does not trigger review",
        }

    try:
        result = await review_pull_request(payload)

        return {
            "status": "success",
            "result": result,
        }

    except Exception as exc:
        print(f"MergeMind review failed: {exc}")

        raise HTTPException(
            status_code=500,
            detail="MergeMind review failed",
        )
