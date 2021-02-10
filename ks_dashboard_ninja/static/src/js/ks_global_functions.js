odoo.define('ks_dashboard_ninja.KsGlobalFunction', function(require) {
    "use strict";

    var session = require('web.session')

    return {
        ksNumFormatter: function(num, digits) {
            var number = Math.abs(num);
            var sign = Math.sign(num);
            if(number < 1000){
                if (Number.isInteger(number)){
                    return number * sign;
                } else {
                    var result = (number * sign).toFixed(digits).toString().substring(0,digits)
                    if (result[result.length - 1] == '.'){
                        return result.slice(0, -1);
                    }
                    return result;
                }
            } else {
                if (number < 1000000){
                    var div = 1000;
                    var unit = 'K';
                } else if (number < 1000000000){
                    var div = 1000000;
                    var unit = 'M';
                } else if (number < 1000000000000){
                    var div = 1000000000;
                    var unit = 'B'
                }
                var result = (number / div * sign).toFixed(digits).toString().substring(0,digits);
                if (result[result.length - 1] == '.'){
                    return result.slice(0, -1) + unit;
                }
                return result + unit;
            }
        },

        ks_monetary: function(value, currency_id) {
            var currency = session.get_currency(currency_id);
            if (!currency) {
                return value;
            }
            if (currency.position === "after") {
                return value += ' ' + currency.symbol;
            } else {
                return currency.symbol + ' ' + value;
            }
        },
    }

});