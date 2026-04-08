"""Rentabilitätskennzahlen und ihre Zerlegung."""


def return_on_sales(profit, revenue):
    """Die Umsatzrendite.

    Raises:
        ValueError: bei einem nicht positiven Umsatz.
    """
    if revenue <= 0:
        raise ValueError("der Umsatz muss positiv sein")
    return profit / revenue


def asset_turnover(revenue, assets):
    """Der Kapitalumschlag.

    Raises:
        ValueError: bei einer nicht positiven Bilanzsumme.
    """
    if assets <= 0:
        raise ValueError("die Bilanzsumme muss positiv sein")
    return revenue / assets


def return_on_assets(profit, assets):
    """Die Gesamtkapitalrentabilität.

    Raises:
        ValueError: bei einer nicht positiven Bilanzsumme.
    """
    if assets <= 0:
        raise ValueError("die Bilanzsumme muss positiv sein")
    return profit / assets


def return_on_equity(profit, equity):
    """Die Eigenkapitalrentabilität.

    Raises:
        ValueError: bei einem nicht positiven Eigenkapital.
    """
    if equity <= 0:
        raise ValueError("das Eigenkapital muss positiv sein")
    return profit / equity


def du_pont(profit, revenue, assets, equity):
    """Zerlegt die Eigenkapitalrentabilität in drei Faktoren.

    Umsatzrendite mal Kapitalumschlag mal Kapitalstruktur ergibt die
    Eigenkapitalrentabilität. Die Zerlegung ist rechnerisch trivial und
    inhaltlich der ganze Punkt: dieselbe Rendite entsteht aus hoher
    Marge oder aus hohem Umschlag oder aus viel Fremdkapital, und das
    sind drei verschiedene Unternehmen.

    Returns:
        Abbildung mit den drei Faktoren und der Probe.

    Raises:
        ValueError: bei nicht positiven Nennern.
    """
    margin = return_on_sales(profit, revenue)
    turnover = asset_turnover(revenue, assets)
    leverage = assets / equity if equity > 0 else None
    if leverage is None:
        raise ValueError("das Eigenkapital muss positiv sein")
    product = margin * turnover * leverage
    direct = return_on_equity(profit, equity)
    return {"margin": margin, "turnover": turnover, "leverage": leverage,
            "product": product, "direct": direct,
            "agree": abs(product - direct) < 1e-9}


def leverage_effect(profit_before_interest, assets, equity, rate):
    """Rechnet den Hebeleffekt aus.

    Solange die Gesamtkapitalrentabilität über dem Fremdkapitalzins
    liegt, hebt zusätzliches Fremdkapital die Eigenkapitalrentabilität.
    Liegt sie darunter, wirkt derselbe Hebel nach unten, und zwar mit
    demselben Faktor. Der Hebel erhöht nicht die Rendite, er erhöht die
    Streuung.

    Raises:
        ValueError: bei einem nicht positiven Eigenkapital oder einer
            Bilanzsumme unter dem Eigenkapital.
    """
    if equity <= 0:
        raise ValueError("das Eigenkapital muss positiv sein")
    if assets < equity:
        raise ValueError("die Bilanzsumme liegt unter dem Eigenkapital")
    debt = assets - equity
    total_return = profit_before_interest / assets
    interest = debt * rate
    equity_return = (profit_before_interest - interest) / equity
    return {"return on assets": total_return, "interest rate": rate,
            "return on equity": equity_return,
            "leverage works": total_return > rate,
            "amplification": debt / equity,
            "rule": "der Hebel wirkt in beide Richtungen gleich stark"}


def the_same_return_three_ways():
    """Zeigt drei Unternehmen mit derselben Eigenkapitalrendite.

    Eines verdient an der Marge, eines am Umschlag, eines am
    Fremdkapital. Die Kennzahl ist dieselbe, das Risiko nicht, und wer
    nur die Kennzahl vergleicht, hält die drei für gleich.

    Returns:
        Abbildung mit den drei Zerlegungen.
    """
    cases = {
        "hohe Marge": du_pont(200.0, 1000.0, 2000.0, 1000.0),
        "hoher Umschlag": du_pont(200.0, 5000.0, 2000.0, 1000.0),
        "viel Fremdkapital": du_pont(100.0, 2000.0, 4000.0, 500.0),
    }
    return {name: {"margin": round(row["margin"], 4),
                   "turnover": round(row["turnover"], 4),
                   "leverage": round(row["leverage"], 4),
                   "return on equity": round(row["direct"], 4)}
            for name, row in cases.items()}


def why_the_denominator_is_contested():
    """Nennt, worüber bei jeder Rentabilität gestritten wird.

    Welcher Gewinn, welches Kapital und welcher Zeitpunkt. Vor oder nach
    Zinsen, vor oder nach Steuern; Kapital zum Stichtag oder im
    Durchschnitt; Eigenkapital mit oder ohne stille Reserven. Jede
    Antwort ist vertretbar, und zwei vertretbare Antworten ergeben
    Kennzahlen, die sich nicht vergleichen lassen. Deshalb steht bei
    einer veröffentlichten Rendite die Definition dabei, oder sie taugt
    nichts.
    """
    return {"which profit": ["vor oder nach Zinsen",
                             "vor oder nach Steuern"],
            "which capital": ["Stichtag oder Durchschnitt",
                              "mit oder ohne stille Reserven"],
            "consequence": "zwei vertretbare Definitionen ergeben "
                           "unvergleichbare Zahlen",
            "rule": "ohne Definition ist eine veröffentlichte Rendite "
                    "wertlos"}
