import json


def calcJson_Disease():
    with open('youlai.json', 'r', encoding='utf-8') as fjson:
        data = json.load(fjson)
    num = len(data)
    fjson.close()
    with open("cql_disease.txt", "w") as ftxt:
        for i in range(0, num):
            dis_name = data[i]['disName']
            if dis_name:  # 既不是空串 也不是null
                s = "CREATE (a" + f'{i}' + ": Disease" + "{name:" + f"'{dis_name}'" + ", group: 1" + "})" + "\n"
                ftxt.write(s)
        # 创建disName group为1
    ftxt.close()


def calcJson_DisLoc():
    with open('youlai.json', 'r', encoding='utf-8') as fjson:
        data = json.load(fjson)
    num = len(data)
    fjson.close()
    with open("cql_disloc.txt", "w") as ftxt:
        loc = set()
        for i in range(0, num):
            dis_loc = data[i]['disLoc']
            if not dis_loc:
                continue
            if dis_loc in loc:
                continue
            else:
                loc.add(dis_loc)
                s = "CREATE (b" + f'{i}' + ": DiseaseLoc" + "{name:" + f"'{dis_loc}'" + ", group: 2" + "})" + "\n"
                ftxt.write(s)
    ftxt.close()


def calcJson_DisTreat():
    with open('youlai.json', 'r', encoding='utf-8') as fjson:
        data = json.load(fjson)
    num = len(data)
    fjson.close()
    with open("cql_distreat.txt", "w") as ftxt:
        treat = set()
        for i in range(0, num):
            dis_treat = data[i]['disTreat']
            if not dis_treat:
                continue
            if dis_treat in treat:
                continue
            else:
                treat.add(dis_treat)
                s = "CREATE (c" + f'{i}' + ": DiseaseTreat" + "{name:" + f"'{dis_treat}'" + ", group: 3" + "})" + "\n"
                ftxt.write(s)
    ftxt.close()


def calcJson_DisDrug():
    with open('youlai.json', 'r', encoding='utf-8') as fjson:
        data = json.load(fjson)
    num = len(data)
    fjson.close()
    with open("cql_disdrug.txt", "w") as ftxt:
        drugs = set()
        for i in range(0, num):
            dis_drug = data[i]['disDrug']
            if dis_drug:
                druglist = dis_drug.split('、')
                tick = 0
                for drug in druglist:
                    if drug in drugs:
                        continue
                    else:
                        drugs.add(drug)
                        s = "CREATE (d" + f'{i}{tick}' + ": DiseaseDrug" + "{name:" + f"'{drug}'" + ", group: 4" + "})" + "\n"
                        ftxt.write(s)
                        tick += 1
    ftxt.close()


def calcJson_DisSymptom():
    with open('youlai.json', 'r', encoding='utf-8') as fjson:
        data = json.load(fjson)
    num = len(data)
    fjson.close()
    with open("cql_dissymptom.txt", "w") as ftxt:
        symptoms = set()
        for i in range(0, num):
            dis_symptom = data[i]['disSymptom']
            if dis_symptom:  # 既不是空串 也不是null
                if dis_symptom not in symptoms:
                    symptoms.add(dis_symptom)
                    s = "CREATE (e" + f'{i}' + ": DiseaseSymptom" + "{name:" + f"'{dis_symptom}'" + ", group: 5" + "})" + "\n"
                    ftxt.write(s)
    ftxt.close()


