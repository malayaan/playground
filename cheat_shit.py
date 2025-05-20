Quick context

We are conducting an inspection focused on Société Générale’s overall exposure to the automotive sector, including remarketing practices across business lines.


---

Questions for the Spanish data-science lead

A. Scene-setting

1. Business goal – Which outcome did the model seek to optimise (profit/car, stock days, channel mix)?


2. Stakeholders – Which teams used or sponsored the model (Remarketing, Risk, Finance, IT)?


3. Data scope – Rough size of the dataset (vehicles, years)?



B. Data & features

What minimum data fields were indispensable (VIN, purchase price, mileage, channel, etc.)?

Which optional or nice-to-have variables improved accuracy?

Sources and refresh frequency of those data feeds?

Any external data added (market prices, seasonality, tax rules)?

Biggest data-quality issues (missing VINs, wrong dates, gaps) and how you fixed them?


C. Method

Algorithm(s) chosen and why (XGBoost, RF, survival …)?

How were predictions explained (SHAP, feature importance)?

Validation approach (time split, back-test)?


D. Results & insights

Segments where B2C clearly beats B2B (or reverse)?

Typical gains (€ per car, days saved) from the best channel?

Examples where the model mis-predicted and causes?


E. Transferability

Spain-specific tax or regulatory factors that might limit reuse?

Minimum data volume and granularity needed for robust results in France?

Parts easy to retune vs parts needing rebuild?


F. Deliverables & tools

Notebook, dashboard, or report template you can share?

Data dictionary and reusable cleaning scripts?


G. Lessons learned

Biggest data pitfalls encountered?

Stakeholders to involve early?

One thing you’d change if starting over?


