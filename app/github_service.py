import httpx

from app.config import settings


class GitHubService:

    def __init__(self):
        self.base_url = "https://api.github.com"

        self.headers = {
            "Authorization": f"Bearer {settings.github_token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        }

    async def get_pull_request(
        self,
        owner: str,
        repo: str,
        pull_number: int,
    ):
        url = (
            f"{self.base_url}/repos/"
            f"{owner}/{repo}/pulls/{pull_number}"
        )

        async with httpx.AsyncClient() as client:

            response = await client.get(
                url,
                headers=self.headers,
            )

        response.raise_for_status()

        return response.json()

    async def get_pull_request_files(
        self,
        owner: str,
        repo: str,
        pull_number: int,
    ):
        url = (
            f"{self.base_url}/repos/"
            f"{owner}/{repo}/pulls/"
            f"{pull_number}/files"
        )

        async with httpx.AsyncClient() as client:

            response = await client.get(
                url,
                headers=self.headers,
            )

        response.raise_for_status()

        return response.json()

    async def create_pull_request_comment(
        self,
        owner: str,
        repo: str,
        pull_number: int,
        comment: str,
    ):
        """
        Creates a general comment on the Pull Request.
        """

        url = (
            f"{self.base_url}/repos/"
            f"{owner}/{repo}/issues/"
            f"{pull_number}/comments"
        )

        data = {
            "body": comment
        }

        async with httpx.AsyncClient() as client:

            response = await client.post(
                url,
                headers=self.headers,
                json=data,
            )

        response.raise_for_status()

        return response.json()
