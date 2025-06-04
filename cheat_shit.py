region = "US"
list_of_factors = ["Value", "Momentum", "Low Risk", "Growth", "Fund. Quality"]

instruments = [{"name": factor, "region": region} for factor in list_of_factors]

parameters = {
    "source": "Equity Factors",
    "instruments": instruments,
    "fields": ["long", "short"],
    "return_type": 1
}