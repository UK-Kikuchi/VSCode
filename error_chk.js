(function() {
    "use strict";

    // ***** ▽ レコード保存前 ▽ *****
    kintone.events.on(['app.record.create.submit', 'app.record.edit.submit'], function(event) {
        var record = event.record;
        if (record['売上台帳登録'].value == '済') {
            record['売上台帳登録'].error = '売上台帳登録済の受注です。';
        }
        return event;
    });
})();