(function () {
    "use strict";
    kintone.events.on('app.record.index.show', function (event) {
        if (document.getElementById('my_index_button') !== null) {
            return;
        }

        var myIndexButton = document.createElement('button');
        myIndexButton.id = 'my_index_button';
        myIndexButton.innerText = '※開発中なので押さないで！※ 売上登録・更新';

        // ボタンクリック時の処理
        myIndexButton.onclick = async function () {
            var result = window.confirm('一覧画面に表示されている受注の売上を作成します。よろしいですか？');
            if (result) {
                window.alert('処理を予約しました。（売上：未 かつ 売上No：入力有 の受注の売上を作成します。）');

                // Promiseの処理をループで繰り返す
                var myPromise = Promise.resolve();
                for (var i = 0; i < event.records.length; i++) {
                    var u_no = event.records[i].売上計上NO.value;
                    var chk = event.records[i].売上計上_chk.value;
                    if (u_no != '' && chk == '未') {
                        myPromise = myPromise
                            .then(task1.bind(this, event.records[i])) // bindでtask1に行レコードを渡す
                            .then(task2)
                            .then(task3)
                            .then(task4)
                            .then(task5)
                    }
                }

                // ループで実行する処理
                // 売上チェック
                function task1(record) { // 対象行レコード
                    return new Promise(function (resolve, reject) {
                        setTimeout(function () {
                            console.log('*** task1　実行 ***');
                            var u_no = record.売上計上NO.value;
                            var params_01 = {
                                'app': 43,
                                'query': 'uriage_no = "' + u_no + '"'
                            };
                            kintone.api(kintone.api.url('/k/v1/records', true), 'GET', params_01, function (resp) {
                                console.log('*** 既存売上データの存在チェック実行 ***');
                                console.log(resp);
                                resolve([record, resp]);
                            });

                        }, 2000);
                    });
                }
                function task2(values) { // 検索の結果を受け取る
                    return new Promise(function (resolve, reject) {
                        setTimeout(function () {
                            console.log('task2 実行...');
                            // 1行レコードを受け取る
                            var record = values[0]; // 対象行のレコード
                            var record_no = record.レコード番号.value;
                            var u_no = record.売上計上NO.value;
                            var bun1 = record.bun1.value;
                            var bun2 = record.bun2.value;
                            var cust = record.請求用得意先コード.value;
                            var yotei = record.回収予定日.value;
                            var nyukinmoto = record.入金元コード.value;
                            // task1の既存データ存在チェックの結果を受け取る
                            var resp = values[1]; // 存在チェックの結果
                            if (resp.records[0]) {
                                console.log('既存データが存在するため既存データを更新');
                                // 既存のデータが存在する場合は既存データを更新（テーブルに明細を追加）
                                // テーブルの中身を取得(既存データIDを追加)
                                var param_value = '';
                                var param_value_arry = [];
                                for (var i = 0; i < resp.records[0].table.value.length; i++) {
                                    var p_id = resp.records[0].table.value[i].id;
                                    param_value += '{"id":"' + p_id + '"},';
                                    param_value_arry.push({
                                        "id": p_id
                                    });
                                }
                                var p_val1 = {
                                    "value": record_no
                                };
                                var p_val2 = {
                                    "受注": p_val1
                                };
                                var p_val3 = {
                                    "value": p_val2
                                }
                                param_value_arry.push(p_val3);
                                param_value += '{"value":{"受注":{"value":' + record_no + '}}}'
                                // テーブル更新用のパラメータを定義
                                var upd_param = {
                                    "app": 43, // 売上
                                    "id": resp.records[0].レコード番号.value,
                                    "record": {
                                        "table": {
                                            "value": param_value_arry
                                        }
                                    }
                                };
                                kintone.api(kintone.api.url('/k/v1/record', true), 'PUT', upd_param, function (resp) {
                                    console.log('*** 売上レコードの更新処理実行 ***');
                                    console.log(resp);
                                    resolve(record);
                                });
                            } else {
                                console.log("既存データが存在しないため、新規登録");
                                var uriageno = u_no.substr(-8);
                                // 登録用パラメータを定義
                                var ins_param = {
                                    "app": 43, //売上
                                    "record": {
                                        "ラジオボタン_0": {
                                            "value": "未確定"
                                        },
                                        "bun1": {
                                            "value": bun1
                                        },
                                        "bun2": {
                                            "value": bun2
                                        },
                                        "uriageno_c": {
                                            "value": uriageno
                                        },
                                        "ルックアップ": {
                                            "value": cust
                                        },
                                        "日付_2": {
                                            "value": yotei
                                        },
                                        "taxmet": {
                                            "value": "合計"
                                        },
                                        "taxlate": {
                                            "value": "10%"
                                        },
                                        "table": {
                                            "value": [{
                                                "value": {
                                                    "受注": {
                                                        "value": record_no
                                                    }
                                                }
                                            }]
                                        }
                                    }
                                };
                                kintone.api(kintone.api.url('/k/v1/record', true), 'POST', ins_param, function (resp) {
                                    console.log('*** 売上レコードの新規処理実行 ***');
                                    console.log(resp);
                                    resolve(record);
                                });
                            }
                            //resolve(val);
                        }, 2000);
                    });
                }
                function task3(record) { // 入金元処理
                    return new Promise(function (resolve, reject) {
                        setTimeout(function () {
                            console.log('task3 実行');
                            var u_no = record.売上計上NO.value;
                            var nyukinmoto = record.入金元コード.value;
                            console.log('*** 入金元コード :' + nyukinmoto);
                            // 入金元が存在する場合のみ処理を実行
                            if (nyukinmoto != '') {
                                // 入金元をゼロ埋め
                                nyukinmoto = ('0000' + nyukinmoto).slice(-4);
                                // 入金元用の売上Noの作成(売上Noの年月までの部分と入金元コードを合体)
                                var uriageno2 = u_no.substr(-8).substr(0, 4) + nyukinmoto;
                                // 売上計上No検索処理
                                // ▽▼ *** 更新対象取得 *** ▼▽
                                var params = {
                                    "app": 43, // 売上
                                    'query': 'uriage_no like "' + uriageno2 + '"',
                                    'fields': ['レコード番号', 'table']
                                };
                                console.log(params);
                                kintone.api(kintone.api.url('/k/v1/records', true), 'GET', params, function (resp) {
                                    console.log('*** 入金元レコードの取得処理実行 ***');
                                    console.log(resp);
                                    resolve([record, resp]);
                                });
                            } else {
                                resolve([record, "skip"]);
                            }

                        }, 2000);
                    });
                }
                function task4(values) { // 引数iを受け取る
                    return new Promise(function (resolve, reject) {
                        setTimeout(function () {
                            console.log('task4 実行');
                            var record = values[0]; // 対象行のレコード
                            var resp = values[1]; // 存在チェックの結果

                            console.log('*** record ***');
                            console.log(record);
                            console.log('*** resp ***');
                            console.log(resp);

                            // 入金元コードが存在しない場合は処理をSkip
                            if (resp == 'skip') {
                                console.log('入金元コードが存在しない場合は処理をSkip');
                                resolve(record);
                            } else {
                                var record_no = record.レコード番号.value;
                                var u_no = record.売上計上NO.value;
                                var nyukinmoto = record.入金元コード.value;
                                // 入金元をゼロ埋め
                                nyukinmoto = ('0000' + nyukinmoto).slice(-4);
                                // 入金元用の売上Noの作成(売上Noの年月までの部分と入金元コードを合体)
                                var uriageno2 = u_no.substr(-8).substr(0, 4) + nyukinmoto;
                                var bun1 = record.bun1.value;
                                var bun2 = record.bun2.value;
                                var cust = record.請求用得意先コード.value;
                                var yotei = record.回収予定日.value;
                                // 入金元データが存在する場合
                                if (resp.records[0]) {
                                    console.log('入金元データが存在する場合（既存データ更新）');
                                    console.log(resp.records[0]);
                                    // テーブルの中身を取得(既存データIDを追加)
                                    var param_value = '';
                                    var param_value_arry = [];
                                    for (var i = 0; i < resp.records[0].table.value.length; i++) {
                                        var p_id = resp.records[0].table.value[i].id;
                                        param_value += '{"id":"' + p_id + '"},';
                                        param_value_arry.push({
                                            "id": p_id
                                        });
                                    }
                                    var p_val1 = {
                                        "value": record_no
                                    };
                                    var p_val2 = {
                                        "受注": p_val1
                                    };
                                    var p_val3 = {
                                        "value": p_val2
                                    }
                                    param_value_arry.push(p_val3);
                                    param_value += '{"value":{"受注":{"value":' + record_no + '}}}'
                                    //console.log(param_value_arry);
                                    // テーブル更新用のパラメータを定義
                                    var upd_param2 = {
                                        "app": 43, // 売上登録 
                                        "id": resp.records[0].レコード番号.value,
                                        "record": {
                                            "table": {
                                                "value": param_value_arry
                                            }
                                        }
                                    };
                                    kintone.api(kintone.api.url('/k/v1/record', true), 'PUT', upd_param2, function (resp) {
                                        console.log('*** 売上レコードの更新処理実行（入金元） ***');
                                        console.log(resp);
                                        resolve(record);
                                    });

                                } else {
                                    // 登録用パラメータを定義
                                    var ins_param2 = {
                                        "app": 43, // 売上登録 移行済
                                        "record": {
                                            "ラジオボタン_0": {
                                                "value": "未確定"
                                            },
                                            "bun1": {
                                                "value": bun1
                                            },
                                            "bun2": {
                                                "value": bun2
                                            },
                                            "uriageno_c": {
                                                "value": uriageno2
                                            },
                                            "ルックアップ": {
                                                "value": nyukinmoto
                                            },
                                            "日付_2": {
                                                "value": yotei
                                            },
                                            "taxmet": {
                                                "value": "合計"
                                            },
                                            "taxlate": {
                                                "value": "10%"
                                            },
                                            "table": {
                                                "value": [{
                                                    "value": {
                                                        "受注": {
                                                            "value": record_no
                                                        }
                                                    }
                                                }]
                                            }
                                        }
                                    };
                                    kintone.api(kintone.api.url('/k/v1/record', true), 'POST', ins_param2, function (resp) {
                                        console.log('*** 売上レコードの新規処理実行（入金元） ***');
                                        console.log(resp);
                                        resolve(record);
                                    });
                                }

                            }
                            //resolve([record]);
                        }, 2000);
                    });
                }
                function task5(record) { // 引数iを受け取る
                    return new Promise(function (resolve, reject) {
                        setTimeout(function () {
                            console.log('task5 処理中...');
                            var record_no = record.レコード番号.value;
                            var body = {
                                'app': 44, // 受注
                                'id': record_no,
                                'record': {
                                    '売上計上_chk': {
                                        'value': '済'
                                    }
                                }
                            };
                            kintone.api(kintone.api.url('/k/v1/record.json', true), 'PUT', body, function (resp) {
                                console.log('*** 受注レコードステイタス更新処理実行 ***');
                                console.log(resp);
                                resolve();
                            });
                        }, 2000);
                    });
                }
            } else {
                window.alert('処理をキャンセルしました。');
            }
        };
        kintone.app.getHeaderMenuSpaceElement().appendChild(myIndexButton);
    });
})();