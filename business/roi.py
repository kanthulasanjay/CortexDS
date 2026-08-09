class ROIEstimator:

    def estimate(

        self,

        customers,

        avg_loss,

        accuracy

    ):

        prevented_defaults = (

            customers

            * (accuracy * 0.25)

        )

        savings = (

            prevented_defaults

            * avg_loss

        )

        roi = {

            "customers": customers,

            "estimated_prevented_defaults":

                int(prevented_defaults),

            "estimated_savings":

                round(savings,2)

        }

        return roi