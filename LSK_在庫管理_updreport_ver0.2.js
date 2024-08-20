moment.locale('ja');

(function () {
    "use strict";
    kintone.events.on('app.record.index.show', function (event) {
        if (document.getElementById('my_index_button') !== null) {
            return;
        }
        // 画面のパスワード入力を作成
        var pass = document.createElement('input');
        pass.type = 'password';
        pass.placeholder = 'パスワード';
        pass.id = 'pass';
        // 画面にセレクトボックスを作成
        var select_1 = document.createElement("select");
        var option_nouki = document.createElement("option");
        var option_syukabi = document.createElement("option");
        option_nouki.setAttribute("value", "nouki");
        option_nouki.appendChild(document.createTextNode("納期"));
        option_syukabi.setAttribute("value", "syukabi");
        option_syukabi.appendChild(document.createTextNode("出荷日"));
        select_1.setAttribute("name", "select_1");
        select_1.appendChild(option_nouki);
        select_1.appendChild(option_syukabi);
        var select_2 = document.createElement("select");
        var option_1 = document.createElement("option");
        var option_2 = document.createElement("option");
        var option_3 = document.createElement("option");
        var option_4 = document.createElement("option");
        var option_5 = document.createElement("option");
        var option_6 = document.createElement("option");
        var option_7 = document.createElement("option");
        var option_8 = document.createElement("option");
        var option_9 = document.createElement("option");
        var option_10 = document.createElement("option");
        option_1.setAttribute("value", "2021");
        option_1.appendChild(document.createTextNode("2021年"));
        option_2.setAttribute("value", "2022");
        option_2.appendChild(document.createTextNode("2022年"));
        option_3.setAttribute("value", "2023");
        option_3.appendChild(document.createTextNode("2023年"));
        option_4.setAttribute("value", "2024");
        option_4.appendChild(document.createTextNode("2024年"));
        option_5.setAttribute("value", "2025");
        option_5.appendChild(document.createTextNode("2025年"));
        option_6.setAttribute("value", "2026");
        option_6.appendChild(document.createTextNode("2026年"));
        option_7.setAttribute("value", "2027");
        option_7.appendChild(document.createTextNode("2027年"));
        option_8.setAttribute("value", "2028");
        option_8.appendChild(document.createTextNode("2028年"));
        option_9.setAttribute("value", "2029");
        option_9.appendChild(document.createTextNode("2029年"));
        option_10.setAttribute("value", "2030");
        option_10.appendChild(document.createTextNode("2030年"));
        select_2.appendChild(option_1);
        select_2.appendChild(option_2);
        select_2.appendChild(option_3);
        select_2.appendChild(option_4);
        select_2.appendChild(option_5);
        select_2.appendChild(option_6);
        select_2.appendChild(option_7);
        select_2.appendChild(option_8);
        select_2.appendChild(option_9);
        select_2.appendChild(option_10);
        var select_3 = document.createElement("select");
        var option_1_ = document.createElement("option");
        var option_2_ = document.createElement("option");
        var option_3_ = document.createElement("option");
        var option_4_ = document.createElement("option");
        var option_5_ = document.createElement("option");
        var option_6_ = document.createElement("option");
        var option_7_ = document.createElement("option");
        var option_8_ = document.createElement("option");
        var option_9_ = document.createElement("option");
        var option_10_ = document.createElement("option");
        var option_11_ = document.createElement("option");
        var option_12_ = document.createElement("option");
        option_1_.setAttribute("value", "0");
        option_1_.appendChild(document.createTextNode("1月"));
        option_2_.setAttribute("value", "1");
        option_2_.appendChild(document.createTextNode("2月"));
        option_3_.setAttribute("value", "2");
        option_3_.appendChild(document.createTextNode("3月"));
        option_4_.setAttribute("value", "3");
        option_4_.appendChild(document.createTextNode("4月"));
        option_5_.setAttribute("value", "4");
        option_5_.appendChild(document.createTextNode("5月"));
        option_6_.setAttribute("value", "5");
        option_6_.appendChild(document.createTextNode("6月"));
        option_7_.setAttribute("value", "6");
        option_7_.appendChild(document.createTextNode("7月"));
        option_8_.setAttribute("value", "7");
        option_8_.appendChild(document.createTextNode("8月"));
        option_9_.setAttribute("value", "8");
        option_9_.appendChild(document.createTextNode("9月"));
        option_10_.setAttribute("value", "9");
        option_10_.appendChild(document.createTextNode("10月"));
        option_11_.setAttribute("value", "10");
        option_11_.appendChild(document.createTextNode("11月"));
        option_12_.setAttribute("value", "11");
        option_12_.appendChild(document.createTextNode("12月"));
        select_3.appendChild(option_1_);
        select_3.appendChild(option_2_);
        select_3.appendChild(option_3_);
        select_3.appendChild(option_4_);
        select_3.appendChild(option_5_);
        select_3.appendChild(option_6_);
        select_3.appendChild(option_7_);
        select_3.appendChild(option_8_);
        select_3.appendChild(option_9_);
        select_3.appendChild(option_10_);
        select_3.appendChild(option_11_);
        select_3.appendChild(option_12_);

        var myIndexButton = document.createElement('button');
        myIndexButton.id = 'my_index_button';
        myIndexButton.innerText = '在庫管理台帳作成';

        // ボタンクリック時の処理
        myIndexButton.onclick = function () {

            if (pass.value == '12345678') {
                var kbn = select_1.value;
                var year = select_2.value;
                var month = select_3.value;
                // セレクトボックスの値から検索条件を作成（月初～月末）
                var start_dt = new Date(year, month, 1);
                var end_dt = new Date(year, start_dt.getMonth() + 1, 0);
                //var end_dt = moment(start_dt).endOf('month');
                //console.log("* start_dt" + start_dt);
                //console.log("* end_dt" + end_dt);
                var start_st = start_dt.getFullYear() + '-' + (start_dt.getMonth() + 1) + '-' + start_dt.getDate();
                var end_st = end_dt.getFullYear() + '-' + (end_dt.getMonth() + 1) + '-' + end_dt.getDate();
                var result = window.confirm(start_st + '~' + end_st + 'の在庫台帳を作成しますよろしいですか？ (時間がかかります)');

                // 検索条件の納期／出荷日の切替 
                var query_str = '納期';
                if (kbn == 'syukabi') {
                    query_str = '出荷日';
                }
                if (result) {
                    window.alert('処理を予約しました。処理に時間がかかります。１時間以内に生成されます。');
                    // ############################################################## ↓ promise ↓ ##############################################################
                    // クライアントの作成
                    var client = new KintoneRestAPIClient();
                    // ▼ 処理対象取得処理（セレクトボックスで入力された条件で受注から抽出）▼
                    var query = query_str + " >= \"" + start_st + "\" and " + query_str + " <= \"" + end_st + "\"";
                    var body = {
                        app: 44, // 新環境(受注)
                        condition: query
                    };
                    client.record.getAllRecords(body).then((resp) => {
                        //console.log(resp.length);
                        // ▼▼ 受注レコード毎の処理 ▼▼
                        var ins_record = []; // 受注から取得した対象レコード

                        for (var i = 0; i < resp.length; i++) {
                            var record = resp[i];

                            // 明細分レコードを作成
                            var records = [];
                            if (record.商品コード１.value != "" || record.自由品名_1.value != "" || record.名称１.value != "" || record.数量_1.value != "") {
                                var record_1 = {
                                    "order_id": { "value": record.レコード番号.value }, // 受注レコード番号 
                           
                                    // ↓ 明細項目 ↓
                                    "item": { "value": record.商品コード１.value }, // 品番
                                    "item_nm1": { "value": record.名称１.value }, // 品名
                                    "item_nm2": { "value": record.自由品名_1.value }, // 品名（自由記入）
                                    "qty": { "value": record.数量_1.value }, // 数量
                                    "yoryo": { "value": record.容量１.value }, // 容量
                                    "unit": { "value": record.単位１.value }, // 単位
                                }
                                records.push(record_1);
                                ins_record.push(record_1);
                            }
                            if (record.商品コード２.value != "" || record.自由品名_2.value != "" || record.名称２.value != "" || record.数量_2.value != "") {
                                var record_2 = {
                                    "order_id": { "value": record.レコード番号.value }, // 受注レコード番号 
                                    // ↓ 明細項目 ↓
                                    "item": { "value": record.商品コード２.value }, // 品番
                                    "item_nm1": { "value": record.名称２.value }, // 品名
                                    "item_nm2": { "value": record.自由品名_2.value }, // 品名（自由記入）
                                    "qty": { "value": record.数量_2.value }, // 数量
                                    "yoryo": { "value": record.容量２.value }, // 容量
                                    "unit": { "value": record.単位２.value }, // 単位
                                }
                                records.push(record_2);
                                ins_record.push(record_2);
                            }
                            if (record.商品コード３.value != "" || record.自由品名_3.value != "" || record.名称３.value != "" || record.数量_3.value != "") {
                                var record_3 = {
                                    "order_id": { "value": record.レコード番号.value }, // 受注レコード番号 
                                    // ↓ 明細項目 ↓
                                    "item": { "value": record.商品コード３.value }, // 品番
                                    "item_nm1": { "value": record.名称３.value }, // 品名
                                    "item_nm2": { "value": record.自由品名_3.value }, // 品名（自由記入）
                                    "qty": { "value": record.数量_3.value }, // 数量
                                    "yoryo": { "value": record.容量３.value }, // 容量
                                    "unit": { "value": record.単位３.value }, // 単位
                                }
                                records.push(record_3);
                                ins_record.push(record_3);
                            }
                            if (record.商品コード４.value != "" || record.自由品名_4.value != "" || record.名称４.value != "" || record.数量_4.value != "") {
                                var record_4 = {
                                    "order_id": { "value": record.レコード番号.value }, // 受注レコード番号 
                                    // ↓ 明細項目 ↓
                                    "item": { "value": record.商品コード４.value }, // 品番
                                    "item_nm1": { "value": record.名称４.value }, // 品名
                                    "item_nm2": { "value": record.自由品名_4.value }, // 品名（自由記入）
                                    "qty": { "value": record.数量_4.value }, // 数量
                                    "yoryo": { "value": record.容量４.value }, // 容量
                                    "unit": { "value": record.単位４.value }, // 単位
                                }
                                records.push(record_4);
                                ins_record.push(record_4);
                            }
                            if (record.商品コード５.value != "" || record.自由品名_5.value != "" || record.名称５.value != "" || record.数量_5.value != "") {
                                var record_5 = {
                                    "order_id": { "value": record.レコード番号.value }, // 受注レコード番号 
                                    // ↓ 明細項目 ↓
                                    "item": { "value": record.商品コード５.value }, // 品番
                                    "item_nm1": { "value": record.名称５.value }, // 品名
                                    "item_nm2": { "value": record.自由品名_5.value }, // 品名（自由記入）
                                    "qty": { "value": record.数量_5.value }, // 数量
                                    "yoryo": { "value": record.容量５.value }, // 容量
                                    "unit": { "value": record.単位５.value }, // 単位
                                }
                                records.push(record_5);
                                ins_record.push(record_5);
                            }
                            // ******** 登録用の台帳レコード作成 **************
                        }
                        // ▲▲ 受注レコード毎の処理 ▲▲



                        // ******** ↓台帳新規登録処理↓ **************
                        var param = {

                            app: 87, // 当該APP
                            records: ins_record
                        };
                        client.record.addAllRecords(param).then(function (resp) {
                            console.log(resp);
                        }).catch(function (err) {
                            console.log("*** addAllRecordsでエラーが発生しています。 ***");
                            console.log(err);
                            window.alert('受注データ取得処理でエラーが発生しました、もう一度最初からやりなおしてください。');
                        });
                        // ******** ↑台帳新規登録処理↑ **************
                    }).catch((err) => {
                        console.log("*** getAllRecordsでエラーが発生しています。 ***");
                        console.log(err);
                        window.alert('売上台帳登録処理でエラーが発生しました、もう一度最初からやりなおしてください。');
                    });


                    // ############################################################## ↑ promise ↑ ##############################################################
                    //window.alert('処理が完了しました。');
                } else {
                    window.alert('処理をキャンセルしました。');
                }
            } else {
                window.alert('パスワードが一致しません。');
            }
        };
        kintone.app.getHeaderMenuSpaceElement().appendChild(select_1);
        kintone.app.getHeaderMenuSpaceElement().appendChild(select_2);
        kintone.app.getHeaderMenuSpaceElement().appendChild(select_3);
        kintone.app.getHeaderMenuSpaceElement().appendChild(pass);
        kintone.app.getHeaderMenuSpaceElement().appendChild(myIndexButton);

    });
})();