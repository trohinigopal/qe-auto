"""Cross-channel journey — no duplicate locators or API payloads.

Web behaviour is driven by Netbanking materialized JSON
(`Netbanking/pageobject/nm/nb_homefinance_emicalc_manual_dom_materialized.json`).

API calls use API materialized JSON
(`API/pageobject/nm/api_my_feature_api_materialized.json`).

Step definitions live in:
- `Netbanking/stepdefination/nm/nb_homefinance_emicalc_manual_step_defs.py`
- `API/stepdefination/nm/api_my_feature_step_defs.py`
"""


class CrossChannelLoginJourney:
    """Optional orchestration helper; BDD steps call runners directly."""

    def __init__(self, web_driver=None, mobile_driver=None, api_client=None) -> None:
        self.web_driver = web_driver
        self.mobile_driver = mobile_driver
        self.api_client = api_client
