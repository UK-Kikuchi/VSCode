#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import datetime
from dateutil.relativedelta import relativedelta
import os
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog


# ファイル指定の関数
def dirdialog_clicked_001():
    iDir = os.path.abspath(os.path.dirname(__file__))
    iDirPath = filedialog.askdirectory(initialdir=iDir)
    entry001.set(iDirPath)


def dirdialog_clicked_002():
    iDir = os.path.abspath(os.path.dirname(__file__))
    iDirPath = filedialog.askdirectory(initialdir=iDir)
    entry002.set(iDirPath)


def selectbox_clicked_005_1(event):
    entry005_1.set(entry005_1.get())


def selectbox_clicked_005_2(event):
    entry005_2.set(entry005_2.get())

# コンボボックス


def selectbox_clicked_006(event):
    entry006.set(entry006.get())

# コンボボックス


def selectbox_clicked_007(event):
    entry007.set(entry007.get())

# 実行ボタン押下時の実行関数


def conductMain():
    p_msg = ""
    print(".... ▼ ＊＊＊ データ突合処理を開始します ＊＊＊ ▼")
    print(".... パラメータチェックを開始します。")
    isExcec = False

    # 突合データフォルダ
    p_tar = entry001.get()
    if p_tar == "":
        p_msg += "突合データ（フォルダ）を指定してください。\n"

    # 結果出力先
    p_res = entry002.get()
    if p_res == "":
        p_msg += "結果出力先（フォルダ）を指定してください。\n"

    # 対象年の取得
    p_tar_yyyy = entry005_1.get()
    tar_yyyy = p_tar_yyyy.replace('年', '')

    # 対象月の取得
    p_tar_m = entry005_2.get()
    tar_m = p_tar_m.replace('月', '')
    p_tar_month = p_tar_yyyy + p_tar_m

    # 日付型に変更
    # 翌月初(1月分進めて、1日にする)# => 2020-05-01
    next_month = datetime.date(int(tar_yyyy), int(
        tar_m), 1) + relativedelta(months=+1, day=1)
    p_to = next_month.strftime("%Y-%m-%d")
    # 検索条件を作成（今月の1日から翌月の1日まで）
    # 基準日
    p_tar_day = entry006.get()
    tar_d = p_tar_day.replace('日', '')
    p_from = tar_yyyy + "-" + tar_m + "-1"
    if p_tar != "" and p_res != "":
        isExcec = True

    if not isExcec:
        messagebox.showerror("error", p_msg)
        print("....NG 処理を中断しました。")
        return
    print(".... パラメータチェック .... OK")
    #################### ▼ メインの処理 ▼ ####################
    # ★★ デバッグ出力するかどうかのフラグ
    isOutputDbg = entry007.get()
    # print(isOutputDbg)

    if entry007.get() == 0:
        isOutputDbg = FALSE
    else:
        isOutputDbg = TRUE

    if isOutputDbg:
        # f_dbg = open( p_res + '/debug.txt', 'w', encoding='cp932')
        # エラー回避のためにUTF-8で統一
        f_dbg = open(p_res + '/debug.txt', 'w', encoding='utf-8')
        f_dbg.write(
            "処理実行日時：" + datetime.datetime.now().strftime('%Y年%m月%d日 %H:%M:%S'))
        f_dbg.write('\n')

    print(".... 突合データ解析処理を開始します。")

    files = os.listdir(p_tar)
    # フォルダにあるファイルを解析する
    # 売上データ・・・ 受注→ネクストエンジン→カスタマーリングのデータ(+ 繰越データ：ファイル名に[繰越]の文字が含まれる)
    # 入金データ・・・ 各ECサイトから出力した売上データ 各ECサイトからダウンロードしたままの形式で読み込む
    #  ポイントが存在するYahoo、楽天と過去からの繰越データが含まれる。
    uriage_list_normal = []  # 売上ファイル 通常
    uriage_list_point = []  # 売上ファイル ポイント
    nyukin_list_ebisu = []  # えびす
    nyukin_list_amazon = []  # Amazon
    nyukin_list_amazonPay = []  # AmazonPay
    nyukin_list_rakuten_pay = []  # 楽天ペイ
    nyukin_list_rakuten_coupon = []  # 楽天クーポン
    nyukin_list_yahoo_receipt = []  # Yahoo receipt
    nyukin_list_yahoo_billing = []  # Yahoo billing
    nyukin_list_aupay = []  # auPay
    jyogai_filename_list = []  # 除外ファイル
    kurikoshi_filename_list = []  # 繰越ファイル
    settei_filename_list = []  # 設定

    for f in files:
        file_kbn = "判定不能"  # 0:不明 1:えびす 2:Amazon 3:楽天 4:Yahoo 5:カスタマーリングス 6:auPay 7:OIC 99:設定 98:繰越
        data_kbn = "判定不能"  # 0:不明 1:売上 2:入金
        data_syubetu = "取り込み除外ファイル"
        # ファイルのみ実行(フォルダは除外)
        if (os.path.isfile(os.path.join(p_tar, f))):
            print(f + " 判定中...")
            # CSVファイルファイルの処理
            if (f.endswith(".csv")):
                if (f.startswith("receipt_")):
                    file_kbn = "Yahoo"  # Yahoo
                    data_kbn = "入金データ"  # 入金
                    data_syubetu = "receipt"

                if (f.startswith("billing_")):
                    file_kbn = "Yahoo"  # Yahoo
                    data_kbn = "入金データ"  # 入金
                    data_syubetu = "billing"

                if (f.startswith("seisansyo_")):
                    file_kbn = "えびす"  # えびす（ヤマト）
                    data_kbn = "入金データ"  # 入金
                    data_syubetu = "クレジットか代引きか"

                if (f.find("繰越") != -1):
                    file_kbn = "繰越"
                    data_kbn = "繰越"
                    data_syubetu = "繰越"

                row_no = 0
                fileobj = open(os.path.join(p_tar, f),
                               "r", encoding="cp932")
                # CSVファイルの行ごとに解析
                while True:
                    if row_no == 3:
                        break

                    line = fileobj.readline()
                    if line:
                        if row_no == 0:
                            # ▼ 設定判定 ▼ #
                            if "種別,項目,設定" in line:
                                file_kbn = "設定"
                                data_kbn = "設定"
                                data_syubetu = "設定"
                            # ▲ 設定判定 ▲
                            # ▼ えびす判定 ▼ #
                            if "支払区分,お客様コード,伝票番号,データ区分,訂正区分,利用サービス,決済手段,発送日,入金完了日,品代金,代引手数料,サービス手数料,スプリット手数料,印紙代相当額,返品日,返品伝票番号,電子マネー決済額,消費税,お届け先名,（お届け先）郵便番号,お客様管理番号,（お届け先）都道府県,（お届け先）市区郡町村,振込日,受付番号,伝票番号（他社便含む）" in line:
                                file_kbn = "えびす"  # えびす（ヤマト）
                                data_kbn = "入金データ"  # 入金
                                data_syubetu = "クレジットか代引きか"
                            # ▲ えびす判定 ▲
                            # ▼ auPay ▼
                            if "決済ID,黒赤区分,決済金額,取引ID,決済処理種別コード,決済処理種別名,取引発生日時,消込日時,キャンセル日時" in line:
                                file_kbn = "auPay"  # auPay
                                data_kbn = "入金データ"  # 入金
                                data_syubetu = "クレジットか代引きか"
                            # ▲ auPay ▲
                             # ▼ カスタマーリング判定 ▼ #
                            if "システムID,受注日,出荷確定日,受注キャンセル日,発送方法名,支払名,店舗コード,総合計,伝票番号,入金状況名,受注キャンセル区分,発送伝票番号,受注番号" in line:
                                file_kbn = "カスタマーリングス"  # カスタマーリングス
                                data_kbn = "売上データ"  # 売上
                                data_syubetu = "通常"
                            elif "システムID,受注日,出荷確定日,受注キャンセル日,発送方法名,支払名,店舗コード,ポイント,伝票番号,入金状況名,受注キャンセル区分,発送伝票番号,受注番号" in line:
                                file_kbn = "カスタマーリングス"  # カスタマーリングス
                                data_kbn = "売上データ"  # 売上
                                data_syubetu = "ポイント"
                            elif "システムID,受注日,出荷確定日,受注キャンセル日,発送方法名,支払名,店舗コード,ポイント,送料,伝票番号,入金状況名,受注キャンセル区分,発送伝票番号,受注番号" in line:
                                file_kbn = "カスタマーリングス"  # カスタマーリングス
                                data_kbn = "売上データ"  # 売上
                                data_syubetu = "ポイント"
                            # ▼ 楽天 ▼
                            elif line.startswith("精算書No"):
                                file_kbn = "楽天"  # 楽天
                                data_kbn = "入金データ"  # 入金
                            # ▲ 楽天 ▲
                        if row_no == 2:
                            #print("  *****" + str(line))
                            if line.startswith("\"■楽天ﾍﾟｲ_決済金"):
                                data_syubetu = "ペイ"
                            elif line.startswith("■楽天ﾍﾟｲ_決済金"):
                                data_syubetu = "ペイ"
                            elif line.startswith("\"■楽天ﾍﾟｲ_調整金"):
                                data_syubetu = "ペイ"
                            elif line.startswith("■楽天ﾍﾟｲ_調整金"):
                                data_syubetu = "ペイ"
                            elif line.startswith("\"■楽天ﾍﾟｲ_後払い決済"):
                                data_syubetu = "ペイ"
                            elif line.startswith("■楽天ﾍﾟｲ_後払い決済"):
                                data_syubetu = "ペイ"
                            elif line.startswith("\"■楽天ﾍﾟｲ_ｸｰﾎﾟﾝ利用注文分支払額"):
                                data_syubetu = "クーポン"
                            elif line.startswith("■楽天ﾍﾟｲ_ｸｰﾎﾟﾝ利用注文分支払額"):
                                data_syubetu = "クーポン"
                        row_no += 1
                    else:
                        break
            elif (f.endswith(".txt")):
                row_no = 0
                fileobj = open(os.path.join(p_tar, f),
                               "r", encoding="cp932")
                # CSVファイルの行ごとに解析
                while True:
                    if row_no == 2:
                        break
                    line = fileobj.readline()
                    if line:
                        if row_no == 0:
                            #print("  *****" + str(line))
                            if line.startswith("Amazon Payments Advanced"):
                                file_kbn = "AmazonPay"  # AmazonPay
                                data_kbn = "入金データ"  # 入金
                                data_syubetu = "txt"
                            elif line.startswith("\"Amazon Payments Advanced"):
                                file_kbn = "AmazonPay"  # AmazonPay
                                data_kbn = "入金データ"  # 入金
                                data_syubetu = "txt"
                            elif line.startswith("settlement-id"):
                                file_kbn = "Amazon"  # Amazon
                                data_kbn = "入金データ"  # 入金
                                data_syubetu = "txt"

                        row_no += 1
                    else:
                        break

        # ファイルの取り込み処理
        print("  * ファイル名：" + f)
        print("  * ファイル区分：" + str(file_kbn))
        print("  * データ区分：" + str(data_kbn))
        print("  * データ種別：" + str(data_syubetu))
        print("      .... OK ")

        # 売上データの取り込み処理（エラー回避のためにstrとして取り込む）
        if data_kbn == "売上データ":
            if data_syubetu == "通常":
                # ファイル名
                df = pd.DataFrame()
                df = pd.read_csv(os.path.join(p_tar, f), encoding="cp932", dtype="object")
                df['ファイル名'] = "【" + f + "】"
                uriage_list_normal.append(df)
                #    p_tar, f), encoding="cp932", dtype="object")
                #uriage_list_normal.append(pd.read_csv(os.path.join(
                #    p_tar, f), encoding="cp932", dtype="object"))
            elif data_syubetu == "ポイント":
                # ファイル名
                df = pd.DataFrame()
                df = pd.read_csv(os.path.join(p_tar, f), encoding="cp932", dtype="object")
                df['ファイル名'] = "【" + f + "】"
                uriage_list_point.append(df)
                
                #uriage_list_point.append(pd.read_csv(os.path.join(
                #    p_tar, f), encoding="cp932", dtype="object"))

        elif data_kbn == "入金データ":
            # ◆ Yahoo ◆
            if file_kbn == "Yahoo" and data_syubetu == "billing":
                # ファイル名
                df = pd.DataFrame()
                df = pd.read_csv(os.path.join(p_tar, f), encoding="cp932", dtype="object")
                df['ファイル名'] = "【" + f + "】"
                nyukin_list_yahoo_billing.append(df)
                #nyukin_list_yahoo_billing.append(pd.read_csv(
                #    os.path.join(p_tar, f), encoding="cp932", dtype="object"))
            elif file_kbn == "Yahoo" and data_syubetu == "receipt":
                # ファイル名
                df = pd.DataFrame()
                df = pd.read_csv(os.path.join(p_tar, f), encoding="cp932", dtype="object")
                df['ファイル名'] = "【" + f + "】"
                nyukin_list_yahoo_receipt.append(df)
                
                #nyukin_list_yahoo_receipt.append(pd.read_csv(
                #    os.path.join(p_tar, f), encoding="cp932", dtype="object"))
            # ◆ 楽天 ◆
            elif file_kbn == "楽天" and data_syubetu == "ペイ":
                # ファイル名
                df = pd.DataFrame()
                df = pd.read_csv(os.path.join(p_tar, f), encoding="cp932", skiprows=3, dtype="object")
                df['ファイル名'] = "【" + f + "】"
                nyukin_list_rakuten_pay.append(df)
                
                #nyukin_list_rakuten_pay.append(pd.read_csv(
                #    os.path.join(p_tar, f), encoding="cp932", skiprows=3, dtype="object"))
            elif file_kbn == "楽天" and data_syubetu == "クーポン":
                nyukin_list_rakuten_coupon.append(pd.read_csv(
                    os.path.join(p_tar, f), encoding="cp932", skiprows=3, dtype="object"))
             # ◆ えびす ◆
            elif file_kbn == "えびす":
                # ファイル名追加処理
                df = pd.DataFrame()
                df = pd.read_csv(os.path.join(p_tar, f), encoding="cp932", low_memory=False, dtype="object")
                df['ファイル名'] = "【" + f + "】"
                nyukin_list_ebisu.append(df)
                #nyukin_list_ebisu.append(pd.read_csv(os.path.join(
                #    p_tar, f), encoding="cp932", low_memory=False, dtype="object"))
             # ◆ auPay ◆
            elif file_kbn == "auPay":
                # ファイル名追加処理
                df = pd.DataFrame()
                df = pd.read_csv(os.path.join(p_tar, f), encoding="cp932", low_memory=False, dtype="object")
                df['ファイル名'] = "【" + f + "】"
                nyukin_list_aupay.append(df)
                
                #nyukin_list_aupay.append(pd.read_csv(os.path.join(
                #    p_tar, f), encoding="cp932", low_memory=False, dtype="object"))
             # ◆ Amazon ◆
            elif file_kbn == "Amazon":
                # ファイル名追加処理
                df = pd.DataFrame()
                df = pd.read_csv(os.path.join(p_tar, f), encoding="UTF-8", low_memory=False,  sep='\t', dtype='object')
                df['ファイル名'] = "【" + f + "】"
                nyukin_list_amazon.append(df)
                
                #nyukin_list_amazon.append(pd.read_csv(os.path.join(
                #    p_tar, f), encoding="UTF-8", low_memory=False,  sep='\t', dtype='object'))
                print("*** Amazon関連処理 ***")
                ########## Amazon 集計ファイル出力 ##########
                amazon_syukei = pd.read_csv(os.path.join(
                    p_tar, f), encoding="UTF-8", low_memory=False,  sep='\t', dtype='object')
                amazon_syukei = amazon_syukei[[
                    "order-id", "amount", "amount-description", "amount-type"]]
                amazon_syukei = amazon_syukei.rename(columns={
                                                     'order-id': 'order_id', 'amount-description': 'amount_description', 'amount-type': 'amount_type'})
                amazon_syukei.to_csv(
                    p_res + "\\" + p_tar_month + '_Amazon集計用ファイル_' + f + '.csv', encoding='UTF-8', index=False)
                ########## Amazon 集計ファイル出力 ##########
            # ◆ AmazonPay ◆
            elif file_kbn == "AmazonPay":
                print("*** AmazonPay関連処理 ***")
                # ファイル名追加処理
                df = pd.DataFrame()
                df = pd.read_csv(os.path.join(p_tar, f), encoding="UTF-8", dtype='object', low_memory=False, skiprows=6, header=None, names=['TransactionPostedDate', 'SettlementId', 'AmazonTransactionId', 'SellerReferenceId', 'TransactionType', 'AmazonOrderReferenceId', 'SellerOrderId', 'StoreName', 'CurrencyCode', 'TransactionDescription', 'TransactionAmount', 'TransactionPercentageFee', 'TransactionFixedFee', 'TotalTransactionFee', 'NetTransactionAmount'])
                df['ファイル名'] = "【" + f + "】"
                nyukin_list_amazonPay.append(df)
                
                #nyukin_list_amazonPay.append(pd.read_csv(os.path.join(p_tar, f), encoding="UTF-8", dtype='object', low_memory=False, skiprows=6, header=None, names=[
                #                           'TransactionPostedDate', 'SettlementId', 'AmazonTransactionId', 'SellerReferenceId', 'TransactionType', 'AmazonOrderReferenceId', 'SellerOrderId', 'StoreName', 'CurrencyCode', 'TransactionDescription', 'TransactionAmount', 'TransactionPercentageFee', 'TransactionFixedFee', 'TotalTransactionFee', 'NetTransactionAmount']))

        elif data_kbn == "設定":
            settei_filename_list.append(pd.read_csv(
                os.path.join(p_tar, f), encoding="cp932"))
        elif data_kbn == "繰越":
            # ファイル名追加処理
            df = pd.DataFrame()
            df = pd.read_csv(os.path.join(p_tar, f), encoding="cp932", dtype="object")
            df['ファイル名'] = "【" + f + "】"
            kurikoshi_filename_list.append(df)
            #kurikoshi_filename_list.append(pd.read_csv(os.path.join(p_tar, f), encoding="cp932", dtype="object"))

        else:
            jyogai_filename_list.append(f)

        if isOutputDbg:
            f_dbg.write("******************************" + '\n')
            f_dbg.write("  * ファイル名：" + f + '\n')
            f_dbg.write("  * ファイル区分：" + str(file_kbn) + '\n')
            f_dbg.write("  * データ区分：" + str(data_kbn) + '\n')
            f_dbg.write("  * データ種別：" + str(data_syubetu) + '\n')

    ##################################################
    #   設定データの確認
    ##################################################
    print(".... 設定データ解析処理を開始します。")
    if not settei_filename_list:
        messagebox.showerror("error", "設定データが存在しません、フォルダ内のデータを確認ください。")
        print("....NG 処理を中断しました。")
        return
    # 設定ファイルから値を取得
    settei = pd.concat(settei_filename_list, axis=0, sort=True)
    ebisu_credit_settei = settei.query(
        "種別 == 'えびす' & 項目 == 'クレジット'")['設定'].iloc[-1]
    # print("えびすクレジット：" + ebisu_credit_settei)
    ebisu_daibiki_settei = settei.query(
        "種別 == 'えびす' & 項目 == '代引き'")['設定'].iloc[-1]
    # print("えびす代引：" + ebisu_daibiki_settei)
    oic_settei = settei.query("種別 == 'OIC' & 項目 == 'コード'")['設定'].iloc[-1]
    bcart_settei = settei.query("種別 == 'Bカート' & 項目 == 'コード'")['設定'].iloc[-1]
    ##################################################
    #   分割処理
    ##################################################
    # えびすをクレジットと代引きに分割
    nyukin_ebisu_credit = ""
    nyukin_ebisu_daibiki = ""
    nyukin_oic = ""
    nyukin_bcart = ""
    if nyukin_list_ebisu:
        nyukin_ebisu = pd.concat(nyukin_list_ebisu, axis=0, sort=True)
        ##### 型変換 ### 
        nyukin_ebisu['品代金'] = nyukin_ebisu['品代金'].str.replace(',', '').fillna(0).astype(float)
        nyukin_ebisu_credit = nyukin_ebisu.query(ebisu_credit_settei)
        nyukin_ebisu_daibiki = nyukin_ebisu.query(ebisu_daibiki_settei)
        nyukin_oic = nyukin_ebisu.query(oic_settei)
        nyukin_bcart = nyukin_ebisu.query(bcart_settei)

    # 繰越データを売上と入金に分割
    kurikoshi_uriage = ""
    kurikoshi_nyukin = ""
    if kurikoshi_filename_list:
        kurikoshi = pd.concat(kurikoshi_filename_list, axis=0, sort=True)
        kurikoshi['日付'] = pd.to_datetime(kurikoshi['日付'])
        kurikoshi_uriage = kurikoshi.query("繰越区分 == '売上'")
        kurikoshi_nyukin = kurikoshi.query("繰越区分  == '入金'")

    ##################################################
    #   解析結果の書き出しと、EC毎のKEYの設定
    #       1:えびす =>
    #            →　さらにBカートOICを分岐
    #       2:Amazon =>
    #       3:楽天 =>
    #       4:Yahoo =>
    #       6:auPay =>
    ##################################################
    uriage_column = ""
    nyukin_colomun = ""
    if len(nyukin_bcart) > 0:
        print(".... 入金データは【Bカート】です。")
        uriage_column = settei.query("種別 == 'Bカート' & 項目 == '売上照合項目'")[
            '設定'].iloc[-1]
        nyukin_colomun = settei.query("種別 == 'Bカート' & 項目 == '入金照合項目'")[
            '設定'].iloc[-1]
        # データを出力
        nyukin_bcart.to_csv(p_res + "\\" + p_tar_month +
                            '_Bカート入金データ抽出.csv', encoding='cp932', index=False)
    if len(nyukin_oic) > 0:
        print(".... 入金データは【OIC】です。")
        uriage_column = settei.query("種別 == 'OIC' & 項目 == '売上照合項目'")[
            '設定'].iloc[-1]
        print("売上照合キー：", uriage_column)
        nyukin_colomun = settei.query("種別 == 'OIC' & 項目 == '入金照合項目'")[
            '設定'].iloc[-1]
        print("入金照合キー：", nyukin_colomun)
        # データを出力
        nyukin_oic.to_csv(p_res + "\\" + p_tar_month +
                          '_OIC入金データ抽出.csv', encoding='cp932', index=False)
    if len(nyukin_ebisu_credit) > 0:
        print(".... 入金データは【えびすクレジット】です。")
        uriage_column = settei.query("種別 == 'えびす' & 項目 == '売上照合項目（クレジット）'")[
            '設定'].iloc[-1]
        nyukin_colomun = settei.query("種別 == 'えびす' & 項目 == '入金照合項目（クレジット）'")[
            '設定'].iloc[-1]
        # データを出力
        nyukin_ebisu_credit.to_csv(p_res + "\\" + p_tar_month +
                                   '_えびすクレジット入金データ抽出.csv', encoding='cp932', index=False)
    if len(nyukin_ebisu_daibiki) > 0:
        print(".... 入金データは【えびす代引き】です。")

        uriage_column = settei.query("種別 == 'えびす' & 項目 == '売上照合項目（代引き）'")[
            '設定'].iloc[-1]
        nyukin_colomun = settei.query("種別 == 'えびす' & 項目 == '入金照合項目（代引き）'")[
            '設定'].iloc[-1]
        # データを出力
        nyukin_ebisu_daibiki.to_csv(p_res + "\\" + p_tar_month +
                                    '_えびす代引き入金データ抽出.csv', encoding='cp932', index=False)
    if len(nyukin_list_amazon) > 0:
        print(".... 入金データは【Amazon】です。")

        uriage_column = settei.query("種別 == 'Amazon' & 項目 == '売上照合項目'")[
            '設定'].iloc[-1]
        nyukin_colomun = settei.query("種別 == 'Amazon' & 項目 == '入金照合項目'")[
            '設定'].iloc[-1]
        taisyou_amazon = settei.query("種別 == 'Amazon' & 項目 == '対象項目'")['設定'].iloc[-1]
        taisyou_amazon_list = taisyou_amazon.split(",")
        
    if len(nyukin_list_rakuten_pay) > 0:
        print(".... 入金データは【楽天】です。")
        uriage_column = settei.query("種別 == '楽天' & 項目 == '売上照合項目'")[
            '設定'].iloc[-1]
        nyukin_colomun = settei.query("種別 == '楽天' & 項目 == '入金照合項目'")[
            '設定'].iloc[-1]
    if len(nyukin_list_yahoo_receipt) > 0:
        print(".... 入金データは【Yahoo】です。")
        uriage_column = settei.query("種別 == 'Yahoo' & 項目 == '売上照合項目'")[
            '設定'].iloc[-1]
        nyukin_colomun = settei.query("種別 == 'Yahoo' & 項目 == '入金照合項目'")[
            '設定'].iloc[-1]
        taisyou = settei.query("種別 == 'Yahoo' & 項目 == '対象項目'")['設定'].iloc[-1]
        taisyou_list = taisyou.split(",")
    if len(nyukin_list_aupay) > 0:
        print(".... 入金データは【auPay】です。")
        uriage_column = settei.query("種別 == 'auPay' & 項目 == '売上照合項目'")[
            '設定'].iloc[-1]
        nyukin_colomun = settei.query("種別 == 'auPay' & 項目 == '入金照合項目'")[
            '設定'].iloc[-1]
    ##################################################
    #   売上データ解析処理（共通）
    #   売上データの作成　→　ポイントデータのマージ　→　繰越データのマージ
    ##################################################
    print(".... 売上データ解析処理を開始します。")
    if not uriage_list_normal:
        messagebox.showerror("error", "売上データが存在しません、フォルダ内のデータを確認ください。")
        print("....NG 処理を中断しました。")
        return
    # 売上データを結合して金額項目を加工
    uriage = pd.concat(uriage_list_normal, axis=0, sort=True)
    ##### 型変換 ### 
    uriage['総合計'] = uriage['総合計'].str.replace(',', '').fillna(0).astype(float)
    uriage['出荷確定日'] = pd.to_datetime(uriage['出荷確定日'])
    # ◎　システム備考
    uriage['備考_売'] = "売(" + uriage['総合計'].astype(str) + ") " + uriage['ファイル名']

    # ***** ▽ ポイントマージ ▽ *****
    # カスタマーリングスに項目：ポイントが存在する場合は、ポイントを総合計に加算してやる
    if uriage_list_point:
        uriage_point = pd.concat(uriage_list_point, axis=0, sort=True)
        # ポイントを金額項目に加工
        uriage_point['ポイント'] = uriage_point['ポイント'].str.replace(
            ',', '').fillna(0).astype(float)

        # 受注番号をKeyに総合計とポイントをSUMしてから合計する。
        uriage_a = uriage[[uriage_column]]
        # uriage_a.to_csv('./temp/uriage_a.csv', encoding='cp932')
        uriage_b = uriage_point[[uriage_column]]
        # uriage_b.to_csv('./temp/uriage_b.csv', encoding='cp932')
        uriage_merge = pd.concat([uriage_a, uriage_b], axis=0).sort_values(
            uriage_column).drop_duplicates(keep='first')
        # uriage_merge.to_csv('./temp/uriage_merge.csv', encoding='cp932')
        # ポイント以外とポイントのキーを抽出↑

        uriage_goukei_sum = uriage[[uriage_column, "総合計"]].groupby(
            uriage_column).sum().rename(columns={'総合計': 'ポイント抜き合計額'})
        uriage_point_sum = uriage_point[[uriage_column, "ポイント"]].groupby(
            uriage_column).sum().rename(columns={'ポイント': 'ポイント'})

        uriage_merge = pd.merge(uriage_merge, uriage, left_on=uriage_column,
                                right_on=uriage_column, how='left').rename(columns={'総合計': '×'})
        uriage_merge = pd.merge(uriage_merge, uriage_goukei_sum, left_on=uriage_column,
                                right_on=uriage_column, how='left')
        uriage = pd.merge(uriage_merge, uriage_point_sum, left_on=uriage_column,
                          right_on=uriage_column, how='left')

        # ポイントを含めた総合計の計算
        uriage['総合計'] = uriage['ポイント抜き合計額'].fillna(0).astype(
            int) + uriage['ポイント'].fillna(0).astype(int)
        # ◎　システム備考
        uriage['備考_売ポ'] = "売ポ(" + uriage['総合計'].astype(str) + ") "  + uriage['ファイル名']
    # ***** △ ポイントマージ △ *****
    
    #uriage.to_csv('./temp/uriage_pointo_inc.csv', encoding='cp932')
    # ***** ▽ 繰越マージ(売上) ▽ *****

    # ★★
    # kurikoshi_uriage.to_csv('./temp/kurikoshi_uriage.csv', encoding='cp932')
    # uriage.to_csv('./temp/uriage.csv', encoding='cp932')
    # print("*** uriage_column ***")
    # print(uriage_column)

    if kurikoshi_uriage.size != 0:

        # 文字項目から数値項目への変更
        if kurikoshi_uriage['金額'].dtype == "object":
            kurikoshi_uriage['金額'] = kurikoshi_uriage['金額'].str.replace(
                ',', '').fillna(0).astype(float)
        if kurikoshi_uriage['ポイント'].dtype == "object":
            kurikoshi_uriage['ポイント'] = kurikoshi_uriage['ポイント'].str.replace(
                ',', '').fillna(0).astype(float)
        # ◎　システム備考
        kurikoshi_uriage['備考_売ポ'] = "売ポ(" + kurikoshi_uriage['ポイント'].astype(str) + ") "  + kurikoshi_uriage['ファイル名']
        # 項目名を加工
        kurikoshi_uriage = kurikoshi_uriage.rename(
            columns={'照合キー': uriage_column, '金額': '総合計', '日付': '出荷確定日'})
        # ◎　システム備考
        kurikoshi_uriage['備考_売繰'] = "売繰(" + kurikoshi_uriage['総合計'].astype(str) + ") "  + kurikoshi_uriage['ファイル名']
        # ★★
        # kurikoshi_uriage.to_csv('./temp/kurikoshi_uriage.csv', encoding='cp932')
        # uriage.to_csv('./temp/uriage_mae.csv', encoding='cp932')
        # 縦方向にマージ
        uriage = pd.concat([uriage, kurikoshi_uriage], axis=0)
        # ★★
        # uriage.to_csv('./temp/uriage.csv', encoding='cp932')
    # ***** △ 繰越マージ（売上） △ *****
    uriage = uriage.rename(
        columns={'出荷確定日': '【売上】出荷確定日', '支払名': '【売上】支払名'})
    # ◎　システム備考
    uriage['システム備考1'] = ""
    if '備考_売' in uriage.columns and '備考_売ポ' in uriage.columns and '備考_売繰' in uriage.columns:
       uriage['システム備考1'] = uriage['備考_売'].fillna('')  + uriage['備考_売ポ'].fillna('')  + uriage['備考_売繰'].fillna('') 
       #print("uriage['備考_売'] + uriage['備考_売ポ'] + uriage['備考_売繰']")
       #print(uriage['備考_売'].fillna('')  + uriage['備考_売ポ'].fillna('')  + uriage['備考_売繰'].fillna('') )

    if '備考_売' in uriage.columns and '備考_売ポ' not in uriage.columns and '備考_売繰' in uriage.columns:
       uriage['システム備考1'] = uriage['備考_売'].fillna('')  + uriage['備考_売繰'].fillna('') 
       #print("uriage['備考_売'] + uriage['備考_売繰']")
       #print(uriage['備考_売'].fillna('')  + uriage['備考_売繰'].fillna('') )

    if '備考_売' in uriage.columns and '備考_売ポ' in uriage.columns and '備考_売繰' not in uriage.columns:
       uriage['システム備考1'] = uriage['備考_売'].fillna('')  + uriage['備考_売ポ'].fillna('') 
       #print("uriage['備考_売'] + uriage['備考_売ポ']")
       #print(uriage['備考_売'].fillna('')  + uriage['備考_売ポ'].fillna('') )
    
    if '備考_売' in uriage.columns and '備考_売ポ' not in uriage.columns and '備考_売繰' not in uriage.columns:
       uriage['システム備考1'] = uriage['備考_売'].fillna('') 
       #print("uriage['備考_売']")
       #print(uriage['備考_売'].fillna('') )
            
    # ★★
    #uriage.to_csv('./temp/uriage_bikou.csv', encoding='cp932')
    # 売上データのKeyを抽出
    uriage_key = uriage[[uriage_column]].rename(columns={'受注番号': '照合キー'})
    uriage_key_cnt = uriage_key.value_counts()
    uriage_key_cnt = uriage_key.apply(pd.value_counts)
    uriage_key_cnt = uriage_key_cnt.rename(columns={'照合キー': '件数(売上)'})
    # Indexを列としてコピー
    uriage_key_cnt['Key'] = uriage_key_cnt.index

    # 2023.05.22 代引きのために照合キーではなく発送伝票番号でキーを作成
    # 2024.03.06 追加
    #if uriage[uriage_column].dtype == "int64":
    #    uriage[uriage_column] = uriage[uriage_column].astype(str)
        # ★★
        # uriage.to_csv('./temp/uriage_int64.csv', encoding='cp932')
    #if uriage[uriage_column].dtype == "float":
    #    uriage[uriage_column] = uriage[uriage_column].astype(str)
        # ★★
        # uriage.to_csv('./temp/uriage_float.csv', encoding='cp932')

    #if uriage[uriage_column].dtype == "float64":
    #    uriage[uriage_column] = uriage[uriage_column].astype(str)

    #uriage[uriage_column] = uriage[uriage_column].replace(
    #    "[\u3000 \t]", "", regex=True)


    #
    uriage_key2 = uriage[[uriage_column]].rename(
        columns={uriage_column: '照合キー'})
    uriage_key_cnt2 = uriage_key2.value_counts()
    uriage_key_cnt2 = uriage_key2.apply(pd.value_counts)
    uriage_key_cnt2 = uriage_key_cnt2.rename(columns={'照合キー': '件数(売上)'})
    # Indexを列としてコピー
    uriage_key_cnt2['Key'] = uriage_key_cnt2.index

    # ★★ debug
    if isOutputDbg:
        f_dbg.write("******************************" + '\n')
        f_dbg.write("** Uriage **\n")
        f_dbg.write(str(uriage.dtypes))
        f_dbg.write("\n")
        f_dbg.write("** Uriage key **\n")
        f_dbg.write(str(uriage_key.dtypes))
        f_dbg.write("\n")
        f_dbg.write("** Uriage key2(代引き照合用) **\n")
        f_dbg.write(str(uriage_key2.dtypes))
        f_dbg.write("\n")

    print(".... 売上データ解析処理 .... OK")
    ##################################################
    #   入金データ解析処理
    ##################################################
    print(".... 入金データ解析処理を開始します。")
    if not nyukin_list_ebisu and not nyukin_list_amazon and not nyukin_list_rakuten_pay and not nyukin_list_rakuten_coupon and not nyukin_list_yahoo_receipt and not nyukin_list_yahoo_billing and not nyukin_list_aupay:
        messagebox.showerror("error", "入金データが存在しません、フォルダ内のデータを確認ください。")
        print("....NG 処理を中断しました。")
        return

    #################### ▼ えびすクレジット ▼ ####################
    if len(nyukin_ebisu_credit) > 0:
        print("  【えびすクレジット】の処理を開始します。")
        ##### 型変換 ###
        # 分割のところで型変換は終わってるの！ 
        #nyukin_ebisu_credit['品代金'] = nyukin_ebisu_credit['品代金'].str.replace(',', '').fillna(0).astype(float)
        # ◎　システム備考
        nyukin_ebisu_credit['備考_入'] = "入(" + nyukin_ebisu_credit['品代金'].astype(str) + ") " + nyukin_ebisu_credit['ファイル名']
        # ***** ▽ 繰越マージ(入金) ▽ *****
        if kurikoshi_nyukin.size != 0:
            # 文字項目から数値項目への変更
            if kurikoshi_nyukin['金額'].dtype == "object":
                kurikoshi_nyukin['金額'] = kurikoshi_nyukin['金額'].str.replace(
                    ',', '').fillna(0).astype(float)
            if kurikoshi_nyukin['ポイント'].dtype == "object":
                kurikoshi_nyukin['ポイント'] = kurikoshi_nyukin['ポイント'].str.replace(
                    ',', '').fillna(0).astype(float)
            # ◎　システム備考
            kurikoshi_nyukin['備考_入繰'] = "入繰(" + kurikoshi_nyukin['金額'].astype(str) + ") " + kurikoshi_nyukin['ファイル名']
            kurikoshi_nyukin['備考_入ポ'] = "入ポ(" + kurikoshi_nyukin['ポイント'].astype(str) + ") " + kurikoshi_nyukin['ファイル名']
                
            # 項目名を加工
            kurikoshi_nyukin = kurikoshi_nyukin.rename(
                columns={'照合キー': nyukin_colomun, '金額': '品代金'})
            # 縦方向にマージ
            nyukin_ebisu_credit = pd.concat(
                [nyukin_ebisu_credit, kurikoshi_nyukin], axis=0)
            # nyukin_ebisu_credit.to_csv('./temp/nyukin_ebisu_credit.csv', encoding='cp932')
        # ***** △ 繰越マージ（入金） △ *****
        # ◎　システム備考
        nyukin_ebisu_credit['システム備考2'] = ""
        if '備考_入' in nyukin_ebisu_credit.columns and '備考_入ポ' in nyukin_ebisu_credit.columns and '備考_入繰' in nyukin_ebisu_credit.columns:
            nyukin_ebisu_credit['システム備考2'] = nyukin_ebisu_credit['備考_入'].fillna('')  + nyukin_ebisu_credit['備考_入ポ'].fillna('')  + nyukin_ebisu_credit['備考_入繰'].fillna('') 
        
        if '備考_入' in nyukin_ebisu_credit.columns and '備考_入ポ' not in nyukin_ebisu_credit.columns and '備考_入繰' in nyukin_ebisu_credit.columns:
            nyukin_ebisu_credit['システム備考2'] = nyukin_ebisu_credit['備考_入'].fillna('')  + nyukin_ebisu_credit['備考_入繰'].fillna('') 

        if '備考_入' in nyukin_ebisu_credit.columns and '備考_入ポ' in nyukin_ebisu_credit.columns and '備考_入繰' not in nyukin_ebisu_credit.columns:
            nyukin_ebisu_credit['システム備考2'] = nyukin_ebisu_credit['備考_入'].fillna('')  + nyukin_ebisu_credit['備考_入ポ'].fillna('') 
        
        if '備考_入' in nyukin_ebisu_credit.columns and '備考_入ポ' not in nyukin_ebisu_credit.columns and '備考_入繰' not in nyukin_ebisu_credit.columns:
            nyukin_ebisu_credit['システム備考2'] = nyukin_ebisu_credit['備考_入'].fillna('') 

        # ファイルを結合　→ リネーム →　件数表示用に加工
        bikou = pd.DataFrame(nyukin_ebisu_credit.groupby('受付番号')['システム備考2'].apply(lambda x: "%s" % ','.join(x)))
        
        ebisu = nyukin_ebisu_credit[["受付番号", "品代金"]].rename(
            columns={'受付番号': '【売上】受注番号', '品代金': '【売上】金額'}).groupby('【売上】受注番号').sum()
        
        ebisu = pd.concat([ebisu, bikou], axis=1)
        ### ★デバッグの為の出力 ###
        #bikou.to_csv('./temp/bikou.csv', encoding='cp932')
        #ebisu.to_csv('./temp/ebisu.csv', encoding='cp932')
        
        ############ 

        ebisu['【売上】受注番号2'] = ebisu.index
        ebisu_key = ebisu[['【売上】受注番号2']].rename(
            columns={'【売上】受注番号2': '照合キー'})
        ebisu_key_cnt = ebisu_key.value_counts()
        ebisu_key_cnt = ebisu_key.apply(pd.value_counts)
        ebisu_key_cnt = ebisu_key_cnt.rename(columns={'照合キー': '件数(入金)'})
        # Indexを列としてコピー
        ebisu_key_cnt['Key'] = ebisu_key_cnt.index
        # Keyをマージして重複をのぞいて並び替え
        key = pd.concat([uriage_key, ebisu_key], axis=0).sort_values(
            '照合キー').drop_duplicates(keep='first')
        # 売上-入金をマージ
        # データ
        if uriage['受注番号'].dtype == "int64":
            uriage['受注番号'] = uriage['受注番号'].astype(str)
        key = pd.merge(key, uriage, left_on='照合キー',
                       right_on='受注番号', how='left')

        if ebisu['【売上】受注番号2'].dtype == "int64":
            ebisu['【売上】受注番号2'] = ebisu['【売上】受注番号2'].astype(str)
        key = pd.merge(key, ebisu, left_on='照合キー',
                       right_on='【売上】受注番号2', how='left')
        # 件数
        if uriage_key_cnt['Key'].dtype == "int64":
            uriage_key_cnt['Key'] = uriage_key_cnt['Key'].astype(str)
        key = pd.merge(key, uriage_key_cnt, left_on='照合キー',
                       right_on='Key', how='left')

        if ebisu_key_cnt['Key'].dtype == "int64":
            ebisu_key_cnt['Key'] = ebisu_key_cnt['Key'].astype(str)
        key = pd.merge(key, ebisu_key_cnt, left_on='照合キー',
                       right_on='Key', how='left')

        if key['【売上】金額'].dtype == "object":
            key['【売上】金額'] = key['【売上】金額'].str.replace(
                ',', '').fillna(0).astype(float)
        if key['総合計'].dtype == "object":
            key['総合計'] = key['総合計'].str.replace(
                ',', '').fillna(0).astype(float)

        key['取引額'] = key['総合計']
        key['決済額'] = key['【売上】金額']
        key['繰越金額'] = 0.0
        key['差額'] = key['総合計'].fillna(0) - key['【売上】金額'].fillna(0)
        key['備考2'] = key['【売上】支払名']
        key['備考3'] = key['【売上】出荷確定日']
        key['照合結果'] = ""
        key['決済不能'] = ""
        key['顧客情報'] = ""
        key['情報2'] = ""
        key['判定情報'] = ""
        key['繰越区分'] = ""

        ### デバッグの為の出力 ###
        #key.to_csv('./temp/key.csv', encoding='cp932')
        # 結果出力用に成形
        key = key[["照合キー", "件数(売上)", "取引額", "件数(入金)", "決済額", "差額",
                   "照合結果", "決済不能", "顧客情報", "情報2", "備考2", "備考3", "判定情報", "店舗コード","システム備考1","システム備考2"]]
        #key.to_csv('./temp/key2.csv', encoding='cp932')
        ########## ▼  突合結果書き込み処理  ▼ ##########
        d = datetime.datetime(int(tar_yyyy), int(tar_m), int(tar_d))
        print(".... 【えびすクレジット】の処理 .... OK ")
        print(".... 突合データ出力処理を開始します。")
        for index, row in key.iterrows():

            # 入金データ存在チェック
            if (row['件数(売上)'] == 1 and pd.isna(row['件数(入金)']) and row['備考3'] > d):
                key.at[index, '判定情報'] = "翌月データ"
                key.at[index, '照合結果'] = "キー不一致"
            elif (row['件数(売上)'] == 1 and pd.isna(row['件数(入金)'])):
                key.at[index, '判定情報'] = "入金データなし"
                key.at[index, '照合結果'] = "キー不一致"
            # 差額チェック
            elif (row['差額'] == 0):
                key.at[index, '判定情報'] = "差額なし"
                key.at[index, '照合結果'] = "OK"
            # elif(row['差額'] + row['ポイント'] == 0):
            #    key.at[index, '判定情報'] = "差額なし（ポイントあり）"
            #    key.at[index, '照合結果'] = "OK"
            # elif(row['差額'] + row['ポイント'] == 250 and row['備考2'].find('えびすクレジット後払い') != -1):
            #    key.at[index, '判定情報'] = "えびすクレジット後払い"
            #    key.at[index, '照合結果'] = "OK"
            # elif(str(row['備考2']).find('えびすクレジット後払い') != -1 and row['差額'] == 250):
            #    key.at[index, '判定情報'] = "えびすクレジット後払い"
            #    key.at[index, '照合結果'] = "OK"
            # elif(row['差額'] != 0 and row['ポイント'] != 0):
            #    key.at[index, '判定情報'] = "代引き＋ポイント"
            #    key.at[index, '照合結果'] = "OK"
            else:
                key.at[index, '照合結果'] = "金額相違"
            # 入金データ存在チェック
            if (row['件数(入金)'] == 1 and pd.isna(row['件数(売上)'])):
                key.at[index, '判定情報'] = "売上データなし"
                key.at[index, '照合結果'] = "キー不一致"
        ########## ▲ ▲ ##########
        ### デバッグの為の出力 ###
        # key.to_csv('./temp/key.csv', encoding='cp932')
        key.to_csv(p_res + "\\" + p_tar_month + '_えびすクレジット結果.csv',
                   encoding='cp932', index=False)
        print(".... 突合データ出力処理 .... OK ")
        # 翌月繰越データ出力
        print(".... 翌月繰越データの出力を開始します。 .... OK ")
        yokugetu = key.query('判定情報 == "翌月データ"').copy()
        # yokugetu[['繰越区分']] = "前月繰越"
        yokugetu = yokugetu.rename(
            columns={'照合キー': '照合キー', '取引額': '金額', '備考3': '日付', '備考2': '備考'})
        yokugetu[['繰越区分']] = "入金"
        yokugetu[['ポイント']] = "0"
        yokugetu[['特記事項']] = "システム繰越"
        yokugetu = yokugetu[["繰越区分", "照合キー", "金額", "ポイント", "日付", "備考", "特記事項"]]
        yokugetu.to_csv(p_res + "\\" + p_tar_month +
                        '_えびすクレジット_翌月繰越.csv', encoding='cp932', index=False)

        # 金額相違データ出力
        print(".... 金額相違データの出力を開始します。 .... OK ")
        soui = key.query('照合結果 == "金額相違"').copy()
        soui[['繰越区分']] = "金額相違"
        soui.to_csv(p_res + "\\" + p_tar_month + '_えびすクレジット_金額相違.csv',
                    encoding='cp932', index=False)

        # キー不一致データ出力
        print(".... キー不一致データの出力を開始します。 .... OK ")
        uriage_nasi = key.query('照合結果 == "キー不一致" & 判定情報 == "売上データなし"').copy()
        uriage_nasi[['繰越区分']] = "売上データなし"
        uriage_nasi.to_csv(p_res + "\\" + p_tar_month +
                           '_えびすクレジット_売上データなし.csv', encoding='cp932', index=False)

        nyukin_nasi = key.query('照合結果 == "キー不一致" & 判定情報 == "入金データなし"').copy()
        nyukin_nasi[['繰越区分']] = "入金データなし"
        nyukin_nasi.to_csv(p_res + "\\" + p_tar_month +
                           '_えびすクレジット_入金データなし.csv', encoding='cp932', index=False)

        print(".... 翌月繰越データの出力 .... OK ")
        # 集計データ出力
        print(".... 集計データの出力を開始します。 .... OK ")
        f = open(p_res + "\\" + p_tar_month +
                 '_えびすクレジット集計結果.txt', 'w', encoding='cp932')

        ####################################################
        p_tmp = '*'
        try:
            p_tmp = key['件数(売上)'].sum()
        except:
            p_tmp = 0.0
        f.write('件数(売上):' + str(p_tmp) + '件\n')
        print('件数(売上):' + str(p_tmp) + '件')
        try:
            p_tmp = key['件数(入金)'].sum()
        except:
            p_tmp = 0.0
        f.write('件数(入金):' + str(p_tmp) + '件\n')
        print('件数(入金):' + str(p_tmp) + '件')
        try:
            p_tmp = key['件数(繰越)'].sum()
        except:
            p_tmp = 0.0
        f.write('件数(繰越):' + str(p_tmp) + '件\n')
        print('件数(繰越):' + str(p_tmp) + '件')
        f.write('****************************************\n')
        # 照合結果に記載されている分結果を書き込む
        p_hantei_list = key['照合結果'].unique().tolist()
        for keyword in p_hantei_list:
            p_amt = '*'
            p_cnt = '*'
            try:
                p_amt = key.query("照合結果 == '" + keyword + "'")['取引額'].sum()
                p_cnt = key.query("照合結果 == '" + keyword + "'")['取引額'].count()
            except:
                p_amt = 0.0
                p_cnt = 0.0

            f.write(keyword + '：' + str(p_cnt) + '件 ' + str(p_amt) + '円\n')
            print(keyword + '：' + str(p_cnt) + '件 ' + str(p_amt) + '円')
        f.write('****************************************\n')
        f.write("処理実行日時：" + datetime.datetime.now().strftime('%Y年%m月%d日 %H:%M:%S'))
        f.write('\n')
        f.write("突合データ（フォルダ）:" + p_tar)
        f.write('\n')
        f.write("結果出力先（フォルダ）:" + p_res)
        f.write('\n')
        f.write("出力先：" + p_res)
        f.write('\n')
        f.write("処理対象：" + p_tar_month)
        f.write('\n')
        f.write("出荷確定日 >= " + p_from + " < " + p_to)
        f.write('\n')
        f.write("繰越基準日：" + tar_yyyy + "年" + tar_m + "月" + tar_d + "日")
        f.write('\n')
        f.close()
        print(".... 集計データの出力 .... OK ")

    #################### ▲ えびすクレジット ▲ ####################
    #################### ▼ 代引き ▼ ####################

    # やまと　＝　伝票番号（他社便含む）
    # カスタマーリングス＝　発送伝票番号
    # 代引きは売上データそのもののマッチングキーを変更する必要あり！！ #
    if len(nyukin_ebisu_daibiki) > 0:
        print("  【代引き】の処理を開始します。")
        # お試し
        nyukin_ebisu_daibiki[nyukin_colomun] = "x_" + nyukin_ebisu_daibiki[nyukin_colomun]

        # ◎　システム備考
        nyukin_ebisu_daibiki['備考_入'] = "入(" + nyukin_ebisu_daibiki['品代金'].astype(str) + ") " + nyukin_ebisu_daibiki['ファイル名']
        # ★★
        #nyukin_ebisu_daibiki.to_csv('./temp/nyukin_ebisu_daibiki.csv', encoding='cp932')
        # ***** ▽ 繰越マージ(入金) ▽ *****
        if kurikoshi_nyukin.size != 0:
            # お試し
            kurikoshi_nyukin['照合キー'] = "x_" + kurikoshi_nyukin['照合キー']    
            # 文字項目から数値項目への変更
            if kurikoshi_nyukin['金額'].dtype == "object":
                kurikoshi_nyukin['金額'] = kurikoshi_nyukin['金額'].str.replace(
                    ',', '').fillna(0).astype(float)
            if kurikoshi_nyukin['ポイント'].dtype == "object":
                kurikoshi_nyukin['ポイント'] = kurikoshi_nyukin['ポイント'].str.replace(
                    ',', '').fillna(0).astype(float)
                
            # ◎　システム備考
            kurikoshi_nyukin['備考_入繰'] = "入繰(" + kurikoshi_nyukin['金額'].astype(str) + ") " + kurikoshi_nyukin['ファイル名']
            kurikoshi_nyukin['備考_入ポ'] = "入ポ(" + kurikoshi_nyukin['ポイント'].astype(str) + ") " + kurikoshi_nyukin['ファイル名']
            
            # 項目名を加工
            kurikoshi_nyukin = kurikoshi_nyukin.rename(
                columns={'照合キー': nyukin_colomun, '金額': '品代金'})
            # 縦方向にマージ
            nyukin_ebisu_daibiki = pd.concat(
                [nyukin_ebisu_daibiki, kurikoshi_nyukin], axis=0)
            # ★★
            # nyukin_ebisu_daibiki.to_csv('./temp/nyukin_ebisu_daibiki.csv', encoding='cp932')
        # ***** △ 繰越マージ（入金） △ *****
        # ◎　システム備考
        nyukin_ebisu_daibiki['システム備考2'] = ""
        if '備考_入' in nyukin_ebisu_daibiki.columns and '備考_入ポ' in nyukin_ebisu_daibiki.columns and '備考_入繰' in nyukin_ebisu_daibiki.columns:
            nyukin_ebisu_daibiki['システム備考2'] = nyukin_ebisu_daibiki['備考_入'].fillna('')  + nyukin_ebisu_daibiki['備考_入ポ'].fillna('')  + nyukin_ebisu_daibiki['備考_入繰'].fillna('') 
        
        if '備考_入' in nyukin_ebisu_daibiki.columns and '備考_入ポ' not in nyukin_ebisu_daibiki.columns and '備考_入繰' in nyukin_ebisu_daibiki.columns:
            nyukin_ebisu_daibiki['システム備考2'] = nyukin_ebisu_daibiki['備考_入'].fillna('')  + nyukin_ebisu_daibiki['備考_入繰'].fillna('') 

        if '備考_入' in nyukin_ebisu_daibiki.columns and '備考_入ポ' in nyukin_ebisu_daibiki.columns and '備考_入繰' not in nyukin_ebisu_daibiki.columns:
            nyukin_ebisu_daibiki['システム備考2'] = nyukin_ebisu_daibiki['備考_入'].fillna('')  + nyukin_ebisu_daibiki['備考_入ポ'].fillna('') 
        
        if '備考_入' in nyukin_ebisu_daibiki.columns and '備考_入ポ' not in nyukin_ebisu_daibiki.columns and '備考_入繰' not in nyukin_ebisu_daibiki.columns:
            nyukin_ebisu_daibiki['システム備考2'] = nyukin_ebisu_daibiki['備考_入'].fillna('') 
        ### デバッグの為の出力 ###
        # ★★
        # nyukin_ebisu_daibiki.to_csv('./temp/nyukin_ebisu_daibiki.csv', encoding='cp932')

        # nyukin_ebisu_daibiki[nyukin_colomun] = nyukin_ebisu_daibiki[nyukin_colomun].str.replace(
        #    '.0', '')
        # uriage['発送伝票番号'] = uriage['発送伝票番号'].replace("[\u3000 \t]", "", regex=True)
        bikou = pd.DataFrame(nyukin_ebisu_daibiki.groupby(nyukin_colomun)['システム備考2'].apply(lambda x: "%s" % ','.join(x)))
        
        ebisu = nyukin_ebisu_daibiki[[nyukin_colomun, "品代金"]].rename(
            columns={nyukin_colomun: '【売上】受注番号', '品代金': '【売上】金額'}).groupby('【売上】受注番号').sum()
        
        ebisu = pd.concat([ebisu, bikou], axis=1)


        #ebisu = nyukin_ebisu_daibiki[[nyukin_colomun, "品代金"]].rename(
        #    columns={nyukin_colomun: '【売上】受注番号', '品代金': '【売上】金額'}).groupby('【売上】受注番号').sum()

        # ★★
        # ebisu.to_csv('./temp/ebisu.csv', encoding='cp932')
        # uriage.to_csv('./temp/uriage.csv', encoding='cp932')

        # お試し
        uriage[[uriage_column]] = "x_" + uriage[[uriage_column]]
        
        uriage_key2 = uriage[[uriage_column]].rename(
        columns={uriage_column: '照合キー'})
        uriage_key_cnt2 = uriage_key2.value_counts()
        uriage_key_cnt2 = uriage_key2.apply(pd.value_counts)
        uriage_key_cnt2 = uriage_key_cnt2.rename(columns={'照合キー': '件数(売上)'})
        # Indexを列としてコピー
        uriage_key_cnt2['Key'] = uriage_key_cnt2.index


        ebisu['【売上】受注番号2'] = ebisu.index
        ebisu_key = ebisu[['【売上】受注番号2']].rename(
            columns={'【売上】受注番号2': '照合キー'})
        ebisu_key_cnt = ebisu_key.value_counts()
        ebisu_key_cnt = ebisu_key.apply(pd.value_counts)
        ebisu_key_cnt = ebisu_key_cnt.rename(columns={'照合キー': '件数(入金)'})
        # Indexを列としてコピー
        ebisu_key_cnt['Key'] = ebisu_key_cnt.index

        ### デバッグの為の出力 ###
        # ★★
        # ebisu.to_csv('./temp/daibiki.csv', encoding='cp932')
        # ebisu_key.to_csv('./temp/daibiki_key.csv', encoding='cp932')
        # ebisu_key_cnt.to_csv('./temp/daibiki_key_cnt.csv', encoding='cp932')
        # print(uriage_key2.dtypes)
        # print(ebisu_key.dtypes)
        # Keyをマージして重複をのぞいて並び替え
        key = pd.concat([uriage_key2, ebisu_key],
                        axis=0).drop_duplicates(keep='first')
        # 売上-入金をマージ
        key = pd.merge(key, uriage, left_on='照合キー',
                       right_on=uriage_column, how='left')
        key = pd.merge(key, ebisu, left_on='照合キー',
                       right_on='【売上】受注番号2', how='left')
        key = pd.merge(key, uriage_key_cnt2, left_on='照合キー',
                       right_on='Key', how='left')
        key = pd.merge(key, ebisu_key_cnt, left_on='照合キー',
                       right_on='Key', how='left')

        key['取引額'] = key['総合計']
        key['決済額'] = key['【売上】金額']
        key['繰越金額'] = 0.0
        key['差額'] = key['総合計'].fillna(0) - key['【売上】金額'].fillna(0)
        key['備考2'] = key['【売上】支払名']
        key['備考3'] = key['【売上】出荷確定日']
        key['照合結果'] = ""
        key['決済不能'] = ""
        key['顧客情報'] = ""
        key['情報2'] = ""
        key['判定情報'] = ""
        key['繰越区分'] = ""
        key = key[["照合キー", "件数(売上)", "取引額", "件数(入金)", "決済額", "差額",
                   "照合結果", "決済不能", "顧客情報", "情報2", "備考2", "備考3", "判定情報", "店舗コード","システム備考1","システム備考2"]]

        ########## ▼  突合結果書き込み処理  ▼ ##########
        d = datetime.datetime(int(tar_yyyy), int(tar_m), int(tar_d))
        print(".... 【代引き】の処理 .... OK ")
        print(".... 突合データ出力処理を開始します。")
        for index, row in key.iterrows():

            # 入金データ存在チェック
            if (row['件数(売上)'] == 1 and pd.isna(row['件数(入金)']) and row['備考3'] > d):
                key.at[index, '判定情報'] = "翌月データ"
                key.at[index, '照合結果'] = "キー不一致"
            elif (row['件数(売上)'] == 1 and pd.isna(row['件数(入金)'])):
                key.at[index, '判定情報'] = "入金データなし"
                key.at[index, '照合結果'] = "キー不一致"
            # 差額チェック
            elif (row['差額'] == 0):
                key.at[index, '判定情報'] = "差額なし"
                key.at[index, '照合結果'] = "OK"
            # elif(row['差額'] + row['ポイント'] == 0):
            #    key.at[index, '判定情報'] = "差額なし（ポイントあり）"
            #    key.at[index, '照合結果'] = "OK"
            # elif(row['差額'] + row['ポイント'] == 250 and row['備考2'].find('えびすクレジット後払い') != -1):
            #    key.at[index, '判定情報'] = "えびすクレジット後払い"
            #    key.at[index, '照合結果'] = "OK"
            # elif(str(row['備考2']).find('えびすクレジット後払い') != -1 and row['差額'] == 250):
            #    key.at[index, '判定情報'] = "えびすクレジット後払い"
            #    key.at[index, '照合結果'] = "OK"
            # elif(row['差額'] != 0 and row['ポイント'] != 0):
            #    key.at[index, '判定情報'] = "代引き＋ポイント"
            #    key.at[index, '照合結果'] = "OK"
            else:
                key.at[index, '照合結果'] = "金額相違"
            # 入金データ存在チェック
            if (row['件数(入金)'] == 1 and pd.isna(row['件数(売上)'])):
                key.at[index, '判定情報'] = "売上データなし"
                key.at[index, '照合結果'] = "キー不一致"
        ########## ▲ ▲ ##########
        ### デバッグの為の出力 ###
        # key.to_csv('./temp/key.csv', encoding='cp932')
        key.to_csv(p_res + "\\" + p_tar_month + '_代引き結果.csv',
                   encoding='cp932', index=False)
        print(".... 突合データ出力処理 .... OK ")
        # 翌月繰越データ出力
        print(".... 翌月繰越データの出力を開始します。 .... OK ")
        yokugetu = key.query('判定情報 == "翌月データ"').copy()
        yokugetu = yokugetu.rename(
            columns={'取引額': '金額', '備考3': '日付', '備考2': '備考'})
        yokugetu['照合キー'] =  yokugetu['照合キー'].str.strip('x_') 
        yokugetu[['繰越区分']] = "入金"
        yokugetu[['ポイント']] = "0"
        yokugetu[['特記事項']] = "システム繰越"
        yokugetu = yokugetu[["繰越区分", "照合キー", "金額", "ポイント", "日付", "備考", "特記事項"]]
        yokugetu.to_csv(p_res + "\\" + p_tar_month +
                        '_代引き_翌月繰越.csv', encoding='cp932', index=False)

        # 金額相違データ出力
        print(".... 金額相違データの出力を開始します。 .... OK ")
        soui = key.query('照合結果 == "金額相違"').copy()
        soui[['繰越区分']] = "金額相違"
        soui.to_csv(p_res + "\\" + p_tar_month + '_代引き_金額相違.csv',
                    encoding='cp932', index=False)

        # キー不一致データ出力
        print(".... キー不一致データの出力を開始します。 .... OK ")
        uriage_nasi = key.query('照合結果 == "キー不一致" & 判定情報 == "売上データなし"').copy()
        uriage_nasi[['繰越区分']] = "売上データなし"
        uriage_nasi.to_csv(p_res + "\\" + p_tar_month +
                           '_代引き_売上データなし.csv', encoding='cp932', index=False)

        nyukin_nasi = key.query('照合結果 == "キー不一致" & 判定情報 == "入金データなし"').copy()
        nyukin_nasi[['繰越区分']] = "入金データなし"
        nyukin_nasi.to_csv(p_res + "\\" + p_tar_month +
                           '_代引き_入金データなし.csv', encoding='cp932', index=False)

        print(".... 翌月繰越データの出力 .... OK ")
        # 集計データ出力
        print(".... 集計データの出力を開始します。 .... OK ")
        f = open(p_res + "\\" + p_tar_month +
                 '_代引き集計結果.txt', 'w', encoding='cp932')

        ####################################################
        p_tmp = '*'
        try:
            p_tmp = key['件数(売上)'].sum()
        except:
            p_tmp = 0.0
        f.write('件数(売上):' + str(p_tmp) + '件\n')
        print('件数(売上):' + str(p_tmp) + '件')
        try:
            p_tmp = key['件数(入金)'].sum()
        except:
            p_tmp = 0.0
        f.write('件数(入金):' + str(p_tmp) + '件\n')
        print('件数(入金):' + str(p_tmp) + '件')
        try:
            p_tmp = key['件数(繰越)'].sum()
        except:
            p_tmp = 0.0
        f.write('件数(繰越):' + str(p_tmp) + '件\n')
        print('件数(繰越):' + str(p_tmp) + '件')
        f.write('****************************************\n')
        # 照合結果に記載されている分結果を書き込む
        p_hantei_list = key['照合結果'].unique().tolist()
        for keyword in p_hantei_list:
            p_amt = '*'
            p_cnt = '*'
            try:
                p_amt = key.query("照合結果 == '" + keyword + "'")['取引額'].sum()
                p_cnt = key.query("照合結果 == '" + keyword + "'")['取引額'].count()
            except:
                p_amt = 0.0
                p_cnt = 0.0

            f.write(keyword + '：' + str(p_cnt) + '件 ' + str(p_amt) + '円\n')
            print(keyword + '：' + str(p_cnt) + '件 ' + str(p_amt) + '円')
        f.write('****************************************\n')
        f.write("処理実行日時：" + datetime.datetime.now().strftime('%Y年%m月%d日 %H:%M:%S'))
        f.write('\n')
        f.write("突合データ（フォルダ）:" + p_tar)
        f.write('\n')
        f.write("結果出力先（フォルダ）:" + p_res)
        f.write('\n')
        f.write("出力先：" + p_res)
        f.write('\n')
        f.write("処理対象：" + p_tar_month)
        f.write('\n')
        f.write("出荷確定日 >= " + p_from + " < " + p_to)
        f.write('\n')
        f.write("繰越基準日：" + tar_yyyy + "年" + tar_m + "月" + tar_d + "日")
        f.write('\n')
        f.close()
        print(".... 集計データの出力 .... OK ")
    #################### ▲ えびす代引き ▲ ####################
    #################### ▼ OIC ▼ ####################

    # やまと　＝　伝票番号（他社便含む）
    # カスタマーリングス＝　発送伝票番号
    # 代引きは売上データそのもののマッチングキーを変更する必要あり！！ #
    if len(nyukin_oic) > 0:
        print("【OIC】の処理を開始します。")
        # ◎　システム備考
        nyukin_oic['備考_入'] = "入(" + nyukin_oic['品代金'].astype(str) + ") " + nyukin_oic['ファイル名']
        
        # ***** ▽ 繰越マージ(入金) ▽ *****
        if kurikoshi_nyukin.size != 0:
            # 文字項目から数値項目への変更
            if kurikoshi_nyukin['金額'].dtype == "object":
                kurikoshi_nyukin['金額'] = kurikoshi_nyukin['金額'].str.replace(
                    ',', '').fillna(0).astype(float)
            if kurikoshi_nyukin['ポイント'].dtype == "object":
                kurikoshi_nyukin['ポイント'] = kurikoshi_nyukin['ポイント'].str.replace(
                    ',', '').fillna(0).astype(float)
            #◎　システム備考
            kurikoshi_nyukin['備考_入繰'] = "入繰(" + kurikoshi_nyukin['金額'].astype(str) + ") " + kurikoshi_nyukin['ファイル名']
            kurikoshi_nyukin['備考_入ポ'] = "入ポ(" + kurikoshi_nyukin['ポイント'].astype(str) + ") " + kurikoshi_nyukin['ファイル名']
               
            
            # 項目名を加工
            kurikoshi_nyukin = kurikoshi_nyukin.rename(
                columns={'照合キー': nyukin_colomun, '金額': '品代金'})
            # 縦方向にマージ
            nyukin_oic = pd.concat([nyukin_oic, kurikoshi_nyukin], axis=0)
            # ★★
            # nyukin_oic.to_csv('./temp/nyukin_oic.csv', encoding='cp932')
        # ***** △ 繰越マージ（入金） △ *****
    
        # ***** ▽ AmazonPayマージ(入金) ▽ *****
        if len(nyukin_list_amazonPay) > 0:
            print(".... AmazonPayの入金がデータが存在します。")
            # ファイルを結合　→ リネーム →　件数表示用に加工
            amazonPay = pd.concat(nyukin_list_amazonPay, axis=0, sort=True)
            # ファイル出力
            amazonPay.to_csv(p_res + "\\" + p_tar_month +
                             '_AmazonPay.csv', encoding='UTF-8', index=False)
            # 文字項目から数値項目への変更
            if amazonPay['TransactionAmount'].dtype == "object":
                amazonPay['TransactionAmount'] = amazonPay['TransactionAmount'].str.replace(
                    ',', '').fillna(0).astype(float)
                
            #◎　システム備考
            amazonPay['備考_Ap'] = "入Ap(" + amazonPay['TransactionAmount'].astype(str) + ") " + amazonPay['ファイル名']
                
            # 項目名を加工
            amazonPay = amazonPay.rename(
                columns={'SellerOrderId': nyukin_colomun, 'TransactionAmount': '品代金'})
            # 縦方向にマージ
            nyukin_oic = pd.concat([nyukin_oic, amazonPay], axis=0)
            # ★★
            # nyukin_oic.to_csv('./temp/nyukin_oic.csv', encoding='cp932')
            # amazonPay.to_csv('./temp/amazonPay.csv', encoding='cp932')
        # ***** △ AmazonPayマージ(入金) △ *****
        # ◎　システム備考
        nyukin_oic['システム備考2'] = ""
        if '備考_入' in nyukin_oic.columns and '備考_入ポ' in nyukin_oic.columns and '備考_入繰' in nyukin_oic.columns and '備考_Ap' in nyukin_oic.columns:
            nyukin_oic['システム備考2'] = nyukin_oic['備考_入'].fillna('')  + nyukin_oic['備考_入ポ'].fillna('')  + nyukin_oic['備考_入繰'].fillna('') + nyukin_oic['備考_Ap'].fillna('') 
        
        if '備考_入' in nyukin_oic.columns and '備考_入ポ' not in nyukin_oic.columns and '備考_入繰' in nyukin_oic.columns and '備考_Ap' in nyukin_oic.columns:
            nyukin_oic['システム備考2'] = nyukin_oic['備考_入'].fillna('')  + nyukin_oic['備考_入繰'].fillna('') + nyukin_oic['備考_Ap'].fillna('') 

        if '備考_入' in nyukin_oic.columns and '備考_入ポ' in nyukin_oic.columns and '備考_入繰' not in nyukin_oic.columns and '備考_Ap' in nyukin_oic.columns:
            nyukin_oic['システム備考2'] = nyukin_oic['備考_入'].fillna('')  + nyukin_oic['備考_入ポ'].fillna('') + nyukin_oic['備考_Ap'].fillna('') 
        
        if '備考_入' in nyukin_oic.columns and '備考_入ポ' not in nyukin_oic.columns and '備考_入繰' not in nyukin_oic.columns and '備考_Ap' in nyukin_oic.columns:
            nyukin_oic['システム備考2'] = nyukin_oic['備考_入'].fillna('') + nyukin_oic['備考_Ap'].fillna('') 

        bikou = pd.DataFrame(nyukin_oic.groupby(nyukin_colomun)['システム備考2'].apply(lambda x: "%s" % ','.join(x)))
        ebisu = nyukin_oic[[nyukin_colomun, "品代金"]].rename(
            columns={nyukin_colomun: '【売上】受注番号', '品代金': '【売上】金額'}).groupby('【売上】受注番号').sum()
        ebisu = pd.concat([ebisu, bikou], axis=1)
        
        ebisu['【売上】受注番号2'] = ebisu.index
        ebisu_key = ebisu[['【売上】受注番号2']].rename(
            columns={'【売上】受注番号2': '照合キー'})
        ebisu_key_cnt = ebisu_key.value_counts()
        ebisu_key_cnt = ebisu_key.apply(pd.value_counts)
        ebisu_key_cnt = ebisu_key_cnt.rename(columns={'照合キー': '件数(入金)'})
        # Indexを列としてコピー
        ebisu_key_cnt['Key'] = ebisu_key_cnt.index

        ### デバッグの為の出力 ###
        # ★★
        #ebisu.to_csv('./temp/ebisu.csv', encoding='cp932')
        #ebisu_key.to_csv('./temp/ebisu_key.csv', encoding='cp932')
        #uriage_key2.to_csv('./temp/uriage_key2.csv', encoding='cp932')
        print(uriage_key2.dtypes)
        print(ebisu_key.dtypes)
        # Keyをマージして重複をのぞいて並び替え
        key = pd.concat([uriage_key2, ebisu_key],
                        axis=0).drop_duplicates(keep='first')
        #key.to_csv('./temp/key.csv', encoding='cp932')
        # 売上-入金をマージ
        if ebisu['【売上】受注番号2'].dtype == "int64":
            ebisu['【売上】受注番号2'] = ebisu['【売上】受注番号2'].astype(str)
        if ebisu['【売上】受注番号2'].dtype == "float":
            ebisu['【売上】受注番号2'] = ebisu['【売上】受注番号2'].astype(str)
        if ebisu['【売上】受注番号2'].dtype == "float64":
            ebisu['【売上】受注番号2'] = ebisu['【売上】受注番号2'].astype(str)

        if uriage_key_cnt2['Key'].dtype == "int64":
            uriage_key_cnt2['Key'] = uriage_key_cnt2['Key'].astype(str)
        if uriage_key_cnt2['Key'].dtype == "float":
            uriage_key_cnt2['Key'] = uriage_key_cnt2['Key'].astype(str)
        if uriage_key_cnt2['Key'].dtype == "float64":
            uriage_key_cnt2['Key'] = uriage_key_cnt2['Key'].astype(str)

        if ebisu_key_cnt['Key'].dtype == "int64":
            ebisu_key_cnt['Key'] = ebisu_key_cnt['Key'].astype(str)
        if ebisu_key_cnt['Key'].dtype == "float":
            ebisu_key_cnt['Key'] = ebisu_key_cnt['Key'].astype(str)
        if ebisu_key_cnt['Key'].dtype == "float64":
            ebisu_key_cnt['Key'] = ebisu_key_cnt['Key'].astype(str)

        # print("*** key ***")
        # print(key.dtypes)
        # print("*** uriage ***")
        # print(uriage.dtypes)
        # print("*** ebisu ***")
        # print(ebisu.dtypes)
        #####
        # key['照合キー'] = "A_" + key['照合キー']
        # uriage['発送伝票番号'] = "B_" + uriage['発送伝票番号']
        # ebisu['【売上】受注番号2'] = "C_" + ebisu['【売上】受注番号2']
        ### デバッグの為の出力 ###
        # ★★
        #key.to_csv('./temp/key.csv', encoding='cp932')
        #uriage.to_csv('./temp/uriage.csv', encoding='cp932')
        #ebisu.to_csv('./temp/ebisu.csv', encoding='cp932')

        key = pd.merge(key, uriage, left_on='照合キー',
                       right_on=uriage_column, how='left')
        key = pd.merge(key, ebisu, left_on='照合キー',
                       right_on='【売上】受注番号2', how='left')
        key = pd.merge(key, uriage_key_cnt2, left_on='照合キー',
                       right_on='Key', how='left')
        key = pd.merge(key, ebisu_key_cnt, left_on='照合キー',
                       right_on='Key', how='left')

        key['取引額'] = key['総合計']
        key['決済額'] = key['【売上】金額']
        key['繰越金額'] = 0.0
        key['差額'] = key['総合計'].fillna(0) - key['【売上】金額'].fillna(0)
        key['備考2'] = key['【売上】支払名']
        key['備考3'] = key['【売上】出荷確定日']
        key['照合結果'] = ""
        key['決済不能'] = ""
        key['顧客情報'] = ""
        key['情報2'] = ""
        key['判定情報'] = ""
        key['繰越区分'] = ""
        key = key[["照合キー", "件数(売上)", "取引額", "件数(入金)", "決済額", "差額",
                   "照合結果", "決済不能", "顧客情報", "情報2", "備考2", "備考3", "判定情報", "店舗コード","システム備考1","システム備考2"]]

        ########## ▼  突合結果書き込み処理  ▼ ##########
        d = datetime.datetime(int(tar_yyyy), int(tar_m), int(tar_d))
        print(".... 【代引き】の処理 .... OK ")
        print(".... 突合データ出力処理を開始します。")
        for index, row in key.iterrows():

            # 入金データ存在チェック
            if (row['件数(売上)'] == 1 and pd.isna(row['件数(入金)']) and row['備考3'] > d):
                key.at[index, '判定情報'] = "翌月データ"
                key.at[index, '照合結果'] = "キー不一致"
            elif (row['件数(売上)'] == 1 and pd.isna(row['件数(入金)'])):
                key.at[index, '判定情報'] = "入金データなし"
                key.at[index, '照合結果'] = "キー不一致"
            # 差額チェック
            elif (row['差額'] == 0):
                key.at[index, '判定情報'] = "差額なし"
                key.at[index, '照合結果'] = "OK"
            # elif(row['差額'] + row['ポイント'] == 0):
            #    key.at[index, '判定情報'] = "差額なし（ポイントあり）"
            #    key.at[index, '照合結果'] = "OK"
            # elif(row['差額'] + row['ポイント'] == 250 and row['備考2'].find('えびすクレジット後払い') != -1):
            #    key.at[index, '判定情報'] = "えびすクレジット後払い"
            #    key.at[index, '照合結果'] = "OK"
            # elif(str(row['備考2']).find('えびすクレジット後払い') != -1 and row['差額'] == 250):
            #    key.at[index, '判定情報'] = "えびすクレジット後払い"
            #    key.at[index, '照合結果'] = "OK"
            # elif(row['差額'] != 0 and row['ポイント'] != 0):
            #    key.at[index, '判定情報'] = "代引き＋ポイント"
            #    key.at[index, '照合結果'] = "OK"
            else:
                key.at[index, '照合結果'] = "金額相違"
            # 入金データ存在チェック
            if (row['件数(入金)'] == 1 and pd.isna(row['件数(売上)'])):
                key.at[index, '判定情報'] = "売上データなし"
                key.at[index, '照合結果'] = "キー不一致"
        ########## ▲ ▲ ##########
        ### デバッグの為の出力 ###
        # key.to_csv('./temp/key.csv', encoding='cp932')
        key.to_csv(p_res + "\\" + p_tar_month + '_OIC結果.csv',
                   encoding='cp932', index=False)
        print(".... 突合データ出力処理 .... OK ")
        # 翌月繰越データ出力
        print(".... 翌月繰越データの出力を開始します。 .... OK ")
        yokugetu = key.query('判定情報 == "翌月データ"').copy()
        yokugetu = yokugetu.rename(
            columns={'取引額': '金額', '備考3': '日付', '備考2': '備考'})
        yokugetu[['繰越区分']] = "入金"
        yokugetu[['ポイント']] = "0"
        yokugetu[['特記事項']] = "システム繰越"
        yokugetu = yokugetu[["繰越区分", "照合キー", "金額", "ポイント", "日付", "備考", "特記事項"]]
        yokugetu.to_csv(p_res + "\\" + p_tar_month +
                        '_OIC_翌月繰越.csv', encoding='cp932', index=False)

        # 金額相違データ出力
        print(".... 金額相違データの出力を開始します。 .... OK ")
        soui = key.query('照合結果 == "金額相違"').copy()
        soui[['繰越区分']] = "金額相違"
        soui.to_csv(p_res + "\\" + p_tar_month + '_OIC_金額相違.csv',
                    encoding='cp932', index=False)

        # キー不一致データ出力
        print(".... キー不一致データの出力を開始します。 .... OK ")
        uriage_nasi = key.query('照合結果 == "キー不一致" & 判定情報 == "売上データなし"').copy()
        uriage_nasi[['繰越区分']] = "売上データなし"
        uriage_nasi.to_csv(p_res + "\\" + p_tar_month +
                           '_OIC_売上データなし.csv', encoding='cp932', index=False)

        nyukin_nasi = key.query('照合結果 == "キー不一致" & 判定情報 == "入金データなし"').copy()
        nyukin_nasi[['繰越区分']] = "入金データなし"
        nyukin_nasi.to_csv(p_res + "\\" + p_tar_month +
                           '_OIC_入金データなし.csv', encoding='cp932', index=False)

        print(".... 翌月繰越データの出力 .... OK ")
        # 集計データ出力
        print(".... 集計データの出力を開始します。 .... OK ")
        f = open(p_res + "\\" + p_tar_month +
                 '_OIC集計結果.txt', 'w', encoding='cp932')

        ####################################################
        p_tmp = '*'
        try:
            p_tmp = key['件数(売上)'].sum()
        except:
            p_tmp = 0.0
        f.write('件数(売上):' + str(p_tmp) + '件\n')
        print('件数(売上):' + str(p_tmp) + '件')
        try:
            p_tmp = key['件数(入金)'].sum()
        except:
            p_tmp = 0.0
        f.write('件数(入金):' + str(p_tmp) + '件\n')
        print('件数(入金):' + str(p_tmp) + '件')
        try:
            p_tmp = key['件数(繰越)'].sum()
        except:
            p_tmp = 0.0
        f.write('件数(繰越):' + str(p_tmp) + '件\n')
        print('件数(繰越):' + str(p_tmp) + '件')
        f.write('****************************************\n')
        # 照合結果に記載されている分結果を書き込む
        p_hantei_list = key['照合結果'].unique().tolist()
        for keyword in p_hantei_list:
            p_amt = '*'
            p_cnt = '*'
            try:
                p_amt = key.query("照合結果 == '" + keyword + "'")['取引額'].sum()
                p_cnt = key.query("照合結果 == '" + keyword + "'")['取引額'].count()
            except:
                p_amt = 0.0
                p_cnt = 0.0

            f.write(keyword + '：' + str(p_cnt) + '件 ' + str(p_amt) + '円\n')
            print(keyword + '：' + str(p_cnt) + '件 ' + str(p_amt) + '円')
        f.write('****************************************\n')
        f.write("処理実行日時：" + datetime.datetime.now().strftime('%Y年%m月%d日 %H:%M:%S'))
        f.write('\n')
        f.write("突合データ（フォルダ）:" + p_tar)
        f.write('\n')
        f.write("結果出力先（フォルダ）:" + p_res)
        f.write('\n')
        f.write("出力先：" + p_res)
        f.write('\n')
        f.write("処理対象：" + p_tar_month)
        f.write('\n')
        f.write("出荷確定日 >= " + p_from + " < " + p_to)
        f.write('\n')
        f.write("繰越基準日：" + tar_yyyy + "年" + tar_m + "月" + tar_d + "日")
        f.write('\n')
        f.close()
        print(".... 集計データの出力 .... OK ")
    #################### ▲ OIC ▲ ####################
    #################### ▼ Bカート ▼ ####################

    if len(nyukin_bcart) > 0:
        print("  【Bカート】の処理を開始します。")
        # ◎　システム備考
        nyukin_bcart['備考_入'] = "入(" + nyukin_bcart['品代金'].astype(str) + ") " + nyukin_bcart['ファイル名']
        
        # ***** ▽ 繰越マージ(入金) ▽ *****
        if kurikoshi_nyukin.size != 0:
            # 文字項目から数値項目への変更
            if kurikoshi_nyukin['金額'].dtype == "object":
                kurikoshi_nyukin['金額'] = kurikoshi_nyukin['金額'].str.replace(
                    ',', '').fillna(0).astype(float)
            if kurikoshi_nyukin['ポイント'].dtype == "object":
                kurikoshi_nyukin['ポイント'] = kurikoshi_nyukin['ポイント'].str.replace(
                    ',', '').fillna(0).astype(float)
            # ◎　システム備考
            kurikoshi_nyukin['備考_入繰'] = "入繰(" + kurikoshi_nyukin['金額'].astype(str) + ") " + kurikoshi_nyukin['ファイル名']
            kurikoshi_nyukin['備考_入ポ'] = "入ポ(" + kurikoshi_nyukin['ポイント'].astype(str) + ") " + kurikoshi_nyukin['ファイル名']
            
            # 項目名を加工
            kurikoshi_nyukin = kurikoshi_nyukin.rename(
                columns={'照合キー': nyukin_colomun, '金額': '品代金'})
            # 縦方向にマージ
            nyukin_bcart = pd.concat([nyukin_bcart, kurikoshi_nyukin], axis=0)
            #nyukin_bcart.to_csv('./temp/nyukin_bcart.csv', encoding='cp932')
        # ***** △ 繰越マージ（入金） △ *****
        # ◎　システム備考
        nyukin_bcart['システム備考2'] = ""
        if '備考_入' in nyukin_bcart.columns and '備考_入ポ' in nyukin_bcart.columns and '備考_入繰' in nyukin_bcart.columns:
            nyukin_bcart['システム備考2'] = nyukin_bcart['備考_入'].fillna('')  + nyukin_bcart['備考_入ポ'].fillna('')  + nyukin_bcart['備考_入繰'].fillna('') 
        
        if '備考_入' in nyukin_bcart.columns and '備考_入ポ' not in nyukin_bcart.columns and '備考_入繰' in nyukin_bcart.columns:
            nyukin_bcart['システム備考2'] = nyukin_bcart['備考_入'].fillna('')  + nyukin_bcart['備考_入繰'].fillna('') 

        if '備考_入' in nyukin_bcart.columns and '備考_入ポ' in nyukin_bcart.columns and '備考_入繰' not in nyukin_bcart.columns:
            nyukin_bcart['システム備考2'] = nyukin_bcart['備考_入'].fillna('')  + nyukin_bcart['備考_入ポ'].fillna('') 
        
        if '備考_入' in nyukin_bcart.columns and '備考_入ポ' not in nyukin_bcart.columns and '備考_入繰' not in nyukin_bcart.columns:
            nyukin_bcart['システム備考2'] = nyukin_bcart['備考_入'].fillna('') 
        ### デバッグの為の出力 ###
        # ★★
        # nyukin_ebisu_daibiki.to_csv('./temp/nyukin_ebisu_daibiki.csv', encoding='cp932')
        bikou = pd.DataFrame(nyukin_bcart.groupby(nyukin_colomun)['システム備考2'].apply(lambda x: "%s" % ','.join(x)))
        ebisu = nyukin_bcart[[nyukin_colomun, "品代金"]].rename(
            columns={nyukin_colomun: '【売上】受注番号', '品代金': '【売上】金額'}).groupby('【売上】受注番号').sum()
        ebisu = pd.concat([ebisu, bikou], axis=1)
        ebisu['【売上】受注番号2'] = ebisu.index
        ebisu_key = ebisu[['【売上】受注番号2']].rename(
            columns={'【売上】受注番号2': '照合キー'})
        ebisu_key_cnt = ebisu_key.value_counts()
        ebisu_key_cnt = ebisu_key.apply(pd.value_counts)
        ebisu_key_cnt = ebisu_key_cnt.rename(columns={'照合キー': '件数(入金)'})
        # Indexを列としてコピー
        ebisu_key_cnt['Key'] = ebisu_key_cnt.index

        ### デバッグの為の出力 ###
        # ★★
        # ebisu.to_csv('./temp/daibiki.csv', encoding='cp932')
        # ebisu_key.to_csv('./temp/daibiki_key.csv', encoding='cp932')
        # ebisu_key_cnt.to_csv('./temp/daibiki_key_cnt.csv', encoding='cp932')
        # print(uriage_key2.dtypes)
        # print(ebisu_key.dtypes)
        # Keyをマージして重複をのぞいて並び替え
        key = pd.concat([uriage_key2, ebisu_key],
                        axis=0).drop_duplicates(keep='first')
        # 売上-入金をマージ

        # print("*** uriage ***")
        # print(uriage.dtypes)
        # print("*** ebisu ***")
        # print(ebisu.dtypes)
        if ebisu['【売上】受注番号2'].dtype == "int64":
            ebisu['【売上】受注番号2'] = ebisu['【売上】受注番号2'].astype(str)
        if ebisu['【売上】受注番号2'].dtype == "float":
            ebisu['【売上】受注番号2'] = ebisu['【売上】受注番号2'].astype(str)

        if uriage_key_cnt2['Key'].dtype == "int64":
            uriage_key_cnt2['Key'] = uriage_key_cnt2['Key'].astype(str)
        if uriage_key_cnt2['Key'].dtype == "float":
            uriage_key_cnt2['Key'] = uriage_key_cnt2['Key'].astype(str)

        if ebisu_key_cnt['Key'].dtype == "int64":
            ebisu_key_cnt['Key'] = ebisu_key_cnt['Key'].astype(str)
        if ebisu_key_cnt['Key'].dtype == "float":
            ebisu_key_cnt['Key'] = ebisu_key_cnt['Key'].astype(str)

        key = pd.merge(key, uriage, left_on='照合キー',
                       right_on=uriage_column, how='left')
        key = pd.merge(key, ebisu, left_on='照合キー',
                       right_on='【売上】受注番号2', how='left')
        key = pd.merge(key, uriage_key_cnt2, left_on='照合キー',
                       right_on='Key', how='left')
        key = pd.merge(key, ebisu_key_cnt, left_on='照合キー',
                       right_on='Key', how='left')

        key['取引額'] = key['総合計']
        key['決済額'] = key['【売上】金額']
        key['繰越金額'] = 0.0
        key['差額'] = key['総合計'].fillna(0) - key['【売上】金額'].fillna(0)
        key['備考2'] = key['【売上】支払名']
        key['備考3'] = key['【売上】出荷確定日']
        key['照合結果'] = ""
        key['決済不能'] = ""
        key['顧客情報'] = ""
        key['情報2'] = ""
        key['判定情報'] = ""
        key['繰越区分'] = ""
        key = key[["照合キー", "件数(売上)", "取引額", "件数(入金)", "決済額", "差額",
                   "照合結果", "決済不能", "顧客情報", "情報2", "備考2", "備考3", "判定情報", "店舗コード","システム備考1","システム備考2"]]

        ########## ▼  突合結果書き込み処理  ▼ ##########
        d = datetime.datetime(int(tar_yyyy), int(tar_m), int(tar_d))
        print(".... 【代引き】の処理 .... OK ")
        print(".... 突合データ出力処理を開始します。")
        for index, row in key.iterrows():

            # 入金データ存在チェック
            if (row['件数(売上)'] == 1 and pd.isna(row['件数(入金)']) and row['備考3'] > d):
                key.at[index, '判定情報'] = "翌月データ"
                key.at[index, '照合結果'] = "キー不一致"
            elif (row['件数(売上)'] == 1 and pd.isna(row['件数(入金)'])):
                key.at[index, '判定情報'] = "入金データなし"
                key.at[index, '照合結果'] = "キー不一致"
            # 差額チェック
            elif (row['差額'] == 0):
                key.at[index, '判定情報'] = "差額なし"
                key.at[index, '照合結果'] = "OK"
            # elif(row['差額'] + row['ポイント'] == 0):
            #    key.at[index, '判定情報'] = "差額なし（ポイントあり）"
            #    key.at[index, '照合結果'] = "OK"
            # elif(row['差額'] + row['ポイント'] == 250 and row['備考2'].find('えびすクレジット後払い') != -1):
            #    key.at[index, '判定情報'] = "えびすクレジット後払い"
            #    key.at[index, '照合結果'] = "OK"
            # elif(str(row['備考2']).find('えびすクレジット後払い') != -1 and row['差額'] == 250):
            #    key.at[index, '判定情報'] = "えびすクレジット後払い"
            #    key.at[index, '照合結果'] = "OK"
            # elif(row['差額'] != 0 and row['ポイント'] != 0):
            #    key.at[index, '判定情報'] = "代引き＋ポイント"
            #    key.at[index, '照合結果'] = "OK"
            else:
                key.at[index, '照合結果'] = "金額相違"
            # 入金データ存在チェック
            if (row['件数(入金)'] == 1 and pd.isna(row['件数(売上)'])):
                key.at[index, '判定情報'] = "売上データなし"
                key.at[index, '照合結果'] = "キー不一致"
        ########## ▲ ▲ ##########
        ### デバッグの為の出力 ###
        # key.to_csv('./temp/key.csv', encoding='cp932')
        key.to_csv(p_res + "\\" + p_tar_month + '_Bカート結果.csv',
                   encoding='cp932', index=False)
        print(".... 突合データ出力処理 .... OK ")
        # 翌月繰越データ出力
        print(".... 翌月繰越データの出力を開始します。 .... OK ")
        yokugetu = key.query('判定情報 == "翌月データ"').copy()
        yokugetu = yokugetu.rename(
            columns={'取引額': '金額', '備考3': '日付', '備考2': '備考'})
        yokugetu[['繰越区分']] = "入金"
        yokugetu[['ポイント']] = "0"
        yokugetu[['特記事項']] = "システム繰越"
        yokugetu = yokugetu[["繰越区分", "照合キー", "金額", "ポイント", "日付", "備考", "特記事項"]]
        yokugetu.to_csv(p_res + "\\" + p_tar_month +
                        '_Bカート_翌月繰越.csv', encoding='cp932', index=False)

        # 金額相違データ出力
        print(".... 金額相違データの出力を開始します。 .... OK ")
        soui = key.query('照合結果 == "金額相違"').copy()
        soui[['繰越区分']] = "金額相違"
        soui.to_csv(p_res + "\\" + p_tar_month + '_Bカート_金額相違.csv',
                    encoding='cp932', index=False)

        # キー不一致データ出力
        print(".... キー不一致データの出力を開始します。 .... OK ")
        uriage_nasi = key.query('照合結果 == "キー不一致" & 判定情報 == "売上データなし"').copy()
        uriage_nasi[['繰越区分']] = "売上データなし"
        uriage_nasi.to_csv(p_res + "\\" + p_tar_month +
                           '_Bカート_売上データなし.csv', encoding='cp932', index=False)

        nyukin_nasi = key.query('照合結果 == "キー不一致" & 判定情報 == "入金データなし"').copy()
        nyukin_nasi[['繰越区分']] = "入金データなし"
        nyukin_nasi.to_csv(p_res + "\\" + p_tar_month +
                           '_Bカート_入金データなし.csv', encoding='cp932', index=False)

        print(".... 翌月繰越データの出力 .... OK ")
        # 集計データ出力
        print(".... 集計データの出力を開始します。 .... OK ")
        f = open(p_res + "\\" + p_tar_month +
                 '_Bカート集計結果.txt', 'w', encoding='cp932')

        ####################################################
        p_tmp = '*'
        try:
            p_tmp = key['件数(売上)'].sum()
        except:
            p_tmp = 0.0
        f.write('件数(売上):' + str(p_tmp) + '件\n')
        print('件数(売上):' + str(p_tmp) + '件')
        try:
            p_tmp = key['件数(入金)'].sum()
        except:
            p_tmp = 0.0
        f.write('件数(入金):' + str(p_tmp) + '件\n')
        print('件数(入金):' + str(p_tmp) + '件')
        try:
            p_tmp = key['件数(繰越)'].sum()
        except:
            p_tmp = 0.0
        f.write('件数(繰越):' + str(p_tmp) + '件\n')
        print('件数(繰越):' + str(p_tmp) + '件')
        f.write('****************************************\n')
        # 照合結果に記載されている分結果を書き込む
        p_hantei_list = key['照合結果'].unique().tolist()
        for keyword in p_hantei_list:
            p_amt = '*'
            p_cnt = '*'
            try:
                p_amt = key.query("照合結果 == '" + keyword + "'")['取引額'].sum()
                p_cnt = key.query("照合結果 == '" + keyword + "'")['取引額'].count()
            except:
                p_amt = 0.0
                p_cnt = 0.0

            f.write(keyword + '：' + str(p_cnt) + '件 ' + str(p_amt) + '円\n')
            print(keyword + '：' + str(p_cnt) + '件 ' + str(p_amt) + '円')
        f.write('****************************************\n')
        f.write("処理実行日時：" + datetime.datetime.now().strftime('%Y年%m月%d日 %H:%M:%S'))
        f.write('\n')
        f.write("突合データ（フォルダ）:" + p_tar)
        f.write('\n')
        f.write("結果出力先（フォルダ）:" + p_res)
        f.write('\n')
        f.write("出力先：" + p_res)
        f.write('\n')
        f.write("処理対象：" + p_tar_month)
        f.write('\n')
        f.write("出荷確定日 >= " + p_from + " < " + p_to)
        f.write('\n')
        f.write("繰越基準日：" + tar_yyyy + "年" + tar_m + "月" + tar_d + "日")
        f.write('\n')
        f.close()
        print(".... 集計データの出力 .... OK ")
    #################### ▲ Bカート ▲ ####################
    #################### ▼　Amazon ▼  ####################
    if nyukin_list_amazon:
        print("  【Amazon】の処理を開始します。")
        # ファイルを結合　→ リネーム →　件数表示用に加工
        amazon = pd.concat(nyukin_list_amazon, axis=0, sort=True)
        #amazon.to_csv('./temp/amazon.csv', encoding='utf-8')
        # ***** ▽ 繰越マージ(入金) ▽ *****
        if kurikoshi_nyukin.size != 0:
            # 文字項目から数値項目への変更
            if kurikoshi_nyukin['金額'].dtype == "object":
                kurikoshi_nyukin['金額'] = kurikoshi_nyukin['金額'].str.replace(
                    ',', '').fillna(0).astype(float)
            if kurikoshi_nyukin['ポイント'].dtype == "object":
                kurikoshi_nyukin['ポイント'] = kurikoshi_nyukin['ポイント'].str.replace(
                    ',', '').fillna(0).astype(float)
            # ◎　システム備考
            kurikoshi_nyukin['備考_入繰'] = "入繰(" + kurikoshi_nyukin['金額'].astype(str) + ") " + kurikoshi_nyukin['ファイル名']
            kurikoshi_nyukin['備考_入ポ'] = "入ポ(" + kurikoshi_nyukin['ポイント'].astype(str) + ") " + kurikoshi_nyukin['ファイル名']
            
            # 項目名を加工
            kurikoshi_nyukin = kurikoshi_nyukin.rename(
                columns={'照合キー': nyukin_colomun, '金額': 'amount'})
            kurikoshi_nyukin[['transaction-type']] = "Order"
            kurikoshi_nyukin[['amount-description']] = "Principal"
            kurikoshi_nyukin[['amount-type']] = "ItemPrice"
            # 縦方向にマージ
            amazon = pd.concat([amazon, kurikoshi_nyukin], axis=0)
            #amazon.to_csv('./temp/amazon.csv', encoding='cp932')
        # ***** △ 繰越マージ（入金） △ *****

        #★amazon.to_csv('./temp/amazon.csv', encoding='utf-8')
        #df.pivot(index='order-id', columns='amount-description', values='amount').to_csv('./temp/amazon_pivot.csv', encoding='utf-8')
        #amazon.unstack(level=0).to_csv('./temp/amazon0.csv', encoding='utf-8')
        #amazon.unstack(level=1).to_csv('./temp/amazon1.csv', encoding='utf-8')
        #amazon.unstack(level=12).to_csv('./temp/amazon11.csv', encoding='utf-8')
        # 必要な項目だけにする
        amazon_new = amazon.query('`transaction-type` == "Order"')
        amazon_new = amazon_new[['order-id','amount-description','amount-type','amount']]
        # 型変換
        amazon_new['amount'] = amazon_new['amount'].str.replace(',', '').fillna(0).astype(float)
        # Group Byする
        amazon_new = amazon_new.groupby(['order-id','amount-description','amount-type'])[['amount']].sum()
        #★amazon_new.to_csv('./temp/amazon_new.csv', encoding='utf-8')
        # 横持に
        #amazon_yoko = amazon_new.pivot_table(values=['amount'], index=['order-id'], columns=['amount-description','amount-type'], aggfunc='sum')
        #amazon_yoko.to_csv('./temp/amazon_yoko.csv', encoding='utf-8')
        amazon_yoko = amazon_new.unstack(level=[1, 2])
        # あたしい項目名に
        title = []
        for item in amazon_yoko.columns.values.tolist():
            title.append(item[2]+"["+item[1]+"]")
        amazon_yoko = amazon_yoko.set_axis(title, axis='columns')
        
        amazon_yoko['【売上】金額'] = 0.0
        amazon_yoko['システム備考2'] = ""
        #★amazon_yoko.to_csv('./temp/amazon_yoko.csv', encoding='utf-8')
        
        ######################
        # 必要項目をたしこむ
        ######################
        def SetValue(row):
            amt = 0.0
            biko = ""
            for colomun in taisyou_amazon_list:                
                if row[colomun] != "":
                    amt += row[colomun] 
                    biko += colomun + "(" + str(row[colomun]) + ") "

            row["【売上】金額"] = amt
            row["システム備考2"] = biko
            return row
        amazon_yoko = amazon_yoko.fillna('')
        amazon_yoko = amazon_yoko.apply(SetValue, axis=1)
        amazon_yoko.to_csv(
                    p_res + "\\" + p_tar_month + '_Amazon集計用ファイル２_' + f + '.csv', encoding='cp932')
        
        #★amazon_yoko.to_csv('./temp/amazon_yoko.csv', encoding='cp932')
        # インデックスをふりなおしてコピーしておく
        amazon = amazon_yoko.reset_index()
        amazon["order-id2"] = amazon["order-id"]

        #amazon.to_csv('./temp/amazon.csv', encoding='cp932')
        
        #amazon_yoko["order-id2"] = amazon_yoko["order-id"]
        #amazon_yoko.to_csv('./temp/amazon_yoko.csv', encoding='cp932')
        
        amazon_key = amazon[['order-id2']].rename(
            columns={'order-id2': '照合キー'})
        amazon_key_cnt = amazon_key.value_counts()
        amazon_key_cnt = amazon_key.apply(pd.value_counts)
        amazon_key_cnt = amazon_key_cnt.rename(columns={'照合キー': '件数(入金)'})
        # Indexを列としてコピー
        amazon_key_cnt['Key'] = amazon_key_cnt.index

        # Keyをマージして重複をのぞいて並び替え
        key = pd.concat([uriage_key, amazon_key], axis=0).sort_values(
            '照合キー').drop_duplicates(keep='first')
        # 売上-入金をマージ
        # データ
        if uriage['受注番号'].dtype == "int64":
            uriage['受注番号'] = uriage['受注番号'].astype(str)
        key = pd.merge(key, uriage, left_on='照合キー',
                       right_on='受注番号', how='left')

        if amazon['order-id2'].dtype == "int64":
            amazon['order-id2'] = amazon['order-id2'].astype(str)
        key = pd.merge(key, amazon, left_on='照合キー',
                       right_on='order-id2', how='left')
        # 件数
        if uriage_key_cnt['Key'].dtype == "int64":
            uriage_key_cnt['Key'] = uriage_key_cnt['Key'].astype(str)
        key = pd.merge(key, uriage_key_cnt, left_on='照合キー',
                       right_on='Key', how='left')

        if amazon_key_cnt['Key'].dtype == "int64":
            amazon_key_cnt['Key'] = amazon_key_cnt['Key'].astype(str)
        key = pd.merge(key, amazon_key_cnt, left_on='照合キー',
                       right_on='Key', how='left')

        key['取引額'] = key['総合計']
        key['決済額'] = key['【売上】金額']
        key['繰越金額'] = 0.0

        if key['総合計'].dtype == "object":
            key['総合計'] = key['総合計'].str.replace(',', '').astype(float)
        if key['総合計'].dtype == "int64":
            key['総合計'] = key['総合計'].astype(float)

        if key['【売上】金額'].dtype == "object":
            key['【売上】金額'] = key['【売上】金額'].str.replace(',', '').astype(float)
        if key['【売上】金額'].dtype == "int64":
            key['【売上】金額'] = key['【売上】金額'].astype(float)

        key['差額'] = key['総合計'].fillna(0) - key['【売上】金額'].fillna(0)
        key['備考2'] = key['【売上】支払名']
        key['備考3'] = key['【売上】出荷確定日']
        key['照合結果'] = ""
        key['決済不能'] = ""
        key['顧客情報'] = ""
        key['情報2'] = ""
        key['判定情報'] = ""
        key['繰越区分'] = ""
        # key['件数(繰越)'] = 0
        # key['【繰越】取引額'] = 0.0
        # key['【繰越】決済額'] = 0.0
        # key['【繰越】差額'] = 0.0
        # key['【繰越】出荷確定日'] = ""
        # key['【繰越】支払名'] = ""
        # key['【繰越】判定情報'] = ""

        # 結果出力用に成形
        key = key[["照合キー", "件数(売上)", "取引額", "件数(入金)", "決済額", "差額",
                   "照合結果", "決済不能", "顧客情報", "情報2", "備考2", "備考3", "判定情報", "店舗コード","システム備考1","システム備考2"]]

        ########## ▼  突合結果書き込み処理  ▼ ##########
        d = datetime.datetime(int(tar_yyyy), int(tar_m), int(tar_d))
        print(".... 【Amazon】の処理 .... OK ")
        print(".... 突合データ出力処理を開始します。")
        for index, row in key.iterrows():

            # 入金データ存在チェック
            if (row['件数(売上)'] == 1 and pd.isna(row['件数(入金)']) and row['備考3'] > d):
                key.at[index, '判定情報'] = "翌月データ"
                key.at[index, '照合結果'] = "キー不一致"
            elif (row['件数(売上)'] == 1 and pd.isna(row['件数(入金)'])):
                key.at[index, '判定情報'] = "入金データなし"
                key.at[index, '照合結果'] = "キー不一致"
            # 差額チェック
            elif (row['差額'] == 0):
                key.at[index, '判定情報'] = "差額なし"
                key.at[index, '照合結果'] = "OK"
            else:
                key.at[index, '照合結果'] = "金額相違"
            # 入金データ存在チェック
            if (row['件数(入金)'] == 1 and pd.isna(row['件数(売上)'])):
                key.at[index, '判定情報'] = "売上データなし"
                key.at[index, '照合結果'] = "キー不一致"
        ########## ▲ ▲ ##########
        ### デバッグの為の出力 ###
        # key.to_csv('./temp/key.csv', encoding='cp932')
        key.to_csv(p_res + "\\" + p_tar_month + '_Amazon結果.csv',
                   encoding='cp932', index=False)
        print(".... 突合データ出力処理 .... OK ")
        # 翌月繰越データ出力
        print(".... 翌月繰越データの出力を開始します。 .... OK ")
        yokugetu = key.query('判定情報 == "翌月データ"').copy()
        yokugetu = yokugetu.rename(
            columns={'取引額': '金額', '備考3': '日付', '備考2': '備考'})
        yokugetu[['繰越区分']] = "入金"
        yokugetu[['ポイント']] = "0"
        yokugetu[['特記事項']] = "システム繰越"
        yokugetu = yokugetu[["繰越区分", "照合キー", "金額", "ポイント", "日付", "備考", "特記事項"]]
        yokugetu.to_csv(p_res + "\\" + p_tar_month +
                        '_Amazon_翌月繰越.csv', encoding='cp932', index=False)

        # 金額相違データ出力
        print(".... 金額相違データの出力を開始します。 .... OK ")
        soui = key.query('照合結果 == "金額相違"').copy()
        soui[['繰越区分']] = "金額相違"
        soui.to_csv(p_res + "\\" + p_tar_month + '_Amazon_金額相違.csv',
                    encoding='cp932', index=False)

        # キー不一致データ出力
        print(".... キー不一致データの出力を開始します。 .... OK ")
        uriage_nasi = key.query('照合結果 == "キー不一致" & 判定情報 == "売上データなし"').copy()
        uriage_nasi[['繰越区分']] = "売上データなし"
        uriage_nasi.to_csv(p_res + "\\" + p_tar_month +
                           '_Amazon_売上データなし.csv', encoding='cp932', index=False)

        nyukin_nasi = key.query('照合結果 == "キー不一致" & 判定情報 == "入金データなし"').copy()
        nyukin_nasi[['繰越区分']] = "入金データなし"
        nyukin_nasi.to_csv(p_res + "\\" + p_tar_month +
                           '_Amazon_入金データなし.csv', encoding='cp932', index=False)

        print(".... 翌月繰越データの出力 .... OK ")

        #################################################################################
        # 集計データ出力
        print(".... 集計データの出力を開始します。 .... OK ")
        f = open(p_res + "\\" + p_tar_month +
                 '_Amazon集計結果.txt', 'w', encoding='cp932')

        ####################################################
        p_tmp = '*'
        try:
            p_tmp = key['件数(売上)'].sum()
        except:
            p_tmp = 0.0
        f.write('件数(売上):' + str(p_tmp) + '件\n')
        print('件数(売上):' + str(p_tmp) + '件')
        try:
            p_tmp = key['件数(入金)'].sum()
        except:
            p_tmp = 0.0
        f.write('件数(入金):' + str(p_tmp) + '件\n')
        print('件数(入金):' + str(p_tmp) + '件')
        try:
            p_tmp = key['件数(繰越)'].sum()
        except:
            p_tmp = 0.0
        f.write('件数(繰越):' + str(p_tmp) + '件\n')
        print('件数(繰越):' + str(p_tmp) + '件')
        f.write('****************************************\n')
        # 照合結果に記載されている分結果を書き込む
        p_hantei_list = key['照合結果'].unique().tolist()
        for keyword in p_hantei_list:
            p_amt = '*'
            p_cnt = '*'
            try:
                p_amt = key.query("照合結果 == '" + keyword + "'")['取引額'].sum()
                p_cnt = key.query("照合結果 == '" + keyword + "'")['取引額'].count()
            except:
                p_amt = 0.0
                p_cnt = 0.0

            f.write(keyword + '：' + str(p_cnt) + '件 ' + str(p_amt) + '円\n')
            print(keyword + '：' + str(p_cnt) + '件 ' + str(p_amt) + '円')
        f.write('****************************************\n')
        f.write("処理実行日時：" + datetime.datetime.now().strftime('%Y年%m月%d日 %H:%M:%S'))
        f.write('\n')
        f.write("突合データ（フォルダ）:" + p_tar)
        f.write('\n')
        f.write("結果出力先（フォルダ）:" + p_res)
        f.write('\n')
        f.write("出力先：" + p_res)
        f.write('\n')
        f.write("処理対象：" + p_tar_month)
        f.write('\n')
        f.write("出荷確定日 >= " + p_from + " < " + p_to)
        f.write('\n')
        f.write("繰越基準日：" + tar_yyyy + "年" + tar_m + "月" + tar_d + "日")
        f.write('\n')
        f.close()
        print(".... 集計データの出力 .... OK ")
        #################### ▲ メインの処理 ▲ ####################
    #################### ▲　Amazon ▲  ####################
    #################### ▼ 楽天 ▼ ####################
    if nyukin_list_rakuten_pay:
        print("  【楽天】の処理を開始します。")
        # ファイルを結合　→ リネーム →　件数表示用に加工
        rakuten = pd.concat(nyukin_list_rakuten_pay, axis=0, sort=True)
        
        if rakuten['楽天ﾍﾟｲ_決済金等'].dtype == "object":
            rakuten['楽天ﾍﾟｲ_決済金等'] = rakuten['楽天ﾍﾟｲ_決済金等'].str.replace(
                ',', '').fillna(0).astype(float)
        # ◎　システム備考
        rakuten['備考_入'] = "入(" + rakuten['楽天ﾍﾟｲ_決済金等'].astype(str) + ") " + rakuten['ファイル名']
        # print("*** rakuten ***")
        # print(rakuten.dtypes)
        # print("*** uriage ***")
        # print(uriage.dtypes)
        # ***** ▽ 繰越マージ(入金) ▽ *****
        if kurikoshi_nyukin.size != 0:
            # 文字項目から数値項目への変更
            if kurikoshi_nyukin['金額'].dtype == "object":
                kurikoshi_nyukin['金額'] = kurikoshi_nyukin['金額'].str.replace(
                    ',', '').fillna(0).astype(float)
            if kurikoshi_nyukin['ポイント'].dtype == "object":
                kurikoshi_nyukin['ポイント'] = kurikoshi_nyukin['ポイント'].str.replace(
                    ',', '').fillna(0).astype(float)
            # ◎　システム備考
            kurikoshi_nyukin['備考_入繰'] = "入繰(" + kurikoshi_nyukin['金額'].astype(str) + ") " + kurikoshi_nyukin['ファイル名']
            kurikoshi_nyukin['備考_入ポ'] = "入ポ(" + kurikoshi_nyukin['ポイント'].astype(str) + ") " + kurikoshi_nyukin['ファイル名']
            
            # 項目名を加工
            kurikoshi_nyukin = kurikoshi_nyukin.rename(
                columns={'照合キー': nyukin_colomun, '金額': '楽天ﾍﾟｲ_決済金等'})
            # kurikoshi_nyukin[['transaction-type']] = "Order"
            # kurikoshi_nyukin[['amount-description']] = "Principal"
            # kurikoshi_nyukin[['amount-type']] = "ItemPrice"
            # 縦方向にマージ
            # print("*** kurikoshi_nyukin ***")
            # print(kurikoshi_nyukin.dtypes)
            rakuten = pd.concat([rakuten, kurikoshi_nyukin], axis=0)
        # ***** △ 繰越マージ（入金） △ *****
        # ◎　システム備考
        rakuten['システム備考2'] = ""
        if '備考_入' in rakuten.columns and '備考_入ポ' in rakuten.columns and '備考_入繰' in rakuten.columns:
            rakuten['システム備考2'] = rakuten['備考_入'].fillna('')  + rakuten['備考_入ポ'].fillna('')  + rakuten['備考_入繰'].fillna('') 
        
        if '備考_入' in rakuten.columns and '備考_入ポ' not in rakuten.columns and '備考_入繰' in rakuten.columns:
            rakuten['システム備考2'] = rakuten['備考_入'].fillna('')  + rakuten['備考_入繰'].fillna('') 

        if '備考_入' in rakuten.columns and '備考_入ポ' in rakuten.columns and '備考_入繰' not in rakuten.columns:
            rakuten['システム備考2'] = rakuten['備考_入'].fillna('')  + rakuten['備考_入ポ'].fillna('') 
        
        if '備考_入' in rakuten.columns and '備考_入ポ' not in rakuten.columns and '備考_入繰' not in rakuten.columns:
            rakuten['システム備考2'] = rakuten['備考_入'].fillna('') 
            
        bikou = pd.DataFrame(rakuten.groupby(nyukin_colomun)['システム備考2'].apply(lambda x: "%s" % ','.join(x)))

        rakuten = rakuten[["受注番号", "楽天ﾍﾟｲ_決済金等"]].rename(
            columns={'受注番号': '【売上】受注番号', '楽天ﾍﾟｲ_決済金等': '【売上】金額'}).groupby('【売上】受注番号').sum()
        
        rakuten = pd.concat([rakuten, bikou], axis=1)
        
        rakuten['【売上】受注番号2'] = rakuten.index

        rakuten_key = rakuten[['【売上】受注番号2']].rename(
            columns={'【売上】受注番号2': '照合キー'})
        rakuten_key_cnt = rakuten_key.value_counts()
        rakuten_key_cnt = rakuten_key.apply(pd.value_counts)
        rakuten_key_cnt = rakuten_key_cnt.rename(columns={'照合キー': '件数(入金)'})
        # Indexを列としてコピー
        rakuten_key_cnt['Key'] = rakuten_key_cnt.index

        # Keyをマージして重複をのぞいて並び替え
        key = pd.concat([uriage_key, rakuten_key], axis=0).sort_values(
            '照合キー').drop_duplicates(keep='first')
        # 売上-入金をマージ
        # データ
        if uriage['受注番号'].dtype == "int64":
            uriage['受注番号'] = uriage['受注番号'].astype(str)
        if uriage['受注番号'].dtype == "float":
            uriage['受注番号'] = uriage['受注番号'].astype(str)

        key = pd.merge(key, uriage, left_on='照合キー',
                       right_on='受注番号', how='left')

        if rakuten['【売上】受注番号2'].dtype == "int64":
            rakuten['【売上】受注番号2'] = rakuten['【売上】受注番号2'].astype(str)

        if rakuten['【売上】受注番号2'].dtype == "float":
            rakuten['【売上】受注番号2'] = rakuten['【売上】受注番号2'].astype(str)

        key = pd.merge(key, rakuten, left_on='照合キー',
                       right_on='【売上】受注番号2', how='left')
        # 件数
        if uriage_key_cnt['Key'].dtype == "int64":
            uriage_key_cnt['Key'] = uriage_key_cnt['Key'].astype(str)
        if uriage_key_cnt['Key'].dtype == "float":
            uriage_key_cnt['Key'] = uriage_key_cnt['Key'].astype(str)

        key = pd.merge(key, uriage_key_cnt, left_on='照合キー',
                       right_on='Key', how='left')

        if rakuten_key_cnt['Key'].dtype == "int64":
            rakuten_key_cnt['Key'] = rakuten_key_cnt['Key'].astype(str)

        if rakuten_key_cnt['Key'].dtype == "float":
            rakuten_key_cnt['Key'] = rakuten_key_cnt['Key'].astype(str)

        key = pd.merge(key, rakuten_key_cnt, left_on='照合キー',
                       right_on='Key', how='left')

        key['取引額'] = key['総合計']
        key['決済額'] = key['【売上】金額']
        key['繰越金額'] = 0.0
        key['差額'] = key['総合計'].fillna(0) - key['【売上】金額'].fillna(0)
        key['備考2'] = key['【売上】支払名']
        key['備考3'] = key['【売上】出荷確定日']
        key['照合結果'] = ""
        key['決済不能'] = ""
        key['顧客情報'] = ""
        key['情報2'] = ""
        key['判定情報'] = ""
        key['繰越区分'] = ""

        ### デバッグの為の出力 ###
        # key.to_csv('./temp/key.csv', encoding='cp932')

        # 結果出力用に成形
        key = key[["照合キー", "件数(売上)", "取引額", "件数(入金)", "決済額", "差額", "照合結果", "決済不能", "顧客情報", "情報2", "備考2", "備考3",
                   "ポイント", "判定情報", "店舗コード","システム備考1","システム備考2"]]

        # print(key.dtypes)

        ########## ▼  突合結果書き込み処理  ▼ ##########
        d = datetime.datetime(int(tar_yyyy), int(tar_m), int(tar_d))
        print(".... 【楽天】の処理 .... OK ")
        print(".... 突合データ出力処理を開始します。")
        for index, row in key.iterrows():

            # 入金データ存在チェック
            if (row['件数(売上)'] == 1 and pd.isna(row['件数(入金)']) and row['備考3'] > d):
                key.at[index, '判定情報'] = "翌月データ"
                key.at[index, '照合結果'] = "キー不一致"
            # 差額チェック
            elif (row['差額'] + row['ポイント'] == 0):
                key.at[index, '判定情報'] = "差額なし（ポイントあり）"
                key.at[index, '照合結果'] = "OK"
            elif (row['差額'] + row['ポイント'] == -250 and row['備考2'].find('楽天後払い') != -1):
                key.at[index, '判定情報'] = "楽天後払い"
                key.at[index, '照合結果'] = "OK"
            elif (row['件数(売上)'] == 1 and pd.isna(row['件数(入金)'])):
                key.at[index, '判定情報'] = "入金データなし"
                key.at[index, '照合結果'] = "キー不一致"
            elif (str(row['備考2']).find('楽天後払い') != -1 and row['差額'] == -250):
                key.at[index, '判定情報'] = "楽天後払い"
                key.at[index, '照合結果'] = "OK"
            elif (row['差額'] == -250):
                key.at[index, '判定情報'] = "後払い?"
                key.at[index, '照合結果'] = "OK"
            elif (row['差額'] == 0):
                key.at[index, '判定情報'] = "差額なし"
                key.at[index, '照合結果'] = "OK"
            # elif(row['差額'] != 0 and row['ポイント'] != 0):
            #    key.at[index, '判定情報'] = "代引き＋ポイント"
            #    key.at[index, '照合結果'] = "OK"
            else:
                key.at[index, '照合結果'] = "金額相違"
            # 入金データ存在チェック
            if (row['件数(入金)'] == 1 and pd.isna(row['件数(売上)'])):
                key.at[index, '判定情報'] = "売上データなし"
                key.at[index, '照合結果'] = "キー不一致"
        ########## ▲ ▲ ##########
        ### デバッグの為の出力 ###
        # key.to_csv('./temp/key.csv', encoding='cp932')
        key.to_csv(p_res + "\\" + p_tar_month + '_楽天結果.csv',
                   encoding='cp932', index=False)
        print(".... 突合データ出力処理 .... OK ")
        # 翌月繰越データ出力
        print(".... 翌月繰越データの出力を開始します。 .... OK ")
        yokugetu = key.query('判定情報 == "翌月データ"').copy()
        yokugetu = yokugetu.rename(
            columns={'取引額': '金額', '備考3': '日付', '備考2': '備考'})
        yokugetu[['繰越区分']] = "入金"
        yokugetu[['ポイント']] = "0"
        yokugetu[['特記事項']] = "システム繰越"
        yokugetu = yokugetu[["繰越区分", "照合キー", "金額", "ポイント", "日付", "備考", "特記事項"]]
        yokugetu.to_csv(p_res + "\\" + p_tar_month +
                        '_楽天_翌月繰越.csv', encoding='cp932', index=False)

        # 金額相違データ出力
        print(".... 金額相違データの出力を開始します。 .... OK ")
        soui = key.query('照合結果 == "金額相違"').copy()
        soui[['繰越区分']] = "金額相違"
        soui.to_csv(p_res + "\\" + p_tar_month + '_楽天_金額相違.csv',
                    encoding='cp932', index=False)

        # キー不一致データ出力
        print(".... キー不一致データの出力を開始します。 .... OK ")
        uriage_nasi = key.query('照合結果 == "キー不一致" & 判定情報 == "売上データなし"').copy()
        uriage_nasi[['繰越区分']] = "売上データなし"
        uriage_nasi.to_csv(p_res + "\\" + p_tar_month +
                           '_楽天_売上データなし.csv', encoding='cp932', index=False)

        nyukin_nasi = key.query('照合結果 == "キー不一致" & 判定情報 == "入金データなし"').copy()
        nyukin_nasi[['繰越区分']] = "入金データなし"
        nyukin_nasi.to_csv(p_res + "\\" + p_tar_month +
                           '_楽天_入金データなし.csv', encoding='cp932', index=False)

        print(".... 翌月繰越データの出力 .... OK ")
        # 集計データ出力
        print(".... 集計データの出力を開始します。 .... OK ")
        f = open(p_res + "\\" + p_tar_month +
                 '_楽天集計結果.txt', 'w', encoding='cp932')

        ####################################################
        p_tmp = '*'
        try:
            p_tmp = key['件数(売上)'].sum()
        except:
            p_tmp = 0.0
        f.write('件数(売上):' + str(p_tmp) + '件\n')
        print('件数(売上):' + str(p_tmp) + '件')
        try:
            p_tmp = key['件数(入金)'].sum()
        except:
            p_tmp = 0.0
        f.write('件数(入金):' + str(p_tmp) + '件\n')
        print('件数(入金):' + str(p_tmp) + '件')
        try:
            p_tmp = key['件数(繰越)'].sum()
        except:
            p_tmp = 0.0
        f.write('件数(繰越):' + str(p_tmp) + '件\n')
        print('件数(繰越):' + str(p_tmp) + '件')
        f.write('****************************************\n')
        # 照合結果に記載されている分結果を書き込む
        p_hantei_list = key['照合結果'].unique().tolist()
        for keyword in p_hantei_list:
            p_amt = '*'
            p_cnt = '*'
            try:
                p_amt = key.query("照合結果 == '" + keyword + "'")['取引額'].sum()
                p_cnt = key.query("照合結果 == '" + keyword + "'")['取引額'].count()
            except:
                p_amt = 0.0
                p_cnt = 0.0

            f.write(keyword + '：' + str(p_cnt) + '件 ' + str(p_amt) + '円\n')
            print(keyword + '：' + str(p_cnt) + '件 ' + str(p_amt) + '円')
        # f.write('\n')
        f.write('****************************************\n')
        f.write("処理実行日時：" + datetime.datetime.now().strftime('%Y年%m月%d日 %H:%M:%S'))
        f.write('\n')
        f.write("突合データ（フォルダ）:" + p_tar)
        f.write('\n')
        f.write("結果出力先（フォルダ）:" + p_res)
        f.write('\n')
        f.write("出力先：" + p_res)
        f.write('\n')
        f.write("処理対象：" + p_tar_month)
        f.write('\n')
        f.write("出荷確定日 >= " + p_from + " < " + p_to)
        f.write('\n')
        f.write("繰越基準日：" + tar_yyyy + "年" + tar_m + "月" + tar_d + "日")
        f.write('\n')
        f.close()
        print(".... 集計データの出力 .... OK ")
        #################### ▲ メインの処理 ▲ ####################
    #################### ▲ 楽天 ▲ ####################

    ####################  ▼ Yahoo ▼  ####################
    if nyukin_list_yahoo_receipt:
        print("  【Yahoo】の処理を開始します。")

        yahoo_u = pd.concat(nyukin_list_yahoo_receipt, axis=0, sort=True)
        if yahoo_u['金額（税込）'].dtype == "object":
            yahoo_u['金額（税込）'] = yahoo_u['金額（税込）'].str.replace(
                ',', '').fillna(0).astype(float)
        # ◎　システム備考
        yahoo_u['備考_入'] = "入(" + yahoo_u['金額（税込）'].astype(str) + ") " + yahoo_u['ファイル名']
        
        # print(yahoo_u.dtypes)
        # ***** ▽ 繰越マージ(入金) ▽ *****
        if kurikoshi_nyukin.size != 0:
            # 文字項目から数値項目への変更
            if kurikoshi_nyukin['金額'].dtype == "object":
                kurikoshi_nyukin['金額'] = kurikoshi_nyukin['金額'].str.replace(
                    ',', '').fillna(0).astype(float)
            if kurikoshi_nyukin['ポイント'].dtype == "object":
                kurikoshi_nyukin['ポイント'] = kurikoshi_nyukin['ポイント'].str.replace(
                    ',', '').fillna(0).astype(float)

            if kurikoshi_nyukin['照合キー'].dtype == "int64":
                kurikoshi_nyukin['照合キー'] = kurikoshi_nyukin['照合キー'].astype(str)

            if kurikoshi_nyukin['照合キー'].dtype == "float":
                kurikoshi_nyukin['照合キー'] = kurikoshi_nyukin['照合キー'].astype(str)
         
            # ◎　システム備考
            kurikoshi_nyukin['備考_入繰'] = "入繰(" + kurikoshi_nyukin['金額'].astype(str) + ") " + kurikoshi_nyukin['ファイル名']
            kurikoshi_nyukin['備考_入ポ'] = "入ポ(" + kurikoshi_nyukin['ポイント'].astype(str) + ") " + kurikoshi_nyukin['ファイル名']
                
            # 項目名を加工
            kurikoshi_nyukin = kurikoshi_nyukin.rename(
                columns={'照合キー': nyukin_colomun, '金額': '金額（税込）'})
            # print(kurikoshi_nyukin.dtypes)
            # 縦方向にマージ
            yahoo_u = pd.concat([yahoo_u, kurikoshi_nyukin], axis=0)
            # yahoo_u.to_csv('./temp/yahoo_u.csv', encoding='cp932')
        # ***** △ 繰越マージ（入金） △ *****
        # ◎　システム備考
        yahoo_u['システム備考2'] = ""
        if '備考_入' in yahoo_u.columns and '備考_入ポ' in yahoo_u.columns and '備考_入繰' in yahoo_u.columns:
            yahoo_u['システム備考2'] = yahoo_u['備考_入'].fillna('')  + yahoo_u['備考_入ポ'].fillna('')  + yahoo_u['備考_入繰'].fillna('') 
        
        if '備考_入' in yahoo_u.columns and '備考_入ポ' not in yahoo_u.columns and '備考_入繰' in yahoo_u.columns:
            yahoo_u['システム備考2'] = yahoo_u['備考_入'].fillna('')  + yahoo_u['備考_入繰'].fillna('') 

        if '備考_入' in yahoo_u.columns and '備考_入ポ' in yahoo_u.columns and '備考_入繰' not in yahoo_u.columns:
            yahoo_u['システム備考2'] = yahoo_u['備考_入'].fillna('')  + yahoo_u['備考_入ポ'].fillna('') 
        
        if '備考_入' in yahoo_u.columns and '備考_入ポ' not in yahoo_u.columns and '備考_入繰' not in yahoo_u.columns:
            yahoo_u['システム備考2'] = yahoo_u['備考_入'].fillna('') 

        if nyukin_list_yahoo_billing:

            billing = pd.concat(nyukin_list_yahoo_billing, axis=0, sort=True)
            # 利用項目にキャンセルの文字が含まれているものだけを抽出→符号を反転させてYahooとマージ
            billing['キャンセルFLG'] = billing['利用項目'].str.contains("キャンセル")
            billing = billing.query('キャンセルFLG == True')
            billing.loc[billing['利用項目'] ==
                        billing['利用項目'].str.replace('キャンセル分', '')]
            billing.loc[billing['金額（税込）'] == billing['金額（税込）'] * -1]
            yahoo_u = pd.concat([yahoo_u, billing], axis=0)

        #yahoo_u.to_csv('./temp/yahoo_u1.csv', encoding='cp932')

        # 注文IDの重複を除く
        yahoo_main = yahoo_u['注文ID'].drop_duplicates(keep='first')
        #yahoo_main.to_csv('./temp/yahoo_u2.csv', encoding='cp932')
        # print(taisyou_list)
        # 対象項目の数だけ実行する
        amt_sum = 0
        str_sum = ""
        str_bikou = ""
        for taisyou in taisyou_list:
            
            yahoo_temp = yahoo_u.query('利用項目 == "' + taisyou + '"')[["注文ID", "金額（税込）", "利用項目", "利用日",'システム備考2']].rename(
                columns={'金額（税込）': taisyou, '利用項目': '利用項目(' + taisyou + ')', '利用日': '利用日(' + taisyou + ')','システム備考2': 'システム備考2(' + taisyou + ')'})

            if yahoo_temp[taisyou].dtype == "object":
                yahoo_temp[taisyou] = yahoo_temp[taisyou].str.replace(
                    ',', '').fillna(0).astype(float)

            yahoo_main = pd.merge(yahoo_main, yahoo_temp,
                                  left_on='注文ID', right_on='注文ID', how='left')
            amt_sum = amt_sum + yahoo_main[taisyou].fillna(0)
            str_sum = str_sum + yahoo_main[taisyou].fillna('').astype(str)
            
            
            str_bikou = str_bikou + taisyou + ':' + yahoo_main['システム備考2(' + taisyou + ')'].fillna('').astype(str)
            # 金額をマージ
            # yahoo_main['金額（税込）'] = yahoo_main['金額（税込）'] + yahoo_main[taisyou].fillna(0)
            yahoo_main['金額（税込）'] = amt_sum
            # 文言をマージ
            # yahoo_main['利用項目'] = yahoo_main['利用項目'] + yahoo_main[taisyou].fillna('').astype(str)
            yahoo_main['利用項目'] = str_sum
            yahoo_main['システム備考2'] = str_bikou

        #yahoo_main.to_csv('./temp/yahoo_u3.csv', encoding='cp932')
        # 文言をmerge
        yahoo = yahoo_main.copy()

        # 注文IDを加工
        yahoo['注文ID'] = yahoo['注文ID'].str.replace('real-style-', '')
        yahoo['【Yahoo】注文ID2'] = yahoo['注文ID']

        yahoo_key = yahoo[['【Yahoo】注文ID2']].rename(
            columns={'【Yahoo】注文ID2': '照合キー'})
        yahoo_key_cnt = yahoo_key.value_counts()
        yahoo_key_cnt = yahoo_key.apply(pd.value_counts)
        yahoo_key_cnt = yahoo_key_cnt.rename(columns={'照合キー': '件数(入金)'})
        # Indexを列としてコピー
        yahoo_key_cnt['Key'] = yahoo_key_cnt.index

        # Keyをマージして重複をのぞいて並び替え
        if uriage_key['照合キー'].dtype == "int64":
            uriage_key['照合キー'] = uriage_key['照合キー'].astype(str)
        if yahoo_key['照合キー'].dtype == "int64":
            yahoo_key['照合キー'] = yahoo_key['照合キー'].astype(str)

        if uriage_key['照合キー'].dtype == "object":
            uriage_key['照合キー'] = uriage_key['照合キー'].astype(str)
        if yahoo_key['照合キー'].dtype == "object":
            yahoo_key['照合キー'] = yahoo_key['照合キー'].astype(str)

        key = pd.concat([uriage_key, yahoo_key], axis=0).sort_values(
            '照合キー').drop_duplicates(keep='first')
        # 売上-入金をマージ
        # データ
        if uriage['受注番号'].dtype == "int64":
            uriage['受注番号'] = uriage['受注番号'].astype(str)
        key = pd.merge(key, uriage, left_on='照合キー',
                       right_on='受注番号', how='left')

        if yahoo['【Yahoo】注文ID2'].dtype == "int64":
            yahoo['【Yahoo】注文ID2'] = yahoo['【Yahoo】注文ID2'].astype(str)
        key = pd.merge(key, yahoo, left_on='照合キー',
                       right_on='【Yahoo】注文ID2', how='left')
        # 件数
        if uriage_key_cnt['Key'].dtype == "int64":
            uriage_key_cnt['Key'] = uriage_key_cnt['Key'].astype(str)
        key = pd.merge(key, uriage_key_cnt, left_on='照合キー',
                       right_on='Key', how='left')

        if yahoo_key_cnt['Key'].dtype == "int64":
            yahoo_key_cnt['Key'] = yahoo_key_cnt['Key'].astype(str)
        key = pd.merge(key, yahoo_key_cnt, left_on='照合キー',
                       right_on='Key', how='left')

        key['取引額'] = key['総合計']
        key['決済額'] = key['金額（税込）']
        key['繰越金額'] = 0.0
        key['差額'] = key['総合計'].fillna(0) - key['金額（税込）'].fillna(0)
        key['備考2'] = key['【売上】支払名'].fillna('')
        key['備考3'] = key['【売上】出荷確定日']
        key['照合結果'] = ""
        key['決済不能'] = ""
        key['顧客情報'] = ""
        key['情報2'] = ""
        key['判定情報'] = ""
        key['繰越区分'] = ""
        key['ポイント'] = 0.0

        ### デバッグの為の出力 ###
        # key.to_csv('./temp/key.csv', encoding='cp932')
        # 結果出力用に成形
        key = key[["照合キー", "件数(売上)", "取引額", "件数(入金)", "決済額", "差額", "照合結果", "決済不能", "顧客情報", "情報2", "備考2", "備考3",
                   "ポイント", "判定情報", "店舗コード","システム備考1","システム備考2"]]

        ########## ▼  突合結果書き込み処理  ▼ ##########
        d = datetime.datetime(int(tar_yyyy), int(tar_m), int(tar_d))
        print(".... 【Yahoo】の処理 .... OK ")
        print(".... 突合データ出力処理を開始します。")
        for index, row in key.iterrows():

            # 入金データ存在チェック
            if (row['件数(売上)'] == 1 and pd.isna(row['件数(入金)']) and row['備考3'] > d):
                key.at[index, '判定情報'] = "翌月データ"
                key.at[index, '照合結果'] = "キー不一致"
            elif (row['件数(売上)'] == 1 and pd.isna(row['件数(入金)'])):
                key.at[index, '判定情報'] = "入金データなし"
                key.at[index, '照合結果'] = "キー不一致"
            # 差額チェック
            # ゆっくり払いで差額=0の場合は　NGと判定する 2024.02.29 追加
            elif (row['差額'] == 0 and row['備考2'].find('ゆっくり払い') != -1):
                key.at[index, '判定情報'] = "金額不一致"
                key.at[index, '照合結果'] = "NG"
            elif (row['差額'] == 0 and row['備考2'].find('PayPayあと払い') != -1):
                key.at[index, '判定情報'] = "金額不一致"
                key.at[index, '照合結果'] = "NG"
            # ゆっくり払いで差額=0の場合は　NGと判定する 2024.02.29 追加

            elif (row['差額'] + row['ポイント'] == 0):
                key.at[index, '判定情報'] = "差額なし（ポイントあり）"
                key.at[index, '照合結果'] = "OK"
            elif (row['差額'] + row['ポイント'] == 250 and row['備考2'].find('PayPayあと払い') != -1):
                key.at[index, '判定情報'] = "PayPayあと払い"
                key.at[index, '照合結果'] = "OK"
            elif (row['差額'] + row['ポイント'] == 250 and row['備考2'].find('ゆっくり払い') != -1):
                key.at[index, '判定情報'] = "ゆっくり払い"
                key.at[index, '照合結果'] = "OK"
            elif (row['差額'] == 0):
                key.at[index, '判定情報'] = "差額なし"
                key.at[index, '照合結果'] = "OK"
            # elif(row['差額'] != 0 and row['ポイント'] != 0):
            #    key.at[index, '判定情報'] = "代引き＋ポイント"
            #    key.at[index, '照合結果'] = "OK"
            else:
                key.at[index, '照合結果'] = "金額相違"
            # 入金データ存在チェック
            if (row['件数(入金)'] == 1 and pd.isna(row['件数(売上)'])):
                key.at[index, '判定情報'] = "売上データなし"
                key.at[index, '照合結果'] = "キー不一致"
        ########## ▲ ▲ ##########
        ### デバッグの為の出力 ###
        # key.to_csv('./temp/key.csv', encoding='cp932')
        key.to_csv(p_res + "\\" + p_tar_month + '_Yahoo結果.csv',
                   encoding='cp932', index=False)
        print(".... 突合データ出力処理 .... OK ")
        # 翌月繰越データ出力
        print(".... 翌月繰越データの出力を開始します。 .... OK ")
        yokugetu = key.query('判定情報 == "翌月データ"').copy()
        yokugetu = yokugetu.rename(
            columns={'取引額': '金額', '備考3': '日付', '備考2': '備考'})
        yokugetu[['繰越区分']] = "入金"
        yokugetu[['ポイント']] = "0"
        yokugetu[['特記事項']] = "システム繰越"
        yokugetu = yokugetu[["繰越区分", "照合キー", "金額", "ポイント", "日付", "備考", "特記事項"]]
        yokugetu.to_csv(p_res + "\\" + p_tar_month +
                        '_Yahoo_翌月繰越.csv', encoding='cp932', index=False)

        # 金額相違データ出力
        print(".... 金額相違データの出力を開始します。 .... OK ")
        soui = key.query('照合結果 == "金額相違"').copy()
        soui[['繰越区分']] = "金額相違"
        soui.to_csv(p_res + "\\" + p_tar_month + '_Yahoo_金額相違.csv',
                    encoding='cp932', index=False)

        # キー不一致データ出力
        print(".... キー不一致データの出力を開始します。 .... OK ")
        uriage_nasi = key.query('照合結果 == "キー不一致" & 判定情報 == "売上データなし"').copy()
        uriage_nasi[['繰越区分']] = "売上データなし"
        uriage_nasi.to_csv(p_res + "\\" + p_tar_month +
                           '_Yahoo_売上データなし.csv', encoding='cp932', index=False)

        nyukin_nasi = key.query('照合結果 == "キー不一致" & 判定情報 == "入金データなし"').copy()
        nyukin_nasi[['繰越区分']] = "入金データなし"
        nyukin_nasi.to_csv(p_res + "\\" + p_tar_month +
                           '_Yahoo_入金データなし.csv', encoding='cp932', index=False)

        print(".... 翌月繰越データの出力 .... OK ")
        # 集計データ出力
        print(".... 集計データの出力を開始します。 .... OK ")
        # key.count().to_csv( p_tar_folder + "\\" + p_tar_month + '_Yahoo集計結果.csv', encoding='utf_8_sig', index = True)
        f = open(p_res + "\\" + p_tar_month +
                 '_Yahoo集計結果.txt', 'w', encoding='cp932')

        ####################################################
        p_tmp = '*'
        try:
            p_tmp = key['件数(売上)'].sum()
        except:
            p_tmp = 0.0
        f.write('件数(売上):' + str(p_tmp) + '件\n')
        print('件数(売上):' + str(p_tmp) + '件')
        try:
            p_tmp = key['件数(入金)'].sum()
        except:
            p_tmp = 0.0
        f.write('件数(入金):' + str(p_tmp) + '件\n')
        print('件数(入金):' + str(p_tmp) + '件')
        try:
            p_tmp = key['件数(繰越)'].sum()
        except:
            p_tmp = 0.0
        f.write('件数(繰越):' + str(p_tmp) + '件\n')
        print('件数(繰越):' + str(p_tmp) + '件')
        f.write('****************************************\n')
        # 照合結果に記載されている分結果を書き込む
        p_hantei_list = key['照合結果'].unique().tolist()
        for keyword in p_hantei_list:
            p_amt = '*'
            p_cnt = '*'
            try:
                p_amt = key.query("照合結果 == '" + keyword + "'")['取引額'].sum()
                p_cnt = key.query("照合結果 == '" + keyword + "'")['取引額'].count()
            except:
                p_amt = 0.0
                p_cnt = 0.0

            f.write(keyword + '：' + str(p_cnt) + '件 ' + str(p_amt) + '円\n')
            print(keyword + '：' + str(p_cnt) + '件 ' + str(p_amt) + '円')
        f.write('****************************************\n')
        f.write("処理実行日時：" + datetime.datetime.now().strftime('%Y年%m月%d日 %H:%M:%S'))
        f.write('\n')
        f.write("突合データ（フォルダ）:" + p_tar)
        f.write('\n')
        f.write("結果出力先（フォルダ）:" + p_res)
        f.write('\n')
        f.write("出力先：" + p_res)
        f.write('\n')
        f.write("処理対象：" + p_tar_month)
        f.write('\n')
        f.write("出荷確定日 >= " + p_from + " < " + p_to)
        f.write('\n')
        f.write("繰越基準日：" + tar_yyyy + "年" + tar_m + "月" + tar_d + "日")
        f.write('\n')
        f.close()
        print(".... 集計データの出力 .... OK ")
        ####################  ▲ Yahoo ▲  ####################

        #################### ▼ auPay ▼ ####################
    if nyukin_list_aupay:
        print("  【auPay】の処理を開始します。")
        # ファイルを結合　→ リネーム →　件数表示用に加工
        aupay = pd.concat(nyukin_list_aupay, axis=0, sort=True)
        if aupay['決済金額'].dtype == "object":
            aupay['決済金額'] = aupay['決済金額'].str.replace(
                ',', '').fillna(0).astype(float)
        # ◎　システム備考
        aupay['備考_入'] = "入(" + aupay['決済金額'].astype(str) + ") " + aupay['ファイル名']
        
        # ***** ▽ 繰越マージ(入金) ▽ *****
        if kurikoshi_nyukin.size != 0:
            # 文字項目から数値項目への変更
            if kurikoshi_nyukin['金額'].dtype == "object":
                kurikoshi_nyukin['金額'] = kurikoshi_nyukin['金額'].str.replace(
                    ',', '').fillna(0).astype(float)
            if kurikoshi_nyukin['ポイント'].dtype == "object":
                kurikoshi_nyukin['ポイント'] = kurikoshi_nyukin['ポイント'].str.replace(
                    ',', '').fillna(0).astype(float)
            # ◎　システム備考
            kurikoshi_nyukin['備考_入繰'] = "入繰(" + kurikoshi_nyukin['金額'].astype(str) + ") " + kurikoshi_nyukin['ファイル名']
            kurikoshi_nyukin['備考_入ポ'] = "入ポ(" + kurikoshi_nyukin['ポイント'].astype(str) + ") " + kurikoshi_nyukin['ファイル名']
                    
            # 項目名を加工
            kurikoshi_nyukin = kurikoshi_nyukin.rename(
                columns={'照合キー': nyukin_colomun, '金額': '決済金額'})
            # 縦方向にマージ
            aupay = pd.concat([aupay, kurikoshi_nyukin], axis=0)
        # ***** △ 繰越マージ（入金） △ *****
        # ◎　システム備考
        aupay['システム備考2'] = ""
        if '備考_入' in aupay.columns and '備考_入ポ' in aupay.columns and '備考_入繰' in aupay.columns:
            aupay['システム備考2'] = aupay['備考_入'].fillna('')  + aupay['備考_入ポ'].fillna('')  + aupay['備考_入繰'].fillna('') 
        
        if '備考_入' in aupay.columns and '備考_入ポ' not in aupay.columns and '備考_入繰' in aupay.columns:
            aupay['システム備考2'] = aupay['備考_入'].fillna('')  + aupay['備考_入繰'].fillna('') 

        if '備考_入' in aupay.columns and '備考_入ポ' in aupay.columns and '備考_入繰' not in aupay.columns:
            aupay['システム備考2'] = aupay['備考_入'].fillna('')  + aupay['備考_入ポ'].fillna('') 
        
        if '備考_入' in aupay.columns and '備考_入ポ' not in aupay.columns and '備考_入繰' not in aupay.columns:
            aupay['システム備考2'] = aupay['備考_入'].fillna('') 

        bikou = pd.DataFrame(aupay.groupby(nyukin_colomun)['システム備考2'].apply(lambda x: "%s" % ','.join(x)))

        aupay = aupay[["取引ID", "決済金額"]].rename(
            columns={'取引ID': '【売上】受注番号', '決済金額': '【売上】金額'}).groupby('【売上】受注番号').sum()
        
        aupay = pd.concat([aupay, bikou], axis=1)
        
        aupay['【売上】受注番号2'] = aupay.index
        # print(aupay)
        aupay_key = aupay[['【売上】受注番号2']].rename(
            columns={'【売上】受注番号2': '照合キー'})
        # print(aupay_key)
        aupay_key_cnt = aupay_key.value_counts()
        aupay_key_cnt = aupay_key.apply(pd.value_counts)
        aupay_key_cnt = aupay_key_cnt.rename(columns={'照合キー': '件数(入金)'})
        # print(aupay_key_cnt)
        # Indexを列としてコピー
        aupay_key_cnt['Key'] = aupay_key_cnt.index

        ### デバッグの為の出力 ###
        # uriage_key.to_csv('./temp/uriage_key.csv', encoding='cp932')
        # aupay_key.to_csv('./temp/aupay_key.csv', encoding='cp932')
        # print(uriage_key.dtypes)
        # print(aupay_key.dtypes)
        # key.to_csv('./temp/key.csv', encoding='cp932')

        # Keyをマージして重複をのぞいて並び替え
        # key = pd.concat([uriage_key, aupay_key], axis=0).drop_duplicates(keep='first')
        if uriage_key['照合キー'].dtype == "object":
            uriage_key['照合キー'] = uriage_key['照合キー'].astype(float)

        if aupay_key['照合キー'].dtype == "object":
            aupay_key['照合キー'] = aupay_key['照合キー'].astype(float)

        key = pd.concat([uriage_key, aupay_key], axis=0).drop_duplicates()

        # if key['照合キー'].dtype == "float":
        #  key['照合キー'] = key['照合キー'].astype(str)

        # if key['照合キー'].dtype == "int64":
        #  key['照合キー'] = key['照合キー'].astype(str)
        if key['照合キー'].dtype == "object":
            key['照合キー'] = key['照合キー'].astype(float)

        if key['照合キー'].dtype == "int64":
            key['照合キー'] = key['照合キー'].astype(float)

        # 売上-入金をマージ
        # データ
        # if uriage['受注番号'].dtype == "int64":
        #  uriage['受注番号'] = uriage['受注番号'].astype(str)
        # if uriage['受注番号'].dtype == "float":
        #  uriage['受注番号'] = uriage['受注番号'].astype(str)
        if uriage['受注番号'].dtype == "object":
            uriage['受注番号'] = uriage['受注番号'].astype(float)
        if uriage['受注番号'].dtype == "int64":
            uriage['受注番号'] = uriage['受注番号'].astype(float)
        # print("*** 売上 ***")
        # print(uriage.dtypes)
        # print("*** Key ***")
        # print(key.dtypes)
        # uriage_tmp = uriage[['受注番号','【売上】支払名','【売上】出荷確定日','総合計']]

        key = pd.merge(key, uriage, left_on='照合キー',
                       right_on='受注番号', how='left')
        # uriage.to_csv('./temp/uriage.csv', encoding='cp932')
        # key.to_csv('./temp/key_uriage.csv', encoding='cp932')

        if aupay['【売上】受注番号2'].dtype == "int64":
            aupay['【売上】受注番号2'] = aupay['【売上】受注番号2'].astype(float)

        if aupay['【売上】受注番号2'].dtype == "object":
            aupay['【売上】受注番号2'] = aupay['【売上】受注番号2'].astype(float)

        key = pd.merge(key, aupay, left_on='照合キー',
                       right_on='【売上】受注番号2', how='left')
        # key.to_csv('./temp/key003.csv', encoding='cp932')
        # 件数
        if uriage_key_cnt['Key'].dtype == "int64":
            uriage_key_cnt['Key'] = uriage_key_cnt['Key'].astype(float)
        if uriage_key_cnt['Key'].dtype == "object":
            uriage_key_cnt['Key'] = uriage_key_cnt['Key'].astype(float)

        key = pd.merge(key, uriage_key_cnt, left_on='照合キー',
                       right_on='Key', how='left')

        if aupay_key_cnt['Key'].dtype == "int64":
            aupay_key_cnt['Key'] = aupay_key_cnt['Key'].astype(float)

        if aupay_key_cnt['Key'].dtype == "object":
            aupay_key_cnt['Key'] = aupay_key_cnt['Key'].astype(float)

        key = pd.merge(key, aupay_key_cnt, left_on='照合キー',
                       right_on='Key', how='left')

        # key.to_csv('./temp/key.csv', encoding='cp932')
        # aupay_key_cnt.to_csv('./temp/aupay_key_cnt.csv', encoding='cp932')
        # uriage_key_cnt.to_csv('./temp/uriage_key_cnt.csv', encoding='cp932')

        key['取引額'] = key['総合計']
        key['決済額'] = key['【売上】金額']
        key['繰越金額'] = 0.0
        key['差額'] = key['総合計'].fillna(0) - key['【売上】金額'].fillna(0)
        key['備考2'] = key['【売上】支払名']
        key['備考3'] = key['【売上】出荷確定日']
        key['照合結果'] = ""
        key['決済不能'] = ""
        key['顧客情報'] = ""
        key['情報2'] = ""
        key['判定情報'] = ""
        key['繰越区分'] = ""
        key['ポイント'] = 0.0

        ### デバッグの為の出力 ###
        # key.to_csv('./temp/key.csv', encoding='cp932')

        # 結果出力用に成形
        key = key[["照合キー", "件数(売上)", "取引額", "件数(入金)", "決済額", "差額", "照合結果", "決済不能", "顧客情報", "情報2", "備考2", "備考3",
                   "ポイント", "判定情報", "店舗コード","システム備考1","システム備考2"]]

        # print(key.dtypes)

        ########## ▼  突合結果書き込み処理  ▼ ##########
        d = datetime.datetime(int(tar_yyyy), int(tar_m), int(tar_d))
        print(".... 【auPay】の処理 .... OK ")
        print(".... 突合データ出力処理を開始します。")
        for index, row in key.iterrows():

            # 入金データ存在チェック
            if (row['件数(売上)'] == 1 and pd.isna(row['件数(入金)']) and row['備考2'] == "ポイント全額支払い"):
                key.at[index, '判定情報'] = "ポイント全額払い"
                key.at[index, '照合結果'] = "OK"
            elif (row['件数(売上)'] == 1 and pd.isna(row['件数(入金)']) and row['備考3'] > d):
                key.at[index, '判定情報'] = "翌月データ"
                key.at[index, '照合結果'] = "キー不一致"
            elif (row['件数(売上)'] == 1 and pd.isna(row['件数(入金)'])):
                key.at[index, '判定情報'] = "入金データなし"
                key.at[index, '照合結果'] = "キー不一致"
            # 差額
            elif (row['差額'] == 0 and row['備考2'].find('楽天後払い') != -1):
                key.at[index, '判定情報'] = "差額あり"
                key.at[index, '照合結果'] = "金額相違"
            # 差額チェック
            elif (row['差額'] + row['ポイント'] == 0):
                key.at[index, '判定情報'] = "差額なし（ポイントあり）"
                key.at[index, '照合結果'] = "OK"
            elif (row['差額'] + row['ポイント'] == 250 and row['備考2'].find('楽天後払い') != -1):
                key.at[index, '判定情報'] = "楽天後払い"
                key.at[index, '照合結果'] = "OK"
            elif (str(row['備考2']).find('楽天後払い') != -1 and row['差額'] == 250):
                key.at[index, '判定情報'] = "楽天後払い"
                key.at[index, '照合結果'] = "OK"
            elif (row['差額'] == 0):
                key.at[index, '判定情報'] = "差額なし"
                key.at[index, '照合結果'] = "OK"
            # elif(row['差額'] != 0 and row['ポイント'] != 0):
            #    key.at[index, '判定情報'] = "代引き＋ポイント"
            #    key.at[index, '照合結果'] = "OK"
            else:
                key.at[index, '照合結果'] = "金額相違"
            # 入金データ存在チェック
            if (row['件数(入金)'] == 1 and pd.isna(row['件数(売上)'])):
                key.at[index, '判定情報'] = "売上データなし"
                key.at[index, '照合結果'] = "キー不一致"
        ########## ▲ ▲ ##########
        ### デバッグの為の出力 ###
        # key.to_csv('./temp/key.csv', encoding='cp932')
        key.to_csv(p_res + "\\" + p_tar_month + '_auPay結果.csv',
                   encoding='cp932', index=False)
        print(".... 突合データ出力処理 .... OK ")
        # 翌月繰越データ出力
        print(".... 翌月繰越データの出力を開始します。 .... OK ")
        yokugetu = key.query('判定情報 == "翌月データ"').copy()
        yokugetu = yokugetu.rename(
            columns={'取引額': '金額', '備考3': '日付', '備考2': '備考'})
        yokugetu[['繰越区分']] = "入金"
        yokugetu[['ポイント']] = "0"
        yokugetu[['特記事項']] = "システム繰越"
        yokugetu = yokugetu[["繰越区分", "照合キー", "金額", "ポイント", "日付", "備考", "特記事項"]]
        yokugetu.to_csv(p_res + "\\" + p_tar_month +
                        '_auPay_翌月繰越.csv', encoding='cp932', index=False)

        # 金額相違データ出力
        print(".... 金額相違データの出力を開始します。 .... OK ")
        soui = key.query('照合結果 == "金額相違"').copy()
        soui[['繰越区分']] = "金額相違"
        soui.to_csv(p_res + "\\" + p_tar_month + '_auPay_金額相違.csv',
                    encoding='cp932', index=False)

        # キー不一致データ出力
        print(".... キー不一致データの出力を開始します。 .... OK ")
        uriage_nasi = key.query('照合結果 == "キー不一致" & 判定情報 == "売上データなし"').copy()
        uriage_nasi[['繰越区分']] = "売上データなし"
        uriage_nasi.to_csv(p_res + "\\" + p_tar_month +
                           '_auPay_売上データなし.csv', encoding='cp932', index=False)

        nyukin_nasi = key.query('照合結果 == "キー不一致" & 判定情報 == "入金データなし"').copy()
        nyukin_nasi[['繰越区分']] = "入金データなし"
        nyukin_nasi.to_csv(p_res + "\\" + p_tar_month +
                           '_auPay_入金データなし.csv', encoding='cp932', index=False)

        print(".... 翌月繰越データの出力 .... OK ")
        # 集計データ出力
        print(".... 集計データの出力を開始します。 .... OK ")
        f = open(p_res + "\\" + p_tar_month +
                 '_auPay集計結果.txt', 'w', encoding='cp932')

        ####################################################
        p_tmp = '*'
        try:
            p_tmp = key['件数(売上)'].sum()
        except:
            p_tmp = 0.0
        f.write('件数(売上):' + str(p_tmp) + '件\n')
        print('件数(売上):' + str(p_tmp) + '件')
        try:
            p_tmp = key['件数(入金)'].sum()
        except:
            p_tmp = 0.0
        f.write('件数(入金):' + str(p_tmp) + '件\n')
        print('件数(入金):' + str(p_tmp) + '件')
        try:
            p_tmp = key['件数(繰越)'].sum()
        except:
            p_tmp = 0.0
        f.write('件数(繰越):' + str(p_tmp) + '件\n')
        print('件数(繰越):' + str(p_tmp) + '件')
        f.write('****************************************\n')
        # 照合結果に記載されている分結果を書き込む
        p_hantei_list = key['照合結果'].unique().tolist()
        for keyword in p_hantei_list:
            p_amt = '*'
            p_cnt = '*'
            try:
                p_amt = key.query("照合結果 == '" + keyword + "'")['取引額'].sum()
                p_cnt = key.query("照合結果 == '" + keyword + "'")['取引額'].count()
            except:
                p_amt = 0.0
                p_cnt = 0.0

            f.write(keyword + '：' + str(p_cnt) + '件 ' + str(p_amt) + '円\n')
            print(keyword + '：' + str(p_cnt) + '件 ' + str(p_amt) + '円')
        f.write('****************************************\n')
        f.write("処理実行日時：" + datetime.datetime.now().strftime('%Y年%m月%d日 %H:%M:%S'))
        f.write('\n')
        f.write("突合データ（フォルダ）:" + p_tar)
        f.write('\n')
        f.write("結果出力先（フォルダ）:" + p_res)
        f.write('\n')
        f.write("出力先：" + p_res)
        f.write('\n')
        f.write("処理対象：" + p_tar_month)
        f.write('\n')
        f.write("出荷確定日 >= " + p_from + " < " + p_to)
        f.write('\n')
        f.write("繰越基準日：" + tar_yyyy + "年" + tar_m + "月" + tar_d + "日")
        f.write('\n')
        f.close()
        print(".... 集計データの出力 .... OK ")
        #################### ▲ メインの処理 ▲ ####################
    #################### ▲ auPay ▲ ####################

    messagebox.showinfo("info", "処理が完了しました。")
    print(".... ▲ ＊＊＊ 突合処理が完了しました。 ＊＊＊ ▲")
    isOutputDbg = TRUE
    if isOutputDbg:
        f_dbg.close
    #################### ▲ メインの処理 ▲ ####################


