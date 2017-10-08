import dependency_injector.containers as containers
import dependency_injector.providers as providers

from .FinancialSymbolsSource import *
from pprint import pformat


class FinancialSymbol:
    def __init__(self, namespace, ticker, values,
                 isin=None,
                 short_name=None,
                 long_name=None,
                 exchange=None,
                 currency=None,
                 security_type=None,
                 period=None,
                 adjusted_close=None):
        self.namespace = namespace
        self.ticker = ticker
        self.values = values
        self.isin = isin
        self.short_name = short_name
        self.long_name = long_name
        self.exchange = exchange
        self.currency = currency
        self.security_type = security_type
        self.period = period
        self.adjusted_close = adjusted_close

    def values(self):
        return self.values()

    def __repr__(self):
        return pformat(vars(self))


class FinancialSymbolsSourceContainer(containers.DeclarativeContainer):
    currency_usd_rub_source = providers.Singleton(
        SingleFinancialSymbolSource,
        namespace='cbr',
        ticker='USD',
        path='currency/USD-RUB.csv',
        short_name='Доллар США',
        currency=Currency.USD,
        security_type=SecurityType.CURRENCY,
        period=Period.DAY,
        adjusted_close=True
    )

    currency_eur_rub_source = providers.Singleton(
        SingleFinancialSymbolSource,
        namespace='cbr',
        ticker='EUR',
        path='currency/EUR-RUB.csv',
        short_name='Евро',
        currency=Currency.EUR,
        security_type=SecurityType.CURRENCY,
        period=Period.DAY,
        adjusted_close=True
    )

    inflation_ru_source = providers.Singleton(
        SingleFinancialSymbolSource,
        namespace='infl',
        ticker='RU',
        path='inflation_ru/data.csv',
        short_name='Инфляция РФ',
        currency=Currency.RUB,
        security_type=SecurityType.INFLATION,
        period=Period.MONTH,
        adjusted_close=False
    )

    inflation_eu_source = providers.Singleton(
        SingleFinancialSymbolSource,
        namespace='infl',
        ticker='EU',
        path='inflation_eu/data.csv',
        short_name='Инфляция ЕС',
        currency=Currency.EUR,
        security_type=SecurityType.INFLATION,
        period=Period.MONTH,
        adjusted_close=False
    )

    inflation_us_source = providers.Singleton(
        SingleFinancialSymbolSource,
        namespace='infl',
        ticker='US',
        path='inflation_us/data.csv',
        short_name='Инфляция США',
        currency=Currency.USD,
        security_type=SecurityType.INFLATION,
        period=Period.MONTH,
        adjusted_close=False
    )

    cbr_top_rates_source = providers.Singleton(
        SingleFinancialSymbolSource,
        namespace='cbr',
        ticker='TOP_rates',
        path='cbr_deposit_rate/data.csv',
        long_name='Динамика максимальной процентной ставки (по вкладам в российских рублях) ',
        currency=Currency.RUB,
        security_type=SecurityType.RATES,
        period=Period.DECADE,
        adjusted_close=False
    )

    micex_mcftr_source = providers.Singleton(
        SingleFinancialSymbolSource,
        namespace='micex',
        ticker='MCFTR',
        path='moex/mcftr/data.csv',
        short_name='MICEX Total Return',
        currency=Currency.RUB,
        security_type=SecurityType.INDEX,
        period=Period.DAY,
        adjusted_close=False
    )

    micex_stocks_source = providers.Singleton(MicexStocksFinancialSymbolsSource)

    nlu_muts_source = providers.Singleton(NluFinancialSymbolsSource)

    financial_symbols_registry = providers.Singleton(
        FinancialSymbolsRegistry,
        symbol_sources=[
            currency_usd_rub_source(),
            currency_eur_rub_source(),
            cbr_top_rates_source(),
            inflation_ru_source(),
            inflation_eu_source(),
            inflation_us_source(),
            micex_mcftr_source(),
            micex_stocks_source(),
            nlu_muts_source(),
        ]
    )