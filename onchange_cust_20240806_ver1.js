(function() {
    "use strict";

    // 得意先の更新イベントを登録します
    var events = [
        'app.record.create.change.請求用得意先コード',
        'app.record.edit.change.請求用得意先コード'
    ];

    kintone.events.on(events, function(event) {
        var record = event.record;
        //請求用得意先コード
        var tar = record.請求用得意先コード.value;
        if (tar) {
            // 得意先マスタから情報を取得
            var params = {
                "app": 28, // 得意先マスタ 移行済
                "query": "得意先CD=" + tar
                //'query': '更新日時 > "2012-02-03T09:00:00+0900" and 更新日時 < "2022-02-03T10:00:00+0900" order by レコード番号 asc limit 10 offset 1'
                //"id":tar
                //"query": "\'得意先CD\' = \'" + tar + "\'"
                //'得意先CD': tar
            };
            
            

            kintone.api(kintone.api.url('/k/v1/records.json', true), 'GET', params, function(resp) {
            //kintone.api(kintone.api.url('/k/v1/record', true), 'GET', body, function(resp) {
                // success
                console.log(resp.records[0]);
                
                
          
                
                var obj = kintone.app.record.get();
                obj.record.回収サイクル.value = resp.records[0].ラジオボタン_7.value;
                obj.record.回収日.value = resp.records[0].数値_6.value;
                obj.record.締日.value = resp.records[0].ドロップダウン.value;
                
                //obj.record.回収サイクル.value = resp.record.ラジオボタン_7.value;
                //obj.record.回収日.value = resp.record.数値_6.value;
                //console.log(resp.record.ドロップダウン_1.value);
                //obj.record.回収方法.value = resp.record.ドロップダウン_1.value;
                //console.log(resp.record.ドロップダウン.value);
                //obj.record.締日.value = resp.record.ドロップダウン.value;
                //val_1 = resp.record.ラジオボタン_7.value;
                //val_2 = resp.record.数値_6.value;
                //val_3 = resp.record.ドロップダウン_1.value;
                //val_4 = resp.record.ドロップダウン.value;
                //obj.record.回収サイクル.value = val_1;
                kintone.app.record.set(obj);

                //event.record.回収サイクル.value = val_1;
                //console.log(event.record.回収サイクル.value);
                //console.log(record);
                //console.log(event.record);
            }, function(error) {
                // error
                console.log(error);
            });
        }

        return event;
    });
})();