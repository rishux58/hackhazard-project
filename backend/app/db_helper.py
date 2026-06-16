from neo4j import GraphDatabase

class Neo4jHandler:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(
            uri, 
            auth=(user, password),
        )

    def close(self):
        self.driver.close()

    def save_analysis(self, area, greenery, impact):
        with self.driver.session() as session:
            query = """
            MERGE (a:Area {name: $area})
            CREATE (i:Impact {
                greenery: $greenery, 
                description: $impact, 
                timestamp: datetime()
            })
            MERGE (a)-[:HAS_IMPACT]->(i)
            """
            session.run(query, area=area, greenery=greenery, impact=impact)