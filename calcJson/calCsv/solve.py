import pandas as pd

pad = pd.read_csv("./mimicdata.csv")
# 获取行数
num = pad.index.size

with open("data_mimiciv.txt", "w", encoding='utf-8') as ftxt:
    for i in range(0, num):
        originalText = ("患者患了感染性休克，数据来自mimic iv数据库，患者编号为" + str(pad.loc[i]["患者编号"])
                        + "，sofa评分为" + str(pad.loc[i]["sofa评分"])
                        + "，服用的抗生素药物为" + pad.loc[i]["用的抗生素"] + "。")
        dis_start_pos = 4
        dis_end_pos = 9
        drug_start_pos = len(originalText) - 1 - len(pad.loc[i]["用的抗生素"])
        drug_end_pos = len(originalText) - 1
        s = ("{\"originalText\": \"" + originalText + "\""
             + ", \"entities\": [{\"label_type\": \"疾病\", \"overlap\": 0, \"start_pos\": " +
             str(dis_start_pos) + ", \"end_pos\": " + str(dis_end_pos) + "}, " +
             "{\"label_type\": \"药物治疗手段\", \"overlap\": 0, \"start_pos\": " +
             str(drug_start_pos) + ", \"end_pos\": " + str(drug_end_pos) + "}]}" + "\n")
        ftxt.write(s)
ftxt.close()
