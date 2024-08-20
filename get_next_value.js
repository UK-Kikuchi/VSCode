(function() {
	"use strict";

	kintone.events.on('app.record.create.show', function(event) {

	// 任意のスペースフィールドにボタンを設置
	var mySpaceFieldButton = document.createElement('button');
	mySpaceFieldButton.id = 'my_space_field_button';
	mySpaceFieldButton.innerText = '連番取得';
	mySpaceFieldButton.onclick = function () {
		var msg = '連番の取得に成功しました。';
		var nextvalue = '';
		// 更新のKeyを取得
		var key = '';
		var rec = kintone.app.record.get();
		if (rec) {
			key = rec.record.key.value;

			// ▽ *** 更新対象取得 *** ▽
      
			var params = {
			"app": 38,// 連番管理マスタ
			//'query': 'key = "T.M"',
			'query': 'key = "' + key + '"',
			'fields': ['レコード番号', 'key', 'nextvalue']
			};

      kintone.api(kintone.api.url('/k/v1/records', true), 'GET', params, function(resp) {
      // success
      //console.log(resp.records[0].レコード番号.value);
      var p_id = resp.records[0].レコード番号.value
      nextvalue = resp.records[0].nextvalue.value;
      if (nextvalue){
          var upd_nextvalue = Number(nextvalue) + 1;
          // ５桁のゼロ埋め
          var length = 5;
          if (nextvalue.length < length){
            nextvalue = Array(length).join('0') + nextvalue;
            nextvalue = nextvalue.slice(-length);
          } else {
            //alert('連番の取得に失敗しました。(連番が存在しません)');
          }
       		var record = kintone.app.record.get();
		      // フィールドの値の書き換え
		      record.record['orderno_c'].value = nextvalue;
		      kintone.app.record.set(record);
		      // ▼▼ 連番更新処理
	    		var params2 = {
    			"app": 38,// 連番管理マスタ
    			// "id": p_id,
    			"updateKey": {  "field": "key",  "value": key},
          "record": {"nextvalue": { "value": upd_nextvalue }}
			    };		      
			    kintone.api(kintone.api.url('/k/v1/record', true), 'PUT', params2, function(resp) {
             // success
            console.log(resp);
          }, function(error) {
            // error
            console.log(error);
          });
			    
		      // ▲▲ 連番更新処理
      }
	    //console.log(resp.records[0].nextvalue.value);
      alert('連番を取得しました。');
      }, function(error) {
      // error
      alert('連番の取得に失敗しました。（システムエラー）');
      });
			// △ *** 更新対象取得 *** △
			
		}

	
		kintone.app.record.getSpaceElement('my_space_field_02').innerText = msg;

	}
	kintone.app.record.getSpaceElement('my_space_field_01').appendChild(mySpaceFieldButton);
	});
})();