# v0.1.0
# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }

from genlayer import *

class FactChecker(gl.Contract):
    last_claim: str
    last_verdict: str

    def __init__(self):
        self.last_claim = ""
        self.last_verdict = ""

    @gl.public.view
    def get_last_check(self) -> str:
        return self.last_claim + "|" + self.last_verdict

    @gl.public.write
    def check_fact(self, claim: str) -> None:
        web_result = gl.get_webpage(
            "https://en.wikipedia.org/wiki/" + claim.replace(" ", "_"),
            mode="text"
        )
        verdict = gl.eq_principle_prompt_non_comparative(
            f"Based on: {web_result[:1000]}\nIs this TRUE or FALSE: {claim}\nRespond only TRUE or FALSE.",
            principle="Answer only TRUE or FALSE"
        )
        self.last_claim = claim
        self.last_verdict = verdict.strip()[:5]
