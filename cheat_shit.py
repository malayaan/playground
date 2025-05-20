Quick context

We are running an inspection on Société Générale’s automotive exposure. One work-stream is to benchmark vehicle-resale performance in two channels—Ayvens (B2B leasing) and CGI (B2C dealer financing)—and to spot the factors that lift margin or shorten time-to-sale.


---

Questions to ask the Spanish data-science lead

A. Broad “setting the scene” questions

1. Business goal – What exact outcome did your model aim to improve (profit per car, stock days, channel mix, …)?


2. Stakeholders – Which teams owned / used the model (Remarketing, Risk, Finance, IT)?


3. Data scope – Roughly how many vehicles and what time span did you cover?



B. Specific follow-ups

Data & features

Which vehicle attributes mattered most (segment, fuel type, age, mileage…)?

Any external data added (market price indices, seasonality, tax incentives)?

Biggest data-quality issues (missing VINs, wrong dates, gaps)?


Method

Which algorithm(s) finally deployed (XGBoost, RF, survival model)?

How did you explain the predictions (SHAP, feature importance)?

Validation setup (train/test split, time-based back-test)?


Results & insights

In which segments does B2C clearly beat B2B—or the reverse?

Typical gains (€/car, days saved) for best-performing channels.

Examples where the model mis-predicted and why.


Transferability

Spain-specific tax or regulatory factors that could limit reuse elsewhere?

Minimum data volume needed for robust results in France.

Parts easy to retune vs parts that need a full rebuild.


Deliverables & tools

Notebook, dashboard, or report template you can share?

Data dictionary available?

Cleaning or preprocessing scripts that can be reused?


Lessons learned

Biggest data pitfalls encountered.

Key stakeholders to involve early.

One thing you would change if starting over.



These questions should give you the technical recipe, practical hurdles, and business value needed to adapt the Spanish model to your French analysis.