if __name__ == "__main__":

    # rootの作成
    root = Tk()
    root.title("RS突合くん")

    # ECデータ(フォルダ)
    # フレーム
    frame001 = ttk.Frame(root, padding=10)
    frame001.grid(row=0, column=1, sticky=W)

    # ラベルの作成
    IDirLabel = ttk.Label(frame001, text="1.突合データ(フォルダ)＞＞", padding=(5, 2))
    IDirLabel.pack(side=LEFT)

    # エントリーの作成
    entry001 = StringVar()
    IDirEntry = ttk.Entry(frame001, textvariable=entry001, width=30)
    IDirEntry.pack(side=LEFT)

    # ボタンの作成
    IDirButton = ttk.Button(frame001, text="参照", command=dirdialog_clicked_001)
    IDirButton.pack(side=LEFT)

    # カスタマーリングス(フォルダ)
    # フレーム
    frame002 = ttk.Frame(root, padding=10)
    frame002.grid(row=2, column=1, sticky=W)

    # ラベルの作成
    IDirLabe2 = ttk.Label(frame002, text="2.結果出力先(フォルダ)＞＞", padding=(5, 2))
    IDirLabe2.pack(side=LEFT)

    # エントリーの作成
    entry002 = StringVar()
    IDirEntry = ttk.Entry(frame002, textvariable=entry002, width=30)
    IDirEntry.pack(side=LEFT)

    # ボタンの作成
    IDirButton = ttk.Button(frame002, text="参照", command=dirdialog_clicked_002)
    IDirButton.pack(side=LEFT)

    # 繰越年
    # フレーム
    frame005_1 = ttk.Frame(root, padding=10)
    frame005_1.grid(row=4, column=1, sticky=W)
    frame005_1.grid_configure(padx=5, pady=5)
    # ラベル
    IDirLabel = ttk.Label(frame005_1, text="3.対象年を指定。 ＞＞", padding=(5, 2))
    IDirLabel.pack(side=LEFT)
    # エントリー
    entry005_1 = StringVar()
    cb_1 = ttk.Combobox(frame005_1, textvariable=entry005_1, height=5, width=6)
    cb_1.bind('<<ComboboxSelected>>', selectbox_clicked_005_1)
    cb_1['values'] = ('2021年', '2022年', '2023年', '2024年', '2025年', '2026年', '2027年', '2028年', '2029年', '2030年', '2031年', '2032年', '2033年', '2034年', '2035年')
    cb_1.set("2023年")
    cb_1.pack(side=LEFT)

    # 繰越月
    # フレーム
    frame005_2 = ttk.Frame(root, padding=10)
    frame005_2.grid(row=6, column=1, sticky=W)
    frame005_2.grid_configure(padx=5, pady=5)
    # ラベル
    IDirLabel = ttk.Label(frame005_2, text="4.対象月を指定。 ＞＞", padding=(5, 2))
    IDirLabel.pack(side=LEFT)
    # エントリー
    entry005_2 = StringVar()
    cb_2 = ttk.Combobox(
        frame005_2, textvariable=entry005_2, height=12, width=3)
    cb_2.bind('<<ComboboxSelected>>', selectbox_clicked_005_2)
    cb_2['values'] = ('1月', '2月', '3月', '4月', '5月', '6月',
                      '7月', '8月', '9月', '10月', '11月', '12月')
    cb_2.set("1月")
    cb_2.pack(side=LEFT)

    # 繰越日
    # フレーム
    frame006 = ttk.Frame(root, padding=10)
    frame006.grid(row=10, column=1, sticky=W)
    frame006.grid_configure(padx=5, pady=5)
    # ラベル
    IDirLabel = ttk.Label(frame006, text="5.翌月繰り越し日を指定。 ＞＞", padding=(5, 2))
    IDirLabel.pack(side=LEFT)
    # エントリー
    entry006 = StringVar()
    cb = ttk.Combobox(frame006, textvariable=entry006, height=31, width=4)
    cb.bind('<<ComboboxSelected>>', selectbox_clicked_006)
    cb['values'] = ('1日', '2日', '3日', '4日', '5日', '6日', '7日', '8日', '9日', '10日', '11日', '12日', '13日', '14日', '15日', '16日', '17日', '18日', '19日', '20日', '21日', '22日', '23日', '24日', '25日',
                    '26日', '27日', '28日', '29日', '30日', '31日')
    cb.set("26日")
    cb.pack(side=LEFT)

    # デバッグモード
    frame007 = ttk.Frame(root, padding=10)
    frame007.grid(row=12, column=1, sticky=W)

    # ラベルの作成
    IDirLabel = ttk.Label(frame007, text="デバッグモード ＞＞", padding=(5, 2))
    IDirLabel.pack(side=LEFT)

    # エントリーの作成
    entry007 = IntVar()
    entry007.set(True)
    IDirEntry = ttk.Checkbutton(frame007, text="On", variable=entry007)
    IDirEntry.pack(side=LEFT)

    # 実行(ボタン)
    frame010 = ttk.Frame(root, padding=20)
    frame010.grid(row=14, column=1, sticky=W)
    button1 = ttk.Button(frame010, text="実行", command=conductMain)
    button1.pack(fill="x", padx=30, side="left")
    # #
    root.mainloop()
