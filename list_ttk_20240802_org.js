(function () {
    "use strict";
    kintone.events.on('app.record.index.show', function (event) {
        if (document.getElementById('my_index_button') !== null) {
            return;
        }

        var myIndexButton = document.createElement('button');
        myIndexButton.id = 'my_index_button';
        myIndexButton.innerText = '請求書作成';

        // ボタンクリック時の処理
        myIndexButton.onclick = function () {
            var result = window.confirm('一覧画面に表示されている納品に対して請求を作成します。よろしいですか？ (時間がかかります)');
            if (result) {
                window.alert('処理を実行します。（時間がかかる場合があります。）');
                // ############################################################## ↓ promise ↓ ##############################################################
                // クライアントの作成
                var client = new KintoneRestAPIClient();

                var ins_record = []; // 【請求】登録用データ
                var upd_record = []; // 【請求登録】更新用データ
                var param_table = [];// 【請求】登録用のテーブルデータ

                // Promiseの処理をループで繰り返す
                var myPromise = Promise.resolve();
                for (var i = 0; i < event.records.length; i++) {
                    var flg = event.records[i].請求書出力.value;
                    var flg2 = event.records[i].請求登録.value;
                    if(flg == "する" && flg2 == "未"){ // 請求書書出力＝する　AND 請求登録＝未　のデータのみ処理の対象とする
                        console.log('*** 処理を実行！ ***');
                        myPromise = myPromise
                        .then(task1.bind(this, event.records[i])) // bindでtask1に行レコードを渡す
                    }else{
                        console.log('*** 処理を実行しない ***');
                    }           
                }



                myPromise
                    .then(function () {
                        return new Promise(function (resolve, reject) {
                            // ループ完了後に実行したい処理
                            //console.log('ループ完了後に実行');
                            //console.log(ins_record);
                            //console.log(upd_record);
                            //console.log(param_table);
                            if(upd_record == ""){
                                console.log('対象データなし');
                                resolve();
                            }else{
                            
                            // 基本情報
                            const d = new Date();
                            const formatd = d.getFullYear() + "-" + String(d.getMonth() + 1).padStart(2, '0') + "-" + d.getDate();
                            var param_ins = {
                                "状況": { "value": "未発行" }, // 
                                "請求日": { "value": formatd },
                                "得意先_lu": { "value": event.records[0].得意先.value }, // 受注レコード番号 
                                "t_納品": { "value": param_table }
                            }
                            console.log(param_ins);
                            ins_record.push(param_ins);
                            // ******** ↓新規登録処理↓ **************
                            //console.log(ins_record);
                            var param = {
                                app: 65, // 【請求】
                                records: ins_record
                            };
                            client.record.addAllRecords(param).then(function (resp) {
                                console.log(resp);
                                // ******** ↓【請求登録】ステイタス更新処理↓ **************
                                var upd_param = {
                                    app: 84, // 【請求登録】
                                    records: upd_record
                                };
                                console.log(upd_param);
                                client.record.updateAllRecords(upd_param).then(function (resp) {
                                    console.log(resp);
                                }).catch(function (err) {
                                    console.log("*** 【請求】ステイタス更新でエラーが発生しています。 ***");
                                    console.log(resp);
                                    console.log(err);
                                    window.alert('【請求】ステイタス更新処理でエラーが発生しました、もう一度最初からやりなおしてください。');
                                });
                            }).catch((err) => {
                                console.log("***【請求】新規登録処理でエラーが発生しています。 ***");
                                console.log(err);
                                window.alert('【請求】新規登録処理ででエラーが発生しました、もう一度最初からやりなおしてください。');
                            });
                            // ############################################################## ↑ promise ↑ ##############################################################
                            window.alert('処理が完了しました。');
                            resolve();}
                        });
                    })


                // ループで実行する処理
                function task1(record) { // 引数iを受け取る
                    return new Promise(function (resolve, reject) {
                        setTimeout(function () {
                            console.log("*** task1 ***");
                            // ******** ▽【納品】ステイタス更新用データ生成  ▽ ************** 
                            var upd_param = {
                                "id": record.レコード番号.value,
                                "record": {
                                    "請求登録": {
                                        "value": "済"
                                    }
                                }
                            }
                            upd_record.push(upd_param);
                            console.log(upd_param);
                            // ******** △ 【納品】ステイタス更新用データ生成 △ ************** 
                            //console.log(record);
                            // ******** 登録用のテーブルレコード作成 ************** 
                            var t_nouhin = {
                                value: {
                                    納品: {
                                        value: record.レコード番号.value
                                    }
                                }
                            }
                            param_table.push(t_nouhin);
                            console.log(t_nouhin);
                            resolve();
                        }, 1000);
                    });
                }
                
            } else {
                window.alert('処理をキャンセルしました。');
            }
        };

        var myIndexButton2 = document.createElement('button');
        myIndexButton2.id = 'my_index_button2';
        myIndexButton2.innerText = '納品書作成';

        // ボタンクリック時の処理
        myIndexButton2.onclick = function () {
            var result = window.confirm('納品書を作成しますよろしいですか？ (一覧画面の表示内容かつ「納品出力=>する」に対して実行されます)');
            if (result) {
                window.alert('処理を実行します。（時間がかかる場合があります。）');
                // ############################################################## ↓ promise ↓ ##############################################################
                // クライアントの作成
                var client = new KintoneRestAPIClient();

                var ins_record = []; // 【納品】登録用データ
                var upd_record = []; // 【請求登録】更新用データ
                var param_table = [];// 【納品】登録用のテーブルデータ

                // Promiseの処理をループで繰り返す
                var myPromise = Promise.resolve();
                for (var i = 0; i < event.records.length; i++) {
                    var flg = event.records[i].納品書出力.value;
                    var flg2 = event.records[i].納品登録.value;
                    if(flg == "する" && flg2 == "未"){ // 納品書出力＝する　AND 納品登録＝未　のデータのみ処理の対象とする
                        console.log('*** 処理を実行！ ***');
                        myPromise = myPromise
                        .then(task1.bind(this, event.records[i])) // bindでtask1に行レコードを渡す
                    }else{
                        console.log('*** 処理を実行しない ***');
                    }           
                }

                myPromise
                    .then(function () {
                        return new Promise(function (resolve, reject) {
                            // ループ完了後に実行したい処理
                            //console.log('ループ完了後に実行');
                            //console.log(ins_record);
                            //console.log(upd_record);
                            //console.log(param_table);
                            if(upd_record == ""){
                                console.log('対象データなし');
                                resolve();
                            }else{
                                console.log('対象データあり');
                            // 基本情報
                            const d = new Date();
                            const formatd = d.getFullYear() + "-" + String(d.getMonth() + 1).padStart(2, '0') + "-" + d.getDate();
                            var param_ins = {
                                "状況": { "value": "未発行" }, // 
                                "納品日_0": { "value": formatd },
                                "得意先_lu": { "value": event.records[0].得意先.value }, //
                                "受注番号＿枝番": { "value": event.records[0].受注番号＿枝番.value }, 
                                "t_納品": { "value": param_table }
                            }
                            console.log(param_ins);
                            ins_record.push(param_ins);
                            // ******** ↓新規登録処理↓ **************
                            console.log("新規登録内容");
                            console.log(ins_record);
                            var param = {
                                app: 86, // 【納品】
                                records: ins_record
                            };
                            client.record.addAllRecords(param).then(function (resp) {
                                console.log(resp);
                                // ******** ↓【請求登録】ステイタス更新処理↓ **************
                                var upd_param = {
                                    app: 84, // 【請求登録】
                                    records: upd_record
                                };
                                console.log(upd_param);
                                client.record.updateAllRecords(upd_param).then(function (resp) {
                                    console.log(resp);
                                }).catch(function (err) {
                                    console.log("*** 【納品】ステイタス更新でエラーが発生しています。 ***");
                                    console.log(resp);
                                    console.log(err);
                                    window.alert('【納品】ステイタス更新処理でエラーが発生しました、もう一度最初からやりなおしてください。');
                                });
                            }).catch((err) => {
                                console.log("***【納品】新規登録処理でエラーが発生しています。 ***");
                                console.log(err);
                                window.alert('【納品】新規登録処理ででエラーが発生しました、もう一度最初からやりなおしてください。');
                            });
                            // ############################################################## ↑ promise ↑ ##############################################################
                            window.alert('処理が完了しました。');
                            resolve();
                        }
                        });
                        
                    })


                // ループで実行する処理
                function task1(record) { // 引数iを受け取る
                    return new Promise(function (resolve, reject) {
                        setTimeout(function () {
                            console.log("*** task1 ***");
                            // ******** ▽【納品】ステイタス更新用データ生成  ▽ ************** 
                            var upd_param = {
                                "id": record.レコード番号.value,
                                "record": {
                                    "納品登録": {
                                        "value": "済"
                                    }
                                }
                            }
                            upd_record.push(upd_param);
                            console.log(upd_param);
                            // ******** △ 【納品】ステイタス更新用データ生成 △ ************** 
                            //console.log(record);
                            // ******** 登録用のテーブルレコード作成 ************** 
                            var t_nouhin = {
                                value: {
                                    納品: {
                                        value: record.レコード番号.value
                                    }
                                }
                            }
                            param_table.push(t_nouhin);
                            console.log(t_nouhin);
                            resolve();
                        }, 1000);
                    });
                }
                
            } else {
                window.alert('処理をキャンセルしました。');
            }
        };

        kintone.app.getHeaderMenuSpaceElement().appendChild(myIndexButton);
        kintone.app.getHeaderMenuSpaceElement().appendChild(myIndexButton2);
    });
})();