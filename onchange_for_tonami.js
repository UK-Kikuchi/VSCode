/**
 * トナミ用データ加工
 */
(() => {
    'use strict';

    kintone.events.on(['app.record.create.submit', 'app.record.edit.submit', 'app.record.index.edit.submit'], (event) => {

        /**
         * 全角文字かチェックします。
         * @param src チェック対象の文字列
         * @returns 全角文字の場合 true
         */
        function isFullWidth(src) {
            return (String(src).match(/[\x01-\x7E\uFF65-\uFF9F]/)) ? false : true;
        }

        /**
         * バイト単位で文字列切り取り
         * @param src 対象の文字列
         * @param start 開始バイト
         * @param size 切り取るバイト数
         * @returns バイト単位で切り取った文字列
         */
        function substrByte(src, start, size) {
            console.log("src");
            console.log(src);
            if (src === undefined) {
                return '';
            }
            let result = ""
            let count1 = 0
            let count2 = 0

            for (let i = 0; i < src.length; i++) {
                const c = src.charAt(i)
                const char_size = isFullWidth(c) ? 2 : 1

                if (count1 >= start) {
                    count2 += char_size
                    if (count2 <= size) {
                        result += c
                    } else {
                        break
                    }
                }
                count1 += char_size
            }

            return result
        }


        function count(str) {
            let len = 0;
            for (let i = 0; i < str.length; i++) {
                (str[i].match(/[ -~]/)) ? len += 1 : len += 2;
            }
            return len;
        }
        const p_record = event.record;
        var p_nounyusaki = p_record.納入先住所.value;
        var p_unsoujyo1 = p_record.運送状_1.value;
        var p_unsoujyo2 = p_record.運送状_2.value;
        var p_unsoujyo3 = p_record.運送状_3.value;
        var p_unsoujyo4 = p_record.運送状_4.value;
        var p_unsoujyo5 = p_record.運送状_5.value;


        // 空白文字を削除
        //p_nounyusaki = p_nounyusaki.replace(/\s+/g, '');
        //console.log("p_nounyusaki:", count(p_nounyusaki));
        //console.log("p_nounyusaki:", substrByte(p_nounyusaki, 1, 56));
        //p_unsoujyo1 = p_unsoujyo1.replace(/\s+/g, '');
        //console.log("p_unsoujyo1:", count(p_unsoujyo1));
        //p_unsoujyo2 = p_unsoujyo2.replace(/\s+/g, '');
        //console.log("p_unsoujyo2:", count(p_unsoujyo2));
        //p_unsoujyo3 = p_unsoujyo3.replace(/\s+/g, '');
        //console.log("p_unsoujyo3:", count(p_unsoujyo3));
        //p_unsoujyo4 = p_unsoujyo4.replace(/\s+/g, '');
        //console.log("p_unsoujyo4:", count(p_unsoujyo4));
        //p_unsoujyo5 = p_unsoujyo5.replace(/\s+/g, '');
        //console.log("p_unsoujyo5:", count(p_unsoujyo5));

        // 文字数制限を超える場合は次のカラムに
        //var addr1 = substrByte(p_nounyusaki, 0, 56);
        //var addr2 = p_nounyusaki.replace(addr1, '');
        var addr1 = '';
        var addr2 = '';

        if (p_nounyusaki === undefined || p_nounyusaki == '' || p_nounyusaki == '#N/A!') {
            addr1 = '';
            addr2 = '';
        } else {
            var addr1 = substrByte(p_nounyusaki, 0, 56);
            var addr2 = p_nounyusaki.replace(addr1, '');
        }

        console.log("addr1:", addr1);
        console.log("addr2:", addr2);

        var rmk1 = '';
        var rmk2 = '';

        if (p_unsoujyo1 === undefined || p_unsoujyo1 == '' || p_unsoujyo1 == '#N/A!') {
            rmk1 = '';
            rmk2 = '';
        } else {
            rmk1 = substrByte(p_unsoujyo1, 0, 56);
            rmk2 = p_unsoujyo1.replace(rmk1, '');
        }
        console.log("p_unsoujyo1:", p_unsoujyo1);
        console.log("rmk1:", rmk1);
        console.log("rmk2:", rmk2);

        var rmk3 = '';
        var rmk4 = '';

        if (p_unsoujyo2 === undefined || p_unsoujyo2 == '' || p_unsoujyo2 == '#N/A!') {
            rmk3 = '';
            rmk4 = '';
        } else {
            rmk3 = substrByte(p_unsoujyo2, 0, 56);
            rmk4 = p_unsoujyo2.replace(rmk3, '');
        }

        console.log("p_unsoujyo2:", p_unsoujyo2);
        console.log("rmk3:", rmk3);
        console.log("rmk4:", rmk4);

        var rmk5 = '';
        var rmk6 = '';



        if (p_unsoujyo3 === undefined || p_unsoujyo3 == '' || p_unsoujyo3 == '#N/A!') {
            rmk5 = '';
            rmk6 = '';
        } else {
            rmk5 = substrByte(p_unsoujyo3, 0, 56);
            rmk6 = p_unsoujyo3.replace(rmk5, '');
        }

        console.log("p_unsoujyo3:", p_unsoujyo3);
        console.log("rmk5:", rmk5);
        console.log("rmk6:", rmk6);

        var rmk7 = '';
        var rmk8 = '';




        if (p_unsoujyo4 === undefined || p_unsoujyo4 == '' || p_unsoujyo4 == '#N/A!') {
            rmk7 = '';
            rmk8 = '';
        } else {
            rmk7 = substrByte(p_unsoujyo4, 0, 56);
            rmk8 = p_unsoujyo4.replace(rmk7, '');
        }
        console.log("p_unsoujyo4:", p_unsoujyo4);
        console.log("rmk7:", rmk7);
        console.log("rmk8:", rmk8);

        var rmk9 = '';
        var rmk10 = '';


        if (p_unsoujyo5 === undefined || p_unsoujyo5 == '' || p_unsoujyo5 == '#N/A!') {
            rmk9 = '';
            rmk10 = '';
        } else {
            rmk9 = substrByte(p_unsoujyo5, 0, 56);
            rmk10 = p_unsoujyo5.replace(rmk9, '');
        }
        console.log("p_unsoujyo5:", p_unsoujyo5);
        console.log("rmk9:", rmk9);
        console.log("rmk10:", rmk10);


        // 値をセット
        p_record.トナミ_addr1.value = addr1;
        p_record.トナミ_addr2.value = addr2;

        p_record.トナミ_rmk1.value = rmk1;
        p_record.トナミ_rmk2.value = rmk2;

        p_record.トナミ_rmk3.value = rmk3;
        p_record.トナミ_rmk4.value = rmk4;

        p_record.トナミ_rmk5.value = rmk5;
        p_record.トナミ_rmk6.value = rmk6;

        p_record.トナミ_rmk7.value = rmk7;
        p_record.トナミ_rmk8.value = rmk8;

        p_record.トナミ_rmk9.value = rmk9;
        p_record.トナミ_rmk10.value = rmk10;

        return event;
    });
})();