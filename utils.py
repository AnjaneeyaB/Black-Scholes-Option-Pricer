import QuantLib as ql
import pandas as pd
from numpy import linspace
from plotly.express import imshow

def BSMEuropeanContinuousDiscounting (underlying_spot = 100.0, risk_free_rate = 0.05, volatility = 0.20, time_to_expiry = 1.0, strike_price = 100.0, type = 'call'):
    
    # Initialize today --today's date
    today = ql.Date.todaysDate()
    ql.Settings.instance().evaluationDate = today

    # Initialize expiry date --w.r.t Time-To-Expiry
    expiry_date = today + int(time_to_expiry * 365)

    # Inialize European Option
    option_type = {'call': ql.Option.Call, 'put': ql.Option.Put}[type.lower()]
    option = ql.EuropeanOption(ql.PlainVanillaPayoff(option_type, strike_price),
                            ql.EuropeanExercise(expiry_date))

    # Initialize Engine
    underlying_value = ql.SimpleQuote(underlying_spot)
    risk_free_rate = ql.SimpleQuote(risk_free_rate)
    volatility = ql.SimpleQuote(volatility)
    riskFreeCurve = ql.FlatForward(0,ql.NullCalendar(), ql.QuoteHandle(risk_free_rate), ql.Actual365Fixed(), ql.Continuous)
    volatilityCurve = ql.BlackConstantVol(0, ql.NullCalendar(), ql.QuoteHandle(volatility), ql.Actual365Fixed())

    process = ql.BlackScholesProcess(ql.QuoteHandle(underlying_value), 
                                ql.YieldTermStructureHandle(riskFreeCurve),
                                ql.BlackVolTermStructureHandle(volatilityCurve))
    engine = ql.AnalyticEuropeanEngine(process)

    # Connect option to engine
    option.setPricingEngine(engine)

    return option, underlying_value, volatility

def HeatMap(option, underlying_spot, volatility, min_vol, max_vol, min_spot, max_spot, showscale=False):
    df = pd.DataFrame(
        {
            'volatility': [],
            'spot': [],
            'BS_value': []
        }
    )
    volatility_scale = linspace(min_vol,max_vol,10)
    underlying_spot_scale = linspace(min_spot, max_spot, 10)

    for vol in volatility_scale:
        for spot in underlying_spot_scale:
            volatility.setValue(vol)
            underlying_spot.setValue(spot)
            df.loc[len(df)] = [vol*100, spot, option.NPV()]

    df = df.pivot(index='volatility', columns='spot', values='BS_value')
    df = df.round(2)

    fig = imshow(
        df,
        labels=dict(x="spot", y="volatility(%)", color="BS_value"),
        color_continuous_scale='Viridis',
        text_auto=True
    )
    fig.update_coloraxes(showscale=showscale)
    return fig

if __name__ == '__main__':
    option_data = BSMEuropeanContinuousDiscounting()
    print(option_data[0].NPV())

    option_data[1].setValue(105.0)
    print(option_data[0].NPV())
