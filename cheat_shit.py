parameters = {
    "source": "region",  # exemple: "US"
    "product": "Equity Factors",
    "instruments": [ 
        {
            "name": "Value", 
            "fields": ["long", "short"]
        },
        {
            "name": "Momentum", 
            "fields": ["long", "short"]
        }
    ],
    "return_type": 1
}