def re_disease_disloc():  # 疾病 发病部位
    with open('youlai.json', 'r', encoding='utf-8') as fjson:
        data = json.load(fjson)
    num = len(data)  # num: 2331
    fjson.close()
    step = 301
    with open("cql_re_disease_disloc.txt", "w", encoding='utf-8') as ftxt:
        # 先写所有的MATCH语句
        for i in range(101, step):
            dis_name = data[i]['disName']
            dis_loc = data[i]['disLoc']
            if dis_name and dis_loc:  # 名字和位置都不为空 就可以建立关系
                s = (
                            "MATCH (b" + f'{i}' + ":Disease {name:" + f"'{dis_name}'" + "}),(d" + f'{i}' + ":DiseaseLoc {name:" +
                            f"'{dis_loc}'" + "})" + "\n")
                ftxt.write(s)
        # 再写所有的CREATE语句
        for i in range(4, step):
            dis_name = data[i]['disName']
            dis_loc = data[i]['disLoc']
            if dis_name and dis_loc:  # 名字和位置都不为空 就可以建立关系
                s = "CREATE (b" + f'{i}' + ")-[" + "r" + f'{i}' + ":Location]->(d" + f'{i}' + ")" + "\n"
                ftxt.write(s)
    ftxt.close()


def re_disease_disdrug():  # 疾病 推荐药物
    with open('youlai.json', 'r', encoding='utf-8') as fjson:
        data = json.load(fjson)
    num = len(data)
    fjson.close()
    with open("cql_re_disease_disdrug.txt", "w", encoding='utf-8') as ftxt:
        # 先写所有的match语句
        for i in range(0, num):
            dis_name = data[i]['disName']
            drugs = data[i]['disDrug']
            if dis_name and drugs:  # 名字和药物都不为空
                druglist = drugs.split('、')
                j = 0
                for drug in druglist:
                    s = ("MATCH (b" + f'{i}' + ":Disease {name:" + f"'{dis_name}'" + "}),(drug" + f'{i}{j}'
                         + ":DiseaseDrug {name:" + f"'{drug}'" + "})" + "\n")
                    ftxt.write(s)
                    j += 1
        # 再写所有的create语句
        for i in range(0, num):
            dis_name = data[i]['disName']
            drugs = data[i]['disDrug']
            if dis_name and drugs:  # 名字和药物都不为空
                druglist = drugs.split('、')
                j = 0
                for drug in druglist:
                    s = "CREATE (b" + f'{i}' + ")-[" + "r" + f'{i}{j}' + ":Recommend_Drug]->(drug" + f'{i}{j}' + ")" + "\n"
                    ftxt.write(s)
                    j += 1
    ftxt.close()


def re_disease_symptom():
    with open('youlai.json', 'r', encoding='utf-8') as fjson:
        data = json.load(fjson)
    num = len(data)
    fjson.close()
    with open("cql_re_disease_dissymptom.txt", "w", encoding='utf-8') as ftxt:
        # 先写所有的MATCH语句
        for i in range(0, num):
            dis_name = data[i]['disName']
            dis_symptom = data[i]['disSymptom']
            if dis_name and dis_symptom:  # 名字和症状都不为空 就可以建立关系
                s = (
                            "MATCH (b" + f'{i}' + ":Disease {name:" + f"'{dis_name}'" + "}),(symptom" + f'{i}' + ":DiseaseSymptom {name:"
                            + f"'{dis_symptom}'" + "})" + "\n")
                ftxt.write(s)
        # 再写所有的CREATE语句
        for i in range(0, num):
            dis_name = data[i]['disName']
            dis_symptom = data[i]['disSymptom']
            if dis_name and dis_symptom:  # 名字和症状都不为空 就可以建立关系
                s = "CREATE (b" + f'{i}' + ")-[" + "rsymptom" + f'{i}' + ":Symptom]->(symptom" + f'{i}' + ")" + "\n"
                ftxt.write(s)
    ftxt.close()


