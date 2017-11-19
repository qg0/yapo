import unittest

import yapo
from model.Enums import Currency
import numpy as np
import itertools


class CurrencyConversionTest(unittest.TestCase):

    def test_currency_should_not_be_converted_to_itself_inside_converter(self):
        from model.FinancialSymbolsSourceContainer import FinancialSymbolsSourceContainer
        csr = FinancialSymbolsSourceContainer.currency_symbols_registry()
        for cur in Currency:
            dt = csr.convert(currency_from=cur, currency_to=cur)
            vs = dt['close'].values
            self.assertTrue(np.all(np.abs(vs - 1.) < 1e-3))

    def test_currency_should_not_be_converted_to_itself_inside_datatable(self):
        for cur in Currency:
            vs = yapo.portfolio(assets=[('cbr/' + cur.name, 1.)],
                                start_period='2015-1', end_period='2017-1',
                                currency=cur.name).assets[0].close()

            self.assertTrue(np.all(np.abs(vs - 1.) < 1e-3))

    def test_currency_should_be_converted_other_currency(self):
        vs = yapo.portfolio(assets=[('cbr/EUR', 1.)],
                            start_period='2015-1', end_period='2017-1',
                            currency='USD').assets[0].close()

        self.assertTrue(np.all(vs > 1.05))

    def test_support_all_types_of_currency_conversions(self):
        for currency_from, currency_to in itertools.product(Currency, Currency):
            vs = yapo.portfolio(assets=[('cbr/' + currency_from.name, 1.)],
                                start_period='2015-1', end_period='2016-12',
                                currency=currency_to.name).assets[0].close()

            self.assertEqual(vs.size, 2 * 12)
            self.assertTrue(np.all(vs > 0.))

    def test_currency_conversion_should_be_inversive(self):
        for currency1, currency2 in itertools.product(Currency, Currency):
            vs1 = yapo.portfolio(assets=[('cbr/' + currency1.name, 1.)],
                                 start_period='2015-1', end_period='2016-12',
                                 currency=currency2.name).assets[0].close()

            vs2 = yapo.portfolio(assets=[('cbr/' + currency2.name, 1.)],
                                 start_period='2015-1', end_period='2016-12',
                                 currency=currency1.name).assets[0].close()

            self.assertTrue(np.all(np.abs(vs1 * vs2 - 1.) < 1e-3))

    def test_asset_should_be_converted_correctly(self):
        vs_eur = yapo.portfolio(assets=[('nlu/630', 1.)],
                                start_period='2011-1', end_period='2017-2',
                                currency='EUR').assets[0].close()

        vs_usd = yapo.portfolio(assets=[('nlu/630', 1.)],
                                start_period='2011-1', end_period='2017-2',
                                currency='USD').assets[0].close()

        vs_curr = yapo.portfolio(assets=[('cbr/USD', 1.)],
                                 start_period='2011-1', end_period='2017-2',
                                 currency='EUR').assets[0].close()

        self.assertTrue(np.all(np.abs(vs_eur / vs_usd - vs_curr) < 1e-3))