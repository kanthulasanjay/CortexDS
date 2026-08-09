class DecisionSimulator:

    def simulate(

        self,

        threshold

    ):

        if threshold < 0.5:

            return {

                "risk":"HIGH",

                "approvals":"VERY HIGH"

            }

        elif threshold < 0.7:

            return {

                "risk":"MEDIUM",

                "approvals":"HIGH"

            }

        return {

            "risk":"LOW",

            "approvals":"LOW"

        }