def re_disease_treat():
    with open('youlai.json', 'r', encoding='utf-8') as fjson:
        data = json.load(fjson)
    num = len(data)
    fjson.close()
    with open("cql_re_disease_distreat.txt", "w", encoding='utf-8') as ftxt:
        # 先写所有的MATCH语句
        for i in range(0, num):
            dis_name = data[i]['disName']
            dis_treat = data[i]['disTreat']
            if dis_name and dis_treat:  # 名字和治疗方式都不为空 就可以建立关系
                s = (
                            "MATCH (b" + f'{i}' + ":Disease {name:" + f"'{dis_name}'" + "}),(treat" + f'{i}' + ":DiseaseTreat {name:" +
                            f"'{dis_treat}'" + "})" + "\n")
                ftxt.write(s)
        # 再写所有的CREATE语句
        for i in range(0, num):
            dis_name = data[i]['disName']
            dis_treat = data[i]['disTreat']
            if dis_name and dis_treat:  # 名字和治疗方式都不为空 就可以建立关系
                s = "CREATE (b" + f'{i}' + ")-[" + "rtreat" + f'{i}' + ":TreatWay]->(treat" + f'{i}' + ")" + "\n"
                ftxt.write(s)
    ftxt.close()


def process_data():
    with open('youlai.json', 'r', encoding='utf-8') as fjson:
        data = json.load(fjson)
    num = len(data)
    fjson.close()

    name_dict = dict()
    name_cnt = 0
    name_flag = False

    loc_dict = dict()
    loc_cnt = 0
    loc_flag = False

    treat_dict = dict()
    treat_cnt = 0
    treat_flag = False

    drug_dict = dict()
    drug_cnt = 0
    drug_flag_dict = dict()

    symptom_dict = dict()
    symptom_cnt = 0
    symptom_flag = False

    re_dict = dict()
    re_cnt = 0

    with open("cql.txt", "w", encoding='utf-8') as ftxt:
        for i in range(0, num):  # 遍历每一行数据
            dis_name = data[i]['disName']
            dis_loc = data[i]['disLoc']
            dis_treat = data[i]['disTreat']
            dis_drugs = data[i]['disDrug']
            dis_symptom = data[i]['disSymptom']

            if dis_name:  # 疾病名称正常
                if dis_name not in name_dict:  # 如果不在字典里，加入字典，给予这个病固定编号
                    name_dict[dis_name] = name_cnt
                    name_cnt += 1
                    name_flag = True
            if dis_loc:  # 发病位置正常
                if dis_loc not in loc_dict:  # 发病位置不在字典里，加入字典，给予固定编号
                    loc_dict[dis_loc] = loc_cnt
                    loc_cnt += 1
                    loc_flag = True
            if dis_treat:
                if dis_treat not in treat_dict:
                    treat_dict[dis_treat] = treat_cnt
                    treat_cnt += 1
                    treat_flag = True
            if dis_drugs:
                druglist = dis_drugs.split('、')
                for drug in druglist:
                    if drug not in drug_dict:
                        drug_dict[drug] = drug_cnt
                        drug_cnt += 1
                        drug_flag_dict[drug] = True
            if dis_symptom:
                if dis_symptom not in symptom_dict:
                    symptom_dict[dis_symptom] = symptom_cnt
                    symptom_cnt += 1
                    symptom_flag = True
            #  此时所有的都已经判断完毕
            #  现在开始处理关系
            if dis_name:
                # dis_loc
                if dis_loc:
                    # 两个都正常继续处理
                    if name_flag and loc_flag:
                        # 如果两个都是True 说明都是新的 可以直接create节点和关系
                        s = ("CREATE (" + "dis" + f'{name_dict[dis_name]}' + ": Disease" + "{name:" + f"'{dis_name}'" +
                             ", group: 1" + "})-" + "[" + "re" + f'{re_cnt}' + ":Location]->(" + "disloc" +
                             f'{loc_dict[dis_loc]}' + ": DiseaseLoc" + "{name:" + f"'{dis_loc}'" + ", group: 2" + "})" + "\n")
                        ftxt.write(s)
                        re_dict[dis_name + dis_loc] = re_cnt
                        re_cnt += 1
                        name_flag = False
                    elif name_flag and not loc_flag:
                        # 如果loc之前已经有过了
                        # 需要先创建疾病
                        s = "CREATE (" + "dis" + f'{name_dict[dis_name]}' + ": Disease" + "{name:" + f"'{dis_name}'" + ", group: 1" + "})" + "\n"
                        ftxt.write(s)
                        # 然后创建两者的关系
                        # 先写match
                        s_re_match = (
                                    "MATCH (dis" + f'{name_dict[dis_name]}' + ":Disease {name:" + f"'{dis_name}'" + "}),(disloc" + f'{loc_dict[dis_loc]}' +
                                    ":DiseaseLoc {name:" + f"'{dis_loc}'" + "})" + "\n")
                        ftxt.write(s_re_match)
                        # 再写create
                        s_re_create = (
                                    "CREATE (dis" + f'{name_dict[dis_name]}' + ")-[" + "re" + f'{re_cnt}' + ":Location]->(disloc" +
                                    f'{loc_dict[dis_loc]}' + ")" + "\n")
                        ftxt.write(s_re_create)
                        re_dict[dis_name + dis_loc] = re_cnt
                        re_cnt += 1
                        name_flag = False

                # dis_treat
                if dis_treat:
                    # 疾病肯定已经有了
                    if treat_flag:  # treat之前没有
                        # 先创建treat
                        s = "CREATE (distreat" + f'{treat_dict[dis_treat]}' + ": DiseaseTreat" + "{name:" + f"'{dis_treat}'" + ", group: 3" + "})" + "\n"
                        ftxt.write(s)
                        # 再创建关系
                        # 先写match
                        s_re_match = (
                                "MATCH (dis" + f'{name_dict[dis_name]}' + ":Disease {name:" + f"'{dis_name}'" + "}),(distreat" + f'{treat_dict[dis_treat]}' +
                                ":DiseaseTreat {name:" + f"'{dis_treat}'" + "})" + "\n")
                        ftxt.write(s_re_match)
                        # 再写create
                        s_re_create = (
                                "CREATE (dis" + f'{name_dict[dis_name]}' + ")-[" + "re" + f'{re_cnt}' + ":TreatWays]->(distreat" +
                                f'{treat_dict[dis_treat]}' + ")" + "\n")
                        ftxt.write(s_re_create)

                        re_dict[dis_name + dis_treat] = re_cnt
                        re_cnt += 1
                    elif not treat_flag:
                        # 如果treat之前已经有过了
                        # 然后创建两者的关系
                        # 先写match
                        s_re_match = (
                                "MATCH (dis" + f'{name_dict[dis_name]}' + ":Disease {name:" + f"'{dis_name}'" + "}),(distreat" + f'{treat_dict[dis_treat]}' +
                                ":DiseaseTreat {name:" + f"'{dis_treat}'" + "})" + "\n")
                        ftxt.write(s_re_match)
                        # 再写create
                        s_re_create = (
                                "CREATE (dis" + f'{name_dict[dis_name]}' + ")-[" + "re" + f'{re_cnt}' + ":TreatWays]->(distreat" +
                                f'{treat_dict[dis_treat]}' + ")" + "\n")
                        ftxt.write(s_re_create)
                        re_dict[dis_name + dis_treat] = re_cnt
                        re_cnt += 1

                # dis_drugs
                if dis_drugs:
                    for drug in druglist:
                        # 两个都正常继续处理
                        if drug in drug_flag_dict:
                            s = "CREATE (disdrug" + f'{drug_dict[drug]}' + ": DiseaseDrug" + "{name:" + f"'{drug}'" + ", group: 4" + "})" + "\n"
                            ftxt.write(s)
                            # 先写match
                            s_re_match = (
                                    "MATCH (dis" + f'{name_dict[dis_name]}' + ":Disease {name:" + f"'{dis_name}'" + "}),(disdrug" + f'{drug_dict[drug]}' +
                                    ":DiseaseDrug {name:" + f"'{drug}'" + "})" + "\n")
                            ftxt.write(s_re_match)
                            # 再写create
                            s_re_create = (
                                    "CREATE (dis" + f'{name_dict[dis_name]}' + ")-[" + "re" + f'{re_cnt}' + ":Recommend_Drug]->(disdrug" +
                                    f'{drug_dict[drug]}' + ")" + "\n")
                            ftxt.write(s_re_create)
                            re_dict[dis_name + drug] = re_cnt
                            re_cnt += 1
                            drug_flag_dict.pop(drug)
                        elif drug not in drug_flag_dict:
                            # 如果drug之前已经有过了
                            # 然后创建两者的关系
                            # 先写match
                            s_re_match = (
                                    "MATCH (dis" + f'{name_dict[dis_name]}' + ":Disease {name:" + f"'{dis_name}'" + "}),(disdrug" + f'{drug_dict[drug]}' +
                                    ":DiseaseDrug {name:" + f"'{drug}'" + "})" + "\n")
                            ftxt.write(s_re_match)
                            # 再写create
                            s_re_create = (
                                    "CREATE (dis" + f'{name_dict[dis_name]}' + ")-[" + "re" + f'{re_cnt}' + ":Recommend_Drug]->(disdrug" +
                                    f'{drug_dict[drug]}' + ")" + "\n")
                            ftxt.write(s_re_create)
                            re_dict[dis_name + drug] = re_cnt
                            re_cnt += 1

                # dissymptom
                if dis_symptom:
                    # 两个都正常继续处理
                    if symptom_flag:
                        # 如果两个都是True 说明都是新的 可以直接create节点和关系
                        s = "CREATE (dissymptom" + f'{symptom_dict[dis_symptom]}' + ": DiseaseSymptom" + "{name:" + f"'{dis_symptom}'" + ", group: 5" + "})" + "\n"
                        ftxt.write(s)
                        # 先写match
                        s_re_match = (
                                "MATCH (dis" + f'{name_dict[dis_name]}' + ":Disease {name:" + f"'{dis_name}'" + "}),(dissymptom" + f'{symptom_dict[dis_symptom]}' +
                                ":DiseaseSymptom {name:" + f"'{dis_symptom}'" + "})" + "\n")
                        ftxt.write(s_re_match)
                        # 再写create
                        s_re_create = (
                                "CREATE (dis" + f'{name_dict[dis_name]}' + ")-[" + "re" + f'{re_cnt}' + ":Symptom]->(dissymptom" +
                                f'{symptom_dict[dis_symptom]}' + ")" + "\n")
                        ftxt.write(s_re_create)
                        re_dict[dis_name + dis_symptom] = re_cnt
                        re_cnt += 1
                    elif not symptom_flag:
                        # 如果symptom之前已经有过了
                        # 然后创建两者的关系
                        # 先写match
                        s_re_match = (
                                "MATCH (dis" + f'{name_dict[dis_name]}' + ":Disease {name:" + f"'{dis_name}'" + "}),(dissymptom" + f'{symptom_dict[dis_symptom]}' +
                                ":DiseaseSymptom {name:" + f"'{dis_symptom}'" + "})" + "\n")
                        ftxt.write(s_re_match)
                        # 再写create
                        s_re_create = (
                                "CREATE (dis" + f'{name_dict[dis_name]}' + ")-[" + "re" + f'{re_cnt}' + ":Symptom]->(dissymptom" +
                                f'{symptom_dict[dis_symptom]}' + ")" + "\n")
                        ftxt.write(s_re_create)
                        re_dict[dis_name + dis_symptom] = re_cnt
                        re_cnt += 1
            # 此时处理完了这行的所有语句
            ftxt.write('\n\n')

            name_flag = False
            loc_flag = False
            treat_flag = False
            drug_flag_dict.clear()
            symptom_flag = False

    ftxt.close()


if __name__ == '__main__':
    # calcJson_Disease()
    # calcJson_DisLoc()
    # calcJson_DisTreat()
    # calcJson_DisDrug()
    # calcJson_DisSymptom()
    # re_disease_disloc()
    # re_disease_disdrug()
    # re_disease_symptom()
    # re_disease_treat()
    process_data()
