(function () {
    "use strict";
    kintone.events.on('app.record.index.show', function (event) {
        if (document.getElementById('my_index_button') !== null) {
            return;
        }
        var myIndexButton = document.createElement('button');
        myIndexButton.id = 'my_index_button';
        myIndexButton.innerText = '最新データ取得';
        // ボタンクリック時の処理
        myIndexButton.onclick = async () => {
            var result = window.confirm('受注最新データを取得します');
            if (result) {
                window.alert('処理を実行します。');
                // ############################################################## ↓ promise ↓ ##############################################################
                // クライアントの作成
                var client = new KintoneRestAPIClient();
                // 受注照会から全データを取得して削除
                const res1 = await client.record.getAllRecords({ app: '102' });
                console.log(res1);
                let ary1 = [];
                for (var i = 0; i < res1.length; i++) {
                    let obj = {
                        "id": res1[i].$id.value,
                    };
                    ary1.push(obj);

                }
                //console.log("*** 受注照会データ取得 ***");
                //console.log(res1);

                const res2 = await client.record.deleteAllRecords({
                    app: '102',
                    records: ary1
                });
                //console.log("*** 受注照会データ削除 ***");
                //console.log(res2);

                const res3 = await client.record.getAllRecords({ app: '60' });
                console.log("*** 受注データ取得 ***");
                console.log(res3);

                let ary2 = [];
                for (var i = 0; i < res3.length; i++) {
                    let jutyu_tbl = [];
                    for (var m = 0; m < res3[i].t_受注明細.value.length; m++) {
                        let obj = {
                            "value": {
                                "J_枝番": { "value": res3[i].t_受注明細.value[m].value.order_all_no.value },
                                "j_得意先注文番号": { "value": res3[i].t_受注明細.value[m].value.得意先注文番号.value },
                                "J_生産指示番号": {"value": res3[i].t_受注明細.value[m].value.契約番号.value  },
                                "J_商品名": {"value": res3[i].t_受注明細.value[m].value.商品名_自.value  },
                                "J_受注数量": {"value": res3[i].t_受注明細.value[m].value.受注数量.value  },
                                "J_受注金額": {"value": res3[i].t_受注明細.value[m].value.受注金額.value  }
                            }
                        };
                        jutyu_tbl.push(obj);
                    }  
                    // 関連する納品情報を取得してTBLに追加
                    var query = '受注情報 =' + res3[i].$id.value;
                    const nohin = await client.record.getAllRecords({ app: '59', condition: query });
                    console.log("*** ②納品情報 ***");
                    console.log(nohin);
                    let nohin_tbl = [];
                    for (var j = 0; j < nohin.length; j++) {
                        for (var m = 0; m < nohin[j].t_納品情報.value.length; m++) {
                            let obj = {
                                "value": {
                                    "N_納品情報": { "value": nohin[j].$id.value },
                                    "N_納品日": { "value": nohin[j].t_納品情報.value[m].value.納品日.value },
                                    "N_納品数量": {"value": nohin[j].t_納品情報.value[m].value.納品数量明細.value  },
                                    "N_請求価格": { "value": nohin[j].t_納品情報.value[m].value.請求価格_1.value }
                                }
                            };
                            nohin_tbl.push(obj);
                        }  
                    }
                    // 関連する請求情報を取得してTBLに追加
                    const seikyu = await client.record.getAllRecords({ app: '84', condition: query });
                    console.log("*** ③請求情報 ***");
                    console.log(seikyu);
                    let seikyu_tbl = [];
                    for (var k = 0; k < seikyu.length; k++) {
                        let obj = {
                            "value": {
                                "S_請求情報": { "value": seikyu[k].$id.value }
                            }
                        };
                        seikyu_tbl.push(obj);
                    }
                    let obj = {
                        "受注情報": { "value": res3[i].$id.value },
                        "TBL_受注情報": { "value": jutyu_tbl },
                        "TBL_納品情報": { "value": nohin_tbl },
                        "TBL_請求情報": { "value": seikyu_tbl }
                    };
                    ary2.push(obj);
                }

                const res4 = await client.record.addAllRecords({
                    app: '102',
                    records: ary2
                });
                console.log("*** 受注照会データ登録 ***");
                console.log(res4);
                window.alert('処理が終了しました。');

            } else {
                window.alert('処理をキャンセルしました。');
            }
        };
        kintone.app.getHeaderMenuSpaceElement().appendChild(myIndexButton);
    });
})();