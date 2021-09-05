    def _really_act_on_signal(self):
        """
        aqui eu tenho que
        1) mudar o sinal de entrada pra incluir as duas direçoes
        2) essa é a função que faz os trades, efetivamente. falta isso
        """

        if not self.is_positioned:
            if self.strategy.entry_signal(self):
                self.send_order()
                self._change_position()
        else:

            self._set_current_profits()

            if self.tp_order["status"] == "FILLED":
                self.exit_price = float(self.tp_order["avgPrice"])
                self.qty = self.tp_order["executedQty"]
                self.exit_time = to_datetime_tz(
                    self.tp_order["updateTime"], unit="ms")
                self._set_actual_profits()
                self._register_trade_data(f"TP")
                self._change_position()
                self.entry_price = None

    def send_order(self, protect=False):

        if self.position_type == -1:
            side = "SELL"
            counterside = "BUY"
        elif self.position_type == 1:
            side = "BUY"
            counterside = "SELL"

        try:
            new_position = self.client.futures_create_order(
                symbol=self.symbol,
                side=side,
                type="MARKET",
                quantity=self.qty,
                priceProtect=protect,
                workingType="CONTRACT_PRICE",
            )

        except BinanceAPIException as error:
            print(type(error))
            print("positioning, ", error)
        else:
            self.position = self.client.futures_position_information(
                symbol=self.symbol)
            self.entry_price = float(self.position[0]["entryPrice"])
            tp_price = self.price_formatter(
                self.entry_price + self.entry_price * self.take_profit/100)

            try:
                self.tp_order = self.client.futures_create_order(
                    symbol=self.symbol,
                    side=counterside,
                    type="TAKE_PROFIT_MARKET",
                    stopPrice=tp_price,
                    workingType="CONTRACT_PRICE",
                    quantity=self.qty,
                    reduceOnly=True,
                    priceProtect=protect,
                    timeInForce="GTE_GTC",
                )
            except BinanceAPIException as error:

                print(type(error))
                print("tp order, ", error)
