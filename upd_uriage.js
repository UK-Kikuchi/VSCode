(function() {
    "use strict";
    kintone.events.on('app.record.detail.show', function(event) {
        // 任意のスペースフィールドにボタンを設置
        var mySpaceFieldButton = document.createElement('button');
        mySpaceFieldButton.id = 'my_space_field_button';
        mySpaceFieldButton.innerText = '売上登録・更新';
        mySpaceFieldButton.onclick = function() {
            var record_no = ''; // 受注レコード番号
            var u_no = ''; // 売上計上No
            var chk = ''; // 売上計上チェックボックス
            var bun1 = '';
            var bun2 = '';
            var cust = '';
            var head = '';
            var uriageno = 0;
            var uriageno2 = 0;
            var yotei = '';
            var nyukinmoto = '';
            // 入力値を取得
            var rec = kintone.app.record.get();
            if (rec) {
                record_no = rec.record.レコード番号.value;
                var p_val1 = {
                    "value": record_no
                };
                var p_val2 = {
                    "受注": p_val1
                };
                var p_val3 = {
                        "value": p_val2
                    }
                    //param_value_arry.push(p_val3);
                    //param_value += '{"value":{"受注":{"value":' + record_no + '}}}'                
                u_no = rec.record.売上計上NO.value;
                chk = rec.record.売上計上_chk.value;
                bun1 = rec.record.bun1.value;
                bun2 = rec.record.bun2.value;
                cust = rec.record.請求用得意先コード.value;
                yotei = rec.record.回収予定日.value;
                // 2021-10-29 追加（入金元コード取得）
                nyukinmoto = rec.record.入金元コード.value;
                if (u_no == '') {
                    window.alert('売上計上Noが入力されていません！');
                } else {
                    if (chk == '済') {
                        window.alert('再登録する場合は売上登録を「未」に更新しなおしてください！');
                    } else {
                        // ▼ 売上計上更新処理 ▼
                        var body = {
                            'app': 44, // 受注　移行済
                            'id': record_no,
                            'record': {
                                '売上計上_chk': {
                                    'value': '済'
                                }
                            }
                        };
                        kintone.api(kintone.api.url('/k/v1/record.json', true), 'PUT', body, function(resp) {
                            // success
                            console.log(resp);
                        }, function(error) {
                            // error
                            console.log(error);
                        });
                        // ▲ 売上計上更新処理 ▲
                        // 売上計上Noの８桁を取得
                        // uriageno = u_no.slice(-8);
                        uriageno = u_no.substr(-8);
                        // 売上計上No検索処理
                        // ▽ *** 更新対象取得 *** ▽
                        var params = {
                            "app": 43, // 売上登録 移行済 
                            //'query': '受注No = "' + u_no + '"'
                            'query': 'uriage_no = "' + u_no + '"',
                            'fields': ['レコード番号', 'table']
                        };
                        console.log(params.query);
                        kintone.api(kintone.api.url('/k/v1/records', true), 'GET', params, function(resp) {
                            // すでにレコードが存在する場合の処理
                            if (resp) {
                                if (resp.records[0]) {
                                    //console.log(resp.records[0].テーブル.value.length);
                                    // テーブルの中身を取得(既存データIDを追加)
                                    var param_value = '';
                                    var param_value_arry = [];
                                    for (var i = 0; i < resp.records[0].table.value.length; i++) {
                                        //console.log(resp.records[0].テーブル.value[i].id);
                                        var p_id = resp.records[0].table.value[i].id;
                                        param_value += '{"id":"' + p_id + '"},';
                                        param_value_arry.push({
                                            "id": p_id
                                        });
                                        //ins_param.record.table.value.push({'id':p_id});
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
                                    console.log(param_value_arry);
                                    //param_value = '"value": [' + param_value  + ']';
                                    //console.log(param_value);
                                    //var str = '"value": [{"id":"73841"},{"id":"73843"},{"value":{"受注":{"value":4657}}}]';
                                    // テーブル更新用のパラメータを定義
                                    var ins_param = {
                                        "app": 43, // 売上登録　移行済
                                        "id": resp.records[0].レコード番号.value,
                                        "record": {
                                            "table": {
                                                "value": param_value_arry
                                            }
                                        }
                                    };
                                    // レコード追加
                                    kintone.api(kintone.api.url('/k/v1/record', true), 'PUT', ins_param, function(resp) {
                                        //success
                                        console.log(resp);
                                        window.alert('売上情報にレコードを追加しました。');
                                        // *** ▼▼ 画面遷移関連 ▼▼ ***
                                        //var new_window = window.open("/k/" + 38);
                                        //var new_window = window.location.href = "/k/38";
                                        //new_window.addEventListener("load", function () {
                                        //window.postMessage(new_window.kintone !== null, location.origin);
                                        //});
                                        // *** ▲▲ 画面遷移関連 ▲▲ ***
                                    }, function(error) {
                                        //error
                                        console.log(error);
                                        window.alert('売上の追加登録に失敗しました（システムエラー A001）');
                                    });
                                } else {
                                    console.log('レコード存在せず');
                                    console.log(record_no);
                                    //window.alert('レコード存在せず');
                                    // ▼ 売上新規登録処理 ▼
                                    // 登録用パラメータを定義
                                    var new_param = {
                                        "app": 43, //売上登録 移行済
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
                                    console.log(new_param.record.table);
                                    kintone.api(kintone.api.url('/k/v1/record', true), 'POST', new_param, function(resp) {
                                        // success
                                        window.alert('売上が見つからなかったので、新規登録しました。');
                                        // *** ▼▼ 画面遷移関連 ▼▼ ***
                                        //var new_window = window.open("/k/" + 38);
                                        //var new_window = window.location.href = "/k/38";
                                        //new_window.addEventListener("load", function () {
                                        //window.postMessage(new_window.kintone !== null, location.origin);
                                        //});
                                    }, function(error) {
                                        // error
                                        alert('売上情報の新規登録に失敗しました。（システムエラーA002）');
                                        console.log(error);
                                    });
                                    // ▲ 売上新規登録処理 ▲
                                }
                            }
                        }, function(error) {
                            // error
                            alert('売上情報の取得に失敗しました。（システムエラー）');
                        });
                        // △ *** 更新対象取得 *** △
                        // ▼ ***  入金元*** ▼
                        if (nyukinmoto != '') {
                            head = u_no.substr(0, 4);
                            // 入金元をゼロ埋め
                            nyukinmoto = ('0000' + nyukinmoto).slice(-4);
                            // 入金元用の売上Noの作成(売上Noの年月までの部分と入金元コードを合体)
                            uriageno2 = u_no.substr(-8).substr(0, 4) + nyukinmoto;
                            // 売上計上No検索処理
                            // ▽▼ *** 更新対象取得 *** ▼▽
                            var params = {
                                "app": 43, // 売上登録 移行済
                                //'query': '受注No = "' + u_no + '"'
                                //'query': 'uriage_no = "' + head + uriageno2 + '"',
                                'query': 'uriage_no like "' + uriageno2 + '"',
                                'fields': ['レコード番号', 'table']
                            };
                            console.log("※※入金元検索 " + params.query);
                            kintone.api(kintone.api.url('/k/v1/records', true), 'GET', params, function(resp) {
                                // すでにレコードが存在する場合の処理
                                if (resp) {
                                    if (resp.records[0]) {
                                        //console.log(resp.records[0].テーブル.value.length);
                                        // テーブルの中身を取得(既存データIDを追加)
                                        var param_value = '';
                                        var param_value_arry = [];
                                        for (var i = 0; i < resp.records[0].table.value.length; i++) {
                                            //console.log(resp.records[0].テーブル.value[i].id);
                                            var p_id = resp.records[0].table.value[i].id;
                                            param_value += '{"id":"' + p_id + '"},';
                                            param_value_arry.push({
                                                "id": p_id
                                            });
                                            //ins_param.record.table.value.push({'id':p_id});
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
                                        console.log(param_value_arry);
                                        //param_value = '"value": [' + param_value  + ']';
                                        //console.log(param_value);
                                        //var str = '"value": [{"id":"73841"},{"id":"73843"},{"value":{"受注":{"value":4657}}}]';
                                        // テーブル更新用のパラメータを定義
                                        var ins_param = {
                                            "app": 43, // 売上登録 移行済
                                            "id": resp.records[0].レコード番号.value,
                                            "record": {
                                                "table": {
                                                    "value": param_value_arry
                                                }
                                            }
                                        };
                                        // レコード追加
                                        kintone.api(kintone.api.url('/k/v1/record', true), 'PUT', ins_param, function(resp) {
                                            //success
                                            console.log(resp);
                                            window.alert('売上情報にレコードを追加しました。(入金元データ)');
                                            // *** ▼▼ 画面遷移関連 ▼▼ ***
                                            //var new_window = window.open("/k/" + 38);
                                            //var new_window = window.location.href = "/k/38";
                                            // new_window.addEventListener("load", function () {
                                            //  window.postMessage(new_window.kintone !== null, location.origin);
                                            //});
                                            // *** ▲▲ 画面遷移関連 ▲▲ ***
                                        }, function(error) {
                                            //error
                                            console.log(error);
                                            window.alert('売上の追加登録に失敗しました（システムエラーB002）');
                                        });
                                    } else {
                                        //console.log('レコード存在せず');
                                        //console.log(record_no);
                                        //window.alert('レコード存在せず');
                                        // ▼ 売上新規登録処理 ▼
                                        // 登録用パラメータを定義
                                        var new_param = {
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
                                        console.log(new_param.record.table);
                                        kintone.api(kintone.api.url('/k/v1/record', true), 'POST', new_param, function(resp) {
                                            // success
                                            window.alert('売上が見つからなかったので、新規登録しました。(入金元)');
                                            // *** ▼▼ 画面遷移関連 ▼▼ ***
                                            //var new_window = window.open("/k/" + 38);
                                            //var new_window = window.location.href = "/k/38";
                                            //new_window.addEventListener("load", function () {
                                            // window.postMessage(new_window.kintone !== null, location.origin);
                                            //});
                                        }, function(error) {
                                            // error
                                            console.log(error);
                                            console.log(error.errors);
                                            console.log(resp.errors);

                                            alert('売上情報の新規登録に失敗しました。（システムエラー A003）');
                                            //console.log(error);
                                        });
                                        // ▲ 売上新規登録処理 ▲
                                    }
                                }
                            }, function(error) {
                                // error
                                alert('売上情報の取得に失敗しました。（システムエラー）');
                            });
                            // △ *** 更新対象取得 *** △
                        }
                        // △ *** 入金元関連 *** △
                        // *** ▼▼ 画面遷移関連 ▼▼ ***
                        //var new_window = window.open("/k/" + 38);
                        //var new_window = window.location.href = "/k/38";
                        //new_window.addEventListener("load", function () {
                        //window.postMessage(new_window.kintone !== null, location.origin);
                        //});
                        // *** ▲▲ デバッグ ▲▲ ***

                        // *** ▲▲ 画面遷移関連 ▲▲ ***
                        //window.alert('A001');
                    }
                    //window.alert('A002');
                }
                //window.alert('A003');
            }
            //window.alert('A004');
        }
        var user = kintone.getLoginUser();
        console.log('User:' + user.id);
        if (user.id == '2' || user.id == '1') {
            kintone.app.record.getSpaceElement('my_space_field_03').appendChild(mySpaceFieldButton);
        }
    });
})();