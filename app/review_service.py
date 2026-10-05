from pathlib import Path

from app.ai_service import AIService
from app.github_service import GitHubService


PROMPT_FILE = (
    Path(__file__).parent.parent
    / "prompts"
    / "code_review.txt"
)


def load_prompt_template() -> str:

    return PROMPT_FILE.read_text(
        encoding="utf-8"
    )


def build_review_prompt(
    template: str,
    pull_request: dict,
    files: list,
) -> str:

    title = pull_request.get(
        "title",
        "",
    )

    description = pull_request.get(
        "body",
        "",
    )

    diff_text = ""

    for file in files:

        filename = file.get(
            "filename",
            "",
        )

        patch = file.get(
            "patch",
            "",
        )

        diff_text += f"""
==================================================
File: {filename}
==================================================

{patch}

"""

    prompt = template.format(
        pr_title=title,
        pr_description=description,
        diff=diff_text,
    )

    return prompt


async def review_pull_request(
    payload: dict,
):

    repository = payload.get(
        "repository",
        {},
    )

    pull_request = payload.get(
        "pull_request",
        {},
    )

    owner = repository.get(
        "owner",
        {},
    ).get(
        "login"
    )

    repo = repository.get(
        "name"
    )

    pull_number = pull_request.get(
        "number"
    )

    if not owner or not repo or not pull_number:

        raise ValueError(
            "Could not determine GitHub repository "
            "or Pull Request number"
        )

    print(
        f"Processing GitHub repository="
        f"{owner}/{repo}, PR={pull_number}"
    )

    github = GitHubService()

    # 1. Get PR details

    pr_details = await github.get_pull_request(
        owner,
        repo,
        pull_number,
    )

    # 2. Get changed files

    files = await github.get_pull_request_files(
        owner,
        repo,
        pull_number,
    )

    # 3. Build AI prompt

    template = load_prompt_template()

    prompt = build_review_prompt(
        template,
        pr_details,
        files,
    )

    # 4. AI analysis

    ai_service = AIService()

    review = await ai_service.review_code(
        prompt
    )

    # 5. Format GitHub comment

    comment = f"""## 🤖 MergeMind Code Review

{review}

---

*This review was generated automatically by MergeMind.*
"""

    # 6. Post comment

    result = await github.create_pull_request_comment(
        owner,
        repo,
        pull_number,
        comment,
    )

    return {
        "repository": f"{owner}/{repo}",
        "pull_request": pull_number,
        "comment_id": result.get("id"),
    }
