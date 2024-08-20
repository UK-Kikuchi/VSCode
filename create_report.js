(function() {
    'use strict';
    // ***** ▽ 新規登録 ▽ *****
    kintone.events.on('app.record.create.submit.success', function(event) {
        // ※※　権限チェック
        var user = kintone.getLoginUser();
        console.log('User:' + user.id);
        if (user.id == '5') {
            console.log('制限ユーザの為処理をスキップしました。');
            return event;
        }

        var record = event.record;
        // ▼ *** 登録処理 *** ▼
        var itm1 = record.商品コード１.value;
        var itm_1 = record.自由品名_1.value;
        if (itm1 !== "" || itm_1 !== "") {
            // ▼▼ 売上台帳登録処理 ▼▼
            var params = {
                "app": 37, // 移行済
                "record": {
                    "status": { "value": record.ラジオボタン.value }, // ステイタス
                    "order_id": { "value": event.record.$id.value }, // 受注レコード番号 
                    "order_no": { "value": record.受注NO.value }, // 受注No
                    "order_ymd": { "value": record.日付_2.value }, // 受注日
                    "nouki_ymd": { "value": record.納期.value }, // 納期
                    "syukka_ymd": { "value": record.出荷日.value }, // 出荷日
                    "bun_1": { "value": record.bun1.value }, // 分類１
                    "bun_2": { "value": record.bun2.value }, // 分類２
                    "bun_3": { "value": record.bun3.value }, // 分類３
                    "order_person": { "value": record.tanto.value }, // 受注担当
                    "sales_person": { "value": record.ドロップダウン_1.value }, // 営業担当
                    "tokui_id": { "value": record.ルックアップ.value }, // 得意先
                    "nounyu_id": { "value": record.ルックアップ_10.value }, // 納入先
                    // ↓　新規追加　↓
                    "tokui_nm": { "value": record.得意先名.value }, // 得意先名
                    "tokui_dept": { "value": record.得意先部署.value }, // 得意先部署
                    "nounyu_nm": { "value": record.納入先名.value }, // 納入先名
                    "nounyu_dept": { "value": record.納入先部署.value }, // 納入部署
                    "pre_tokui_id": { "value": record.親得意先コード.value }, // 得意先名
                    "pre_tokui_nm": { "value": record.親得意先.value }, // 納入先名
                    // ↓ 明細項目 ↓
                    "item": { "value": record.商品コード１.value }, // 品番
                    "item_nm1": { "value": record.名称１.value }, // 品名
                    "item_nm2": { "value": record.自由品名_1.value }, // 品名（自由記入）
                    "keijyo": { "value": record.粉液_1.value }, // 粉／液体
                    "nisugata": { "value": record.荷姿_1.value }, // 荷姿
                    "qty": { "value": record.数量_1.value }, // 数量
                    "yoryo": { "value": record.容量１.value }, // 容量
                    "unit": { "value": record.単位１.value }, // 単位
                    "price": { "value": record.単価１.value }, // 単価
                    "sum": { "value": record.計算１.value }, // 小計
                    "rmk": { "value": record.備考１.value }, // 備考
                    "tax_rate": { "value": record.taxlate_1.value }, // 税率
                    "tax_cdn": { "value": record.taxcon_1.value }, // 税調整
                    "tax": { "value": record.taxamt_1.value }, // 税額
                    // ↓↓↓ 明細新規追加（商事品関連） ↓↓↓↓
                    "s_flg": { "value": record.s_flg_1.value }, // 商事品フラグ
                    "s_shu": { "value": record.s_shu_1.value } // 商事品種別

                }
            };

            console.log(params.record);
            // kintone REST API リクエスト ～ レコードの登録（POST）
            kintone.api(
                kintone.api.url('/k/v1/record', true), // - pathOrUrl
                'POST', // - method
                params, // - params
                function(resp) { // - callback
                    //window.alert('成功1');
                    // (特に何もしない)
                },
                function(resp) { // - errback
                    window.alert('システムエラーが発生しました、しばらくしてから再度更新してください。（INS001）');
                    // (特に何もしない)
                }
            );
            // ▲▲ 売上台帳登録処理 ▲▲  
        }
        var itm2 = record.商品コード２.value;
        var itm_2 = record.自由品名_2.value;
        if (itm2 !== "" || itm_2 !== "") {
            // ▼▼ 売上台帳登録処理 ▼▼
            var params = {
                "app": 37, // ← 移行済
                "record": {
                    "status": { "value": record.ラジオボタン.value }, // ステイタス
                    "order_id": { "value": event.record.$id.value }, // 受注レコード番号 
                    "order_no": { "value": record.受注NO.value }, // 受注No
                    "order_ymd": { "value": record.日付_2.value }, // 受注日
                    "nouki_ymd": { "value": record.納期.value }, // 納期
                    "syukka_ymd": { "value": record.出荷日.value }, // 出荷日
                    "bun_1": { "value": record.bun1.value }, // 分類１
                    "bun_2": { "value": record.bun2.value }, // 分類２
                    "bun_3": { "value": record.bun3.value }, // 分類３
                    "order_person": { "value": record.tanto.value }, // 受注担当
                    "sales_person": { "value": record.ドロップダウン_1.value }, // 営業担当
                    "tokui_id": { "value": record.ルックアップ.value }, // 得意先
                    "nounyu_id": { "value": record.ルックアップ_10.value }, // 納入先
                    // ↓　新規追加　↓
                    "tokui_nm": { "value": record.得意先名.value }, // 得意先名
                    "tokui_dept": { "value": record.得意先部署.value }, // 得意先部署
                    "nounyu_nm": { "value": record.納入先名.value }, // 納入先名
                    "nounyu_dept": { "value": record.納入先部署.value }, // 納入部署
                    "pre_tokui_id": { "value": record.親得意先コード.value }, // 得意先名
                    "pre_tokui_nm": { "value": record.親得意先.value }, // 納入先名
                    // ↓ 明細項目 ↓
                    "item": { "value": record.商品コード２.value }, // 品番
                    "item_nm1": { "value": record.名称２.value }, // 品名
                    "item_nm2": { "value": record.自由品名_2.value }, // 品名（自由記入）
                    "keijyo": { "value": record.粉液_2.value }, // 粉／液体
                    "nisugata": { "value": record.荷姿_2.value }, // 荷姿
                    "qty": { "value": record.数量_2.value }, // 数量
                    "yoryo": { "value": record.容量２.value }, // 容量
                    "unit": { "value": record.単位２.value }, // 単位
                    "price": { "value": record.単価２.value }, // 単価
                    "sum": { "value": record.計算２.value }, // 小計
                    "rmk": { "value": record.備考２.value }, // 備考
                    "tax_rate": { "value": record.taxlate_2.value }, // 税率
                    "tax_cdn": { "value": record.taxcon_2.value }, // 税調整
                    "tax": { "value": record.taxamt_2.value }, // 税額
                    // ↓↓↓ 明細新規追加（商事品関連） ↓↓↓↓
                    "s_flg": { "value": record.s_flg_2.value }, // 商事品フラグ
                    "s_shu": { "value": record.s_shu_2.value } // 商事品種別
                }
            };

            // kintone REST API リクエスト ～ レコードの登録（POST）
            kintone.api(
                kintone.api.url('/k/v1/record', true), // - pathOrUrl
                'POST', // - method
                params, // - params
                function(resp) { // - callback
                    //window.alert('成功2');
                    // (特に何もしない)
                },
                function(resp) { // - errback
                    window.alert('システムエラーが発生しました、しばらくしてから再度更新してください。（INS002）');
                    // (特に何もしない)
                }
            );
            // ▲▲ 売上台帳登録処理 ▲▲  
        }
        var itm3 = record.商品コード３.value;
        var itm_3 = record.自由品名_3.value;
        if (itm3 !== "" || itm_3 !== "") {
            // ▼▼ 売上台帳登録処理 ▼▼
            var params = {
                "app": 37, // 移行済
                "record": {
                    "status": { "value": record.ラジオボタン.value }, // ステイタス
                    "order_id": { "value": event.record.$id.value }, // 受注レコード番号 
                    "order_no": { "value": record.受注NO.value }, // 受注No
                    "order_ymd": { "value": record.日付_2.value }, // 受注日
                    "nouki_ymd": { "value": record.納期.value }, // 納期
                    "syukka_ymd": { "value": record.出荷日.value }, // 出荷日
                    "bun_1": { "value": record.bun1.value }, // 分類１
                    "bun_2": { "value": record.bun2.value }, // 分類２
                    "bun_3": { "value": record.bun3.value }, // 分類３
                    "order_person": { "value": record.tanto.value }, // 受注担当
                    "sales_person": { "value": record.ドロップダウン_1.value }, // 営業担当
                    "tokui_id": { "value": record.ルックアップ.value }, // 得意先
                    "nounyu_id": { "value": record.ルックアップ_10.value }, // 納入先
                    // ↓　新規追加　↓
                    "tokui_nm": { "value": record.得意先名.value }, // 得意先名
                    "tokui_dept": { "value": record.得意先部署.value }, // 得意先部署
                    "nounyu_nm": { "value": record.納入先名.value }, // 納入先名
                    "nounyu_dept": { "value": record.納入先部署.value }, // 納入部署
                    "pre_tokui_id": { "value": record.親得意先コード.value }, // 得意先名
                    "pre_tokui_nm": { "value": record.親得意先.value }, // 納入先名
                    // ↓ 明細項目 ↓
                    "item": { "value": record.商品コード３.value }, // 品番
                    "item_nm1": { "value": record.名称３.value }, // 品名
                    "item_nm2": { "value": record.自由品名_3.value }, // 品名（自由記入）
                    "keijyo": { "value": record.粉液_3.value }, // 粉／液体
                    "nisugata": { "value": record.荷姿_3.value }, // 荷姿
                    "qty": { "value": record.数量_3.value }, // 数量
                    "yoryo": { "value": record.容量３.value }, // 容量
                    "unit": { "value": record.単位３.value }, // 単位
                    "price": { "value": record.単価３.value }, // 単価
                    "sum": { "value": record.計算３.value }, // 小計
                    "rmk": { "value": record.備考３.value }, // 備考
                    "tax_rate": { "value": record.taxlate_3.value }, // 税率
                    "tax_cdn": { "value": record.taxcon_3.value }, // 税調整
                    "tax": { "value": record.taxamt_3.value }, // 税額
                    // ↓↓↓ 明細新規追加（商事品関連） ↓↓↓↓
                    "s_flg": { "value": record.s_flg_3.value }, // 商事品フラグ
                    "s_shu": { "value": record.s_shu_3.value } // 商事品種別
                }
            };

            // kintone REST API リクエスト ～ レコードの登録（POST）
            kintone.api(
                kintone.api.url('/k/v1/record', true), // - pathOrUrl
                'POST', // - method
                params, // - params
                function(resp) { // - callback
                    // window.alert('成功3');
                    // (特に何もしない)
                },
                function(resp) { // - errback
                    window.alert('システムエラーが発生しました、しばらくしてから再度更新してください。（INS003）');
                    // (特に何もしない)
                }
            );
            // ▲▲ 売上台帳登録処理 ▲▲  
        }
        var itm4 = record.商品コード４.value;
        var itm_4 = record.自由品名_4.value;
        if (itm4 !== "" || itm_4 !== "") {
            // ▼▼ 売上台帳登録処理 ▼▼
            var params = {
                "app": 37, // 移行済
                "record": {
                    "status": { "value": record.ラジオボタン.value }, // ステイタス
                    "order_id": { "value": event.record.$id.value }, // 受注レコード番号 
                    "order_no": { "value": record.受注NO.value }, // 受注No
                    "order_ymd": { "value": record.日付_2.value }, // 受注日
                    "nouki_ymd": { "value": record.納期.value }, // 納期
                    "syukka_ymd": { "value": record.出荷日.value }, // 出荷日
                    "bun_1": { "value": record.bun1.value }, // 分類１
                    "bun_2": { "value": record.bun2.value }, // 分類２
                    "bun_3": { "value": record.bun3.value }, // 分類３
                    "order_person": { "value": record.tanto.value }, // 受注担当
                    "sales_person": { "value": record.ドロップダウン_1.value }, // 営業担当
                    "tokui_id": { "value": record.ルックアップ.value }, // 得意先
                    "nounyu_id": { "value": record.ルックアップ_10.value }, // 納入先
                    // ↓　新規追加　↓
                    "tokui_nm": { "value": record.得意先名.value }, // 得意先名
                    "tokui_dept": { "value": record.得意先部署.value }, // 得意先部署
                    "nounyu_nm": { "value": record.納入先名.value }, // 納入先名
                    "nounyu_dept": { "value": record.納入先部署.value }, // 納入部署
                    "pre_tokui_id": { "value": record.親得意先コード.value }, // 得意先名
                    "pre_tokui_nm": { "value": record.親得意先.value }, // 納入先名
                    // ↓ 明細項目 ↓
                    "item": { "value": record.商品コード４.value }, // 品番
                    "item_nm1": { "value": record.名称４.value }, // 品名
                    "item_nm2": { "value": record.自由品名_4.value }, // 品名（自由記入）
                    "keijyo": { "value": record.粉液_4.value }, // 粉／液体
                    "nisugata": { "value": record.荷姿_4.value }, // 荷姿
                    "qty": { "value": record.数量_4.value }, // 数量
                    "yoryo": { "value": record.容量４.value }, // 容量
                    "unit": { "value": record.単位４.value }, // 単位
                    "price": { "value": record.単価４.value }, // 単価
                    "sum": { "value": record.計算４.value }, // 小計
                    "rmk": { "value": record.備考４.value }, // 備考
                    "tax_rate": { "value": record.taxlate_4.value }, // 税率
                    "tax_cdn": { "value": record.taxcon_4.value }, // 税調整
                    "tax": { "value": record.taxamt_4.value }, // 税額
                    // ↓↓↓ 明細新規追加（商事品関連） ↓↓↓↓
                    "s_flg": { "value": record.s_flg_4.value }, // 商事品フラグ
                    "s_shu": { "value": record.s_shu_4.value } // 商事品種別
                }
            };


            // kintone REST API リクエスト ～ レコードの登録（POST）
            kintone.api(
                kintone.api.url('/k/v1/record', true), // - pathOrUrl
                'POST', // - method
                params, // - params
                function(resp) { // - callback
                    //window.alert('成功4');
                    // (特に何もしない)
                },
                function(resp) { // - errback
                    window.alert('システムエラーが発生しました、しばらくしてから再度更新してください。（INS004）');
                    // (特に何もしない)
                }
            );
            // ▲▲ 売上台帳登録処理 ▲▲  
        }
        var itm5 = record.商品コード５.value;
        var itm_5 = record.自由品名_5.value;
        if (itm5 !== "" || itm_5 !== "") {
            // ▼▼ 売上台帳登録処理 ▼▼
            var params = {
                "app": 37, // 移行済
                "record": {
                    "status": { "value": record.ラジオボタン.value }, // ステイタス
                    "order_id": { "value": event.record.$id.value }, // 受注レコード番号 
                    "order_no": { "value": record.受注NO.value }, // 受注No
                    "order_ymd": { "value": record.日付_2.value }, // 受注日
                    "nouki_ymd": { "value": record.納期.value }, // 納期
                    "syukka_ymd": { "value": record.出荷日.value }, // 出荷日
                    "bun_1": { "value": record.bun1.value }, // 分類１
                    "bun_2": { "value": record.bun2.value }, // 分類２
                    "bun_3": { "value": record.bun3.value }, // 分類３
                    "order_person": { "value": record.tanto.value }, // 受注担当
                    "sales_person": { "value": record.ドロップダウン_1.value }, // 営業担当
                    "tokui_id": { "value": record.ルックアップ.value }, // 得意先
                    "nounyu_id": { "value": record.ルックアップ_10.value }, // 納入先
                    // ↓　新規追加　↓
                    "tokui_nm": { "value": record.得意先名.value }, // 得意先名
                    "tokui_dept": { "value": record.得意先部署.value }, // 得意先部署
                    "nounyu_nm": { "value": record.納入先名.value }, // 納入先名
                    "nounyu_dept": { "value": record.納入先部署.value }, // 納入部署
                    "pre_tokui_id": { "value": record.親得意先コード.value }, // 得意先名
                    "pre_tokui_nm": { "value": record.親得意先.value }, // 納入先名
                    // ↓ 明細項目 ↓
                    "item": { "value": record.商品コード５.value }, // 品番
                    "item_nm1": { "value": record.名称５.value }, // 品名
                    "item_nm2": { "value": record.自由品名_5.value }, // 品名（自由記入）
                    "keijyo": { "value": record.粉液_5.value }, // 粉／液体
                    "nisugata": { "value": record.荷姿_5.value }, // 荷姿
                    "qty": { "value": record.数量_5.value }, // 数量
                    "yoryo": { "value": record.容量５.value }, // 容量
                    "unit": { "value": record.単位５.value }, // 単位
                    "price": { "value": record.単価５.value }, // 単価
                    "sum": { "value": record.計算５.value }, // 小計
                    "rmk": { "value": record.備考５.value }, // 備考
                    "tax_rate": { "value": record.taxlate_5.value }, // 税率
                    "tax_cdn": { "value": record.taxcon_5.value }, // 税調整
                    "tax": { "value": record.taxamt_5.value }, // 税額
                    // ↓↓↓ 明細新規追加（商事品関連） ↓↓↓↓
                    "s_flg": { "value": record.s_flg_5.value }, // 商事品フラグ
                    "s_shu": { "value": record.s_shu_5.value } // 商事品種別
                }
            };

            // kintone REST API リクエスト ～ レコードの登録（POST）
            kintone.api(
                kintone.api.url('/k/v1/record', true), // - pathOrUrl
                'POST', // - method
                params, // - params
                function(resp) { // - callback
                    //window.alert('成功5');
                    // (特に何もしない)
                },
                function(resp) { // - errback
                    window.alert('システムエラーが発生しました、しばらくしてから再度更新してください。（INS005）');
                    // (特に何もしない)
                }
            );
            // ▲▲ 売上台帳登録処理 ▲▲  
        }
        // ▲ *** 登録処理 *** ▲

        //console.log('レコードID： ' + record.$id.value + ' で保存しました。');
        //console.log('パラメーター：' + params);
        //window.alert('※新規登録 レコードID： ' + record.$id.value + ' で保存しました。');
        return event;
    });

    // ***** 更新処理 *****
    kintone.events.on('app.record.edit.submit.success', function(event) {

        // ※※　権限チェック
        var user = kintone.getLoginUser();
        console.log('User:' + user.id);
        if (user.id == '5') {
            console.log('制限ユーザの為処理をスキップしました。');
            return event;
        }

        var record = event.record;
        var ids = [];
        // ▼▼ 売上台帳削除処理 ▼▼

        // ▼▼▼ 受注番号から削除対象を取得 ▼▼▼
        var body = {
            'app': 37, // 移行済
            'query': 'order_id = ' + event.record.$id.value,
            'fields': ['レコード番号']
        };

        kintone.api(kintone.api.url('/k/v1/records.json', true), 'GET', body, function(resp) {
            // success
            console.log(resp);
            for (var i = 0; i < resp.records.length; i++) {
                ids.push(Number(resp.records[i].レコード番号.value));
                //console.log(resp.records[i].レコード番号.value);
            }
            console.log(ids);
            if (ids != '') {
                //console.log(ids);
                var body = {
                    'app': 37, //移行済
                    'ids': ids
                };

                kintone.api(kintone.api.url('/k/v1/records.json', true), 'DELETE', body, function(resp) {
                    // success
                    console.log(resp);
                    // window.alert('削除成功');
                }, function(error) {
                    // error
                    console.log(error);
                    window.alert('システムエラーが発生しました、しばらくしてから再度更新してください。（UPD-DEL）');
                });
            }
        }, function(error) {
            // error
            console.log(error);
            //window.alert('取得失敗');
        });
        // ▲▲ 売上台帳削除処理 ▲▲

        // ▼▼ 売上台帳登録処理 ▼▼

        // ▼ *** 登録処理 *** ▼
        var itm1 = record.商品コード１.value;
        var itm_1 = record.自由品名_1.value;
        if (itm1 !== "" || itm_1 !== "") {
            // ▼▼ 売上台帳登録処理 ▼▼
            var params = {
                "app": 37, // 移行済
                "record": {
                    "status": { "value": record.ラジオボタン.value }, // ステイタス
                    "order_id": { "value": event.record.$id.value }, // 受注レコード番号 
                    "order_no": { "value": record.受注NO.value }, // 受注No
                    "order_ymd": { "value": record.日付_2.value }, // 受注日
                    "nouki_ymd": { "value": record.納期.value }, // 納期
                    "syukka_ymd": { "value": record.出荷日.value }, // 出荷日
                    "bun_1": { "value": record.bun1.value }, // 分類１
                    "bun_2": { "value": record.bun2.value }, // 分類２
                    "bun_3": { "value": record.bun3.value }, // 分類３
                    "order_person": { "value": record.tanto.value }, // 受注担当
                    "sales_person": { "value": record.ドロップダウン_1.value }, // 営業担当
                    "tokui_id": { "value": record.ルックアップ.value }, // 得意先
                    "nounyu_id": { "value": record.ルックアップ_10.value }, // 納入先
                    // ↓　新規追加　↓
                    "tokui_nm": { "value": record.得意先名.value }, // 得意先名
                    "tokui_dept": { "value": record.得意先部署.value }, // 得意先部署
                    "nounyu_nm": { "value": record.納入先名.value }, // 納入先名
                    "nounyu_dept": { "value": record.納入先部署.value }, // 納入部署
                    "pre_tokui_id": { "value": record.親得意先コード.value }, // 得意先名
                    "pre_tokui_nm": { "value": record.親得意先.value }, // 納入先名
                    // ↓ 明細項目 ↓
                    "item": { "value": record.商品コード１.value }, // 品番
                    "item_nm1": { "value": record.名称１.value }, // 品名
                    "item_nm2": { "value": record.自由品名_1.value }, // 品名（自由記入）
                    "keijyo": { "value": record.粉液_1.value }, // 粉／液体
                    "nisugata": { "value": record.荷姿_1.value }, // 荷姿
                    "qty": { "value": record.数量_1.value }, // 数量
                    "yoryo": { "value": record.容量１.value }, // 容量
                    "unit": { "value": record.単位１.value }, // 単位
                    "price": { "value": record.単価１.value }, // 単価
                    "sum": { "value": record.計算１.value }, // 小計
                    "rmk": { "value": record.備考１.value }, // 備考
                    "tax_rate": { "value": record.taxlate_1.value }, // 税率
                    "tax_cdn": { "value": record.taxcon_1.value }, // 税調整
                    "tax": { "value": record.taxamt_1.value }, // 税額
                    // ↓↓↓ 明細新規追加（商事品関連） ↓↓↓↓
                    "s_flg": { "value": record.s_flg_1.value }, // 商事品フラグ
                    "s_shu": { "value": record.s_shu_1.value } // 商事品種別
                }
            };

            console.log(params.record);
            // kintone REST API リクエスト ～ レコードの登録（POST）
            kintone.api(
                kintone.api.url('/k/v1/record', true), // - pathOrUrl
                'POST', // - method
                params, // - params
                function(resp) { // - callback
                    //window.alert('成功1');
                    // (特に何もしない)
                },
                function(resp) { // - errback
                    window.alert('システムエラーが発生しました、しばらくしてから再度更新してください。（UPD-001）');
                    // (特に何もしない)
                }
            );
            // ▲▲ 売上台帳登録処理 ▲▲  
        }
        var itm2 = record.商品コード２.value;
        var itm_2 = record.自由品名_2.value;
        if (itm2 !== "" || itm_2 !== "") {
            // ▼▼ 売上台帳登録処理 ▼▼
            var params = {
                "app": 37, // 移行済
                "record": {
                    "status": { "value": record.ラジオボタン.value }, // ステイタス
                    "order_id": { "value": event.record.$id.value }, // 受注レコード番号 
                    "order_no": { "value": record.受注NO.value }, // 受注No
                    "order_ymd": { "value": record.日付_2.value }, // 受注日
                    "nouki_ymd": { "value": record.納期.value }, // 納期
                    "syukka_ymd": { "value": record.出荷日.value }, // 出荷日
                    "bun_1": { "value": record.bun1.value }, // 分類１
                    "bun_2": { "value": record.bun2.value }, // 分類２
                    "bun_3": { "value": record.bun3.value }, // 分類３
                    "order_person": { "value": record.tanto.value }, // 受注担当
                    "sales_person": { "value": record.ドロップダウン_1.value }, // 営業担当
                    "tokui_id": { "value": record.ルックアップ.value }, // 得意先
                    "nounyu_id": { "value": record.ルックアップ_10.value }, // 納入先
                    // ↓　新規追加　↓
                    "tokui_nm": { "value": record.得意先名.value }, // 得意先名
                    "tokui_dept": { "value": record.得意先部署.value }, // 得意先部署
                    "nounyu_nm": { "value": record.納入先名.value }, // 納入先名
                    "nounyu_dept": { "value": record.納入先部署.value }, // 納入部署
                    "pre_tokui_id": { "value": record.親得意先コード.value }, // 得意先名
                    "pre_tokui_nm": { "value": record.親得意先.value }, // 納入先名
                    // ↓ 明細項目 ↓
                    "item": { "value": record.商品コード２.value }, // 品番
                    "item_nm1": { "value": record.名称２.value }, // 品名
                    "item_nm2": { "value": record.自由品名_2.value }, // 品名（自由記入）
                    "keijyo": { "value": record.粉液_2.value }, // 粉／液体
                    "nisugata": { "value": record.荷姿_2.value }, // 荷姿
                    "qty": { "value": record.数量_2.value }, // 数量
                    "yoryo": { "value": record.容量２.value }, // 容量
                    "unit": { "value": record.単位２.value }, // 単位
                    "price": { "value": record.単価２.value }, // 単価
                    "sum": { "value": record.計算２.value }, // 小計
                    "rmk": { "value": record.備考２.value }, // 備考
                    "tax_rate": { "value": record.taxlate_2.value }, // 税率
                    "tax_cdn": { "value": record.taxcon_2.value }, // 税調整
                    "tax": { "value": record.taxamt_2.value }, // 税額
                    // ↓↓↓ 明細新規追加（商事品関連） ↓↓↓↓
                    "s_flg": { "value": record.s_flg_2.value }, // 商事品フラグ
                    "s_shu": { "value": record.s_shu_2.value } // 商事品種別
                }
            };

            // kintone REST API リクエスト ～ レコードの登録（POST）
            kintone.api(
                kintone.api.url('/k/v1/record', true), // - pathOrUrl
                'POST', // - method
                params, // - params
                function(resp) { // - callback
                    //window.alert('成功2');
                    // (特に何もしない)
                },
                function(resp) { // - errback
                    window.alert('システムエラーが発生しました、しばらくしてから再度更新してください。（UPD-002）');
                    // (特に何もしない)
                }
            );
            // ▲▲ 売上台帳登録処理 ▲▲  
        }
        var itm3 = record.商品コード３.value;
        var itm_3 = record.自由品名_3.value;
        if (itm3 !== "" || itm_3 !== "") {
            // ▼▼ 売上台帳登録処理 ▼▼
            var params = {
                "app": 37, // 移行済
                "record": {
                    "status": { "value": record.ラジオボタン.value }, // ステイタス
                    "order_id": { "value": event.record.$id.value }, // 受注レコード番号 
                    "order_no": { "value": record.受注NO.value }, // 受注No
                    "order_ymd": { "value": record.日付_2.value }, // 受注日
                    "nouki_ymd": { "value": record.納期.value }, // 納期
                    "syukka_ymd": { "value": record.出荷日.value }, // 出荷日
                    "bun_1": { "value": record.bun1.value }, // 分類１
                    "bun_2": { "value": record.bun2.value }, // 分類２
                    "bun_3": { "value": record.bun3.value }, // 分類３
                    "order_person": { "value": record.tanto.value }, // 受注担当
                    "sales_person": { "value": record.ドロップダウン_1.value }, // 営業担当
                    "tokui_id": { "value": record.ルックアップ.value }, // 得意先
                    "nounyu_id": { "value": record.ルックアップ_10.value }, // 納入先
                    // ↓　新規追加　↓
                    "tokui_nm": { "value": record.得意先名.value }, // 得意先名
                    "tokui_dept": { "value": record.得意先部署.value }, // 得意先部署
                    "nounyu_nm": { "value": record.納入先名.value }, // 納入先名
                    "nounyu_dept": { "value": record.納入先部署.value }, // 納入部署
                    "pre_tokui_id": { "value": record.親得意先コード.value }, // 得意先名
                    "pre_tokui_nm": { "value": record.親得意先.value }, // 納入先名
                    // ↓ 明細項目 ↓
                    "item": { "value": record.商品コード３.value }, // 品番
                    "item_nm1": { "value": record.名称３.value }, // 品名
                    "item_nm2": { "value": record.自由品名_3.value }, // 品名（自由記入）
                    "keijyo": { "value": record.粉液_3.value }, // 粉／液体
                    "nisugata": { "value": record.荷姿_3.value }, // 荷姿
                    "qty": { "value": record.数量_3.value }, // 数量
                    "yoryo": { "value": record.容量３.value }, // 容量
                    "unit": { "value": record.単位３.value }, // 単位
                    "price": { "value": record.単価３.value }, // 単価
                    "sum": { "value": record.計算３.value }, // 小計
                    "rmk": { "value": record.備考３.value }, // 備考
                    "tax_rate": { "value": record.taxlate_3.value }, // 税率
                    "tax_cdn": { "value": record.taxcon_3.value }, // 税調整
                    "tax": { "value": record.taxamt_3.value }, // 税額
                    // ↓↓↓ 明細新規追加（商事品関連） ↓↓↓↓
                    "s_flg": { "value": record.s_flg_3.value }, // 商事品フラグ
                    "s_shu": { "value": record.s_shu_3.value } // 商事品種別
                }
            };

            // kintone REST API リクエスト ～ レコードの登録（POST）
            kintone.api(
                kintone.api.url('/k/v1/record', true), // - pathOrUrl
                'POST', // - method
                params, // - params
                function(resp) { // - callback
                    // window.alert('成功3');
                    // (特に何もしない)
                },
                function(resp) { // - errback
                    window.alert('システムエラーが発生しました、しばらくしてから再度更新してください。（UPD-003）');
                    // (特に何もしない)
                }
            );
            // ▲▲ 売上台帳登録処理 ▲▲  
        }
        var itm4 = record.商品コード４.value;
        var itm_4 = record.自由品名_4.value;
        if (itm4 !== "" || itm_4 !== "") {
            // ▼▼ 売上台帳登録処理 ▼▼
            var params = {
                "app": 37, // 移行済
                "record": {
                    "status": { "value": record.ラジオボタン.value }, // ステイタス
                    "order_id": { "value": event.record.$id.value }, // 受注レコード番号 
                    "order_no": { "value": record.受注NO.value }, // 受注No
                    "order_ymd": { "value": record.日付_2.value }, // 受注日
                    "nouki_ymd": { "value": record.納期.value }, // 納期
                    "syukka_ymd": { "value": record.出荷日.value }, // 出荷日
                    "bun_1": { "value": record.bun1.value }, // 分類１
                    "bun_2": { "value": record.bun2.value }, // 分類２
                    "bun_3": { "value": record.bun3.value }, // 分類３
                    "order_person": { "value": record.tanto.value }, // 受注担当
                    "sales_person": { "value": record.ドロップダウン_1.value }, // 営業担当
                    "tokui_id": { "value": record.ルックアップ.value }, // 得意先
                    "nounyu_id": { "value": record.ルックアップ_10.value }, // 納入先
                    // ↓　新規追加　↓
                    "tokui_nm": { "value": record.得意先名.value }, // 得意先名
                    "tokui_dept": { "value": record.得意先部署.value }, // 得意先部署
                    "nounyu_nm": { "value": record.納入先名.value }, // 納入先名
                    "nounyu_dept": { "value": record.納入先部署.value }, // 納入部署
                    "pre_tokui_id": { "value": record.親得意先コード.value }, // 得意先名
                    "pre_tokui_nm": { "value": record.親得意先.value }, // 納入先名
                    // ↓ 明細項目 ↓
                    "item": { "value": record.商品コード４.value }, // 品番
                    "item_nm1": { "value": record.名称４.value }, // 品名
                    "item_nm2": { "value": record.自由品名_4.value }, // 品名（自由記入）
                    "keijyo": { "value": record.粉液_4.value }, // 粉／液体
                    "nisugata": { "value": record.荷姿_4.value }, // 荷姿
                    "qty": { "value": record.数量_4.value }, // 数量
                    "yoryo": { "value": record.容量４.value }, // 容量
                    "unit": { "value": record.単位４.value }, // 単位
                    "price": { "value": record.単価４.value }, // 単価
                    "sum": { "value": record.計算４.value }, // 小計
                    "rmk": { "value": record.備考４.value }, // 備考
                    "tax_rate": { "value": record.taxlate_4.value }, // 税率
                    "tax_cdn": { "value": record.taxcon_4.value }, // 税調整
                    "tax": { "value": record.taxamt_4.value }, // 税額
                    // ↓↓↓ 明細新規追加（商事品関連） ↓↓↓↓
                    "s_flg": { "value": record.s_flg_4.value }, // 商事品フラグ
                    "s_shu": { "value": record.s_shu_4.value } // 商事品種別
                }
            };


            // kintone REST API リクエスト ～ レコードの登録（POST）
            kintone.api(
                kintone.api.url('/k/v1/record', true), // - pathOrUrl
                'POST', // - method
                params, // - params
                function(resp) { // - callback
                    //window.alert('成功4');
                    // (特に何もしない)
                },
                function(resp) { // - errback
                    window.alert('システムエラーが発生しました、しばらくしてから再度更新してください。（UPD-004）');
                    // (特に何もしない)
                }
            );
            // ▲▲ 売上台帳登録処理 ▲▲  
        }
        var itm5 = record.商品コード５.value;
        var itm_5 = record.自由品名_5.value;
        if (itm5 !== "" || itm_5 !== "") {
            // ▼▼ 売上台帳登録処理 ▼▼
            var params = {
                "app": 37, // 移行済
                "record": {
                    "status": { "value": record.ラジオボタン.value }, // ステイタス
                    "order_id": { "value": event.record.$id.value }, // 受注レコード番号 
                    "order_no": { "value": record.受注NO.value }, // 受注No
                    "order_ymd": { "value": record.日付_2.value }, // 受注日
                    "nouki_ymd": { "value": record.納期.value }, // 納期
                    "syukka_ymd": { "value": record.出荷日.value }, // 出荷日
                    "bun_1": { "value": record.bun1.value }, // 分類１
                    "bun_2": { "value": record.bun2.value }, // 分類２
                    "bun_3": { "value": record.bun3.value }, // 分類３
                    "order_person": { "value": record.tanto.value }, // 受注担当
                    "sales_person": { "value": record.ドロップダウン_1.value }, // 営業担当
                    "tokui_id": { "value": record.ルックアップ.value }, // 得意先
                    "nounyu_id": { "value": record.ルックアップ_10.value }, // 納入先
                    // ↓　新規追加　↓
                    "tokui_nm": { "value": record.得意先名.value }, // 得意先名
                    "tokui_dept": { "value": record.得意先部署.value }, // 得意先部署
                    "nounyu_nm": { "value": record.納入先名.value }, // 納入先名
                    "nounyu_dept": { "value": record.納入先部署.value }, // 納入部署
                    "pre_tokui_id": { "value": record.親得意先コード.value }, // 得意先名
                    "pre_tokui_nm": { "value": record.親得意先.value }, // 納入先名
                    // ↓ 明細項目 ↓
                    "item": { "value": record.商品コード５.value }, // 品番
                    "item_nm1": { "value": record.名称５.value }, // 品名
                    "item_nm2": { "value": record.自由品名_5.value }, // 品名（自由記入）
                    "keijyo": { "value": record.粉液_5.value }, // 粉／液体
                    "nisugata": { "value": record.荷姿_5.value }, // 荷姿
                    "qty": { "value": record.数量_5.value }, // 数量
                    "yoryo": { "value": record.容量５.value }, // 容量
                    "unit": { "value": record.単位５.value }, // 単位
                    "price": { "value": record.単価５.value }, // 単価
                    "sum": { "value": record.計算５.value }, // 小計
                    "rmk": { "value": record.備考５.value }, // 備考
                    "tax_rate": { "value": record.taxlate_5.value }, // 税率
                    "tax_cdn": { "value": record.taxcon_5.value }, // 税調整
                    "tax": { "value": record.taxamt_5.value }, // 税額
                    // ↓↓↓ 明細新規追加（商事品関連） ↓↓↓↓
                    "s_flg": { "value": record.s_flg_5.value }, // 商事品フラグ
                    "s_shu": { "value": record.s_shu_5.value } // 商事品種別
                }
            };

            // kintone REST API リクエスト ～ レコードの登録（POST）
            kintone.api(
                kintone.api.url('/k/v1/record', true), // - pathOrUrl
                'POST', // - method
                params, // - params
                function(resp) { // - callback
                    //window.alert('成功5');
                    // (特に何もしない)
                },
                function(resp) { // - errback
                    window.alert('システムエラーが発生しました、しばらくしてから再度更新してください。（UPD-005）');
                    // (特に何もしない)
                }
            );
            // ▲▲ 売上台帳登録処理 ▲▲  
        }
        // ▲ *** 登録処理 *** ▲

        // ▲▲ 売上台帳登録処理 ▲▲

        return event;
    });

    // ***** 削除処理 *****
    kintone.events.on('app.record.detail.delete.submit', function(event) {
        // ※※　権限チェック
        var user = kintone.getLoginUser();
        console.log('User:' + user.id);
        if (user.id == '5') {
            console.log('制限ユーザの為処理をスキップしました。');
            return event;
        }
        var record = event.record;
        var ids = [];
        // ▼▼ 売上台帳削除処理 ▼▼

        // ▼▼▼ 受注番号から削除対象を取得 ▼▼▼
        var body = {
            'app': 37, //移行済
            'query': 'order_id = ' + event.record.$id.value,
            'fields': ['レコード番号']
        };

        kintone.api(kintone.api.url('/k/v1/records.json', true), 'GET', body, function(resp) {
            // success
            console.log(resp);
            for (var i = 0; i < resp.records.length; i++) {
                ids.push(Number(resp.records[i].レコード番号.value));
                //console.log(resp.records[i].レコード番号.value);
            }
            console.log(ids);
            if (ids != '') {
                //console.log(ids);
                var body = {
                    'app': 37, // 移行済
                    'ids': ids
                };

                kintone.api(kintone.api.url('/k/v1/records.json', true), 'DELETE', body, function(resp) {
                    // success
                    console.log(resp);
                    //window.alert('削除成功');
                }, function(error) {
                    // error
                    console.log(error);
                    window.alert('システムエラーが発生しました、しばらくしてから再度更新してください。（DEL）');
                });
            }
        }, function(error) {
            // error
            console.log(error);
            //window.alert('取得失敗');
        });
        // ▲▲ 売上台帳削除処理 ▲▲
        return event;
    });

})();