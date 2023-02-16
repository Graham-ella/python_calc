from neo4j import GraphDatabase

driver = GraphDatabase.driver("neo4j://localhost:7687",
                              auth=("neo4j", "12345678"))

with driver.session(database="neo4j") as session:
    f = open('../cql.txt', 'r', encoding='utf-8')
    lines = f.readlines()
    num = len(lines)
    i = 0
    while i < num:
        if lines[i][0] == 'C':
            session.run(lines[i])
            i += 1
        elif lines[i][0] == 'M':
            s = lines[i] + ' ' + lines[i+1]
            session.run(s)
            i += 2
        else:
            i += 1
            continue
    f.close()
driver.close()
