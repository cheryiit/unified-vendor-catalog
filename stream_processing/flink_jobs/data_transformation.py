from pyflink.datastream import StreamExecutionEnvironment
from pyflink.table import StreamTableEnvironment, DataTypes
from pyflink.table.udf import udf
from pyflink.table.descriptors import Json, Kafka, Schema

def product_processor():
    env = StreamExecutionEnvironment.get_execution_environment()
    t_env = StreamTableEnvironment.create(env)

    # Kafka kaynak tablosunu oluştur
    t_env.connect(Kafka()
        .version("universal")
        .topic("product_updates")
        .start_from_earliest()
        .property("zookeeper.connect", "localhost:2181")
        .property("bootstrap.servers", "localhost:9092")
        .property("group.id", "product_processor")
    ).with_format(Json()
        .fail_on_missing_field(True)
        .schema(DataTypes.ROW([
            DataTypes.FIELD("id", DataTypes.INT()),
            DataTypes.FIELD("name", DataTypes.STRING()),
            DataTypes.FIELD("description", DataTypes.STRING()),
            DataTypes.FIELD("price", DataTypes.DOUBLE())
        ]))
    ).with_schema(Schema()
        .field("id", DataTypes.INT())
        .field("name", DataTypes.STRING())
        .field("description", DataTypes.STRING())
        .field("price", DataTypes.DOUBLE())
    ).create_temporary_table("product_source")

    # Veri işleme
    result = t_env.sql_query("""
        SELECT 
            id,
            name,
            description,
            price,
            CASE 
                WHEN price < 50 THEN 'Low'
                WHEN price >= 50 AND price < 100 THEN 'Medium'
                ELSE 'High'
            END AS price_category
        FROM product_source
    """)

    # SQLite hedef tablosunu oluştur
    t_env.connect(JdbcCatalog()
        .name("sqlite_catalog")
        .default_database("main")
        .url("jdbc:sqlite:/path/to/your/sqlite/database.db")
        .driver("org.sqlite.JDBC")
    )

    # Sonuçları SQLite'a yaz
    result.execute_insert("sqlite_catalog.main.products")

if __name__ == "__main__":
    product_processor()