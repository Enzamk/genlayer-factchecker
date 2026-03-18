# v0.1.0
# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }

from genlayer import *

class FactChecker(gl.Contract):
    checks: list

    def __init__(self):
        self.checks = []

    @gl.public.view
    def get_checks(self) -> list:
        return self.checks

    @gl.public.write
    def check_fact(self, claim: str) -> None:
        web_result = gl.get_webpage("https://www.google.com/search?q=" + claim.replace(" ", "+"), mode="text")

        result = gl.eq_principle_prompt_comparative(
            f"""
            Based on this web search result:
            {web_result[:2000]}

            Is this claim TRUE or FALSE: "{claim}"

            Respond with ONLY a JSON object like this:
            {{"verdict": "TRUE", "reason": "brief explanation"}}
            or
            {{"verdict": "FALSE", "reason": "brief explanation"}}
            """,
            principle="The verdict and reason must be consistent with the web evidence"
        )

        import json
        parsed = json.loads(result)
        self.checks.append({
            "claim": claim,
            "verdict": parsed["verdict"],
            "reason": parsed["reason"]
        })
