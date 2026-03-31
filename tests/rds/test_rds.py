"""
Tests for the Glue ETL transformation output.
Validates schema, transformations, and data quality
of the shop.customer_orders_transformed table.
"""

EXPECTED_COLUMNS = {
    "order_id",
    "customer_id",
    "first_name",
    "last_name",
    "email",
    "country",
    "product",
    "quantity",
    "price",
    "total_amount",
    "order_date",
}


class TestSchema:
    """Verify the transformed table has the correct structure."""

    """Verify that the table exists."""
    def test_table_exists(self, cursor):
        cursor.execute("""
            SELECT EXISTS (
                SELECT 1 FROM information_schema.tables
                WHERE table_schema = 'shop'
                AND table_name = 'customer_orders_transformed'
            );
        """)
        assert cursor.fetchone()[0] is True, "Table shop.customer_orders_transformed does not exist"
        
    """Verify that the transformed table contains exactly the expected columns, with no missing or extra columns."""
    def test_column_names(self, cursor):
        cursor.execute("""
            SELECT column_name
            FROM information_schema.columns
            WHERE table_schema = 'shop'
            AND table_name = 'customer_orders_transformed';
        """)
        actual_columns = {row[0] for row in cursor.fetchall()}
        assert actual_columns == EXPECTED_COLUMNS, (
            f"Column mismatch.\n"
            f"Missing: {EXPECTED_COLUMNS - actual_columns}\n"
            f"Extra: {actual_columns - EXPECTED_COLUMNS}"
        )
    """Verify that the transformed table contains exactly the expected number of columns."""
    def test_column_count(self, cursor):
        cursor.execute("""
            SELECT COUNT(*)
            FROM information_schema.columns
            WHERE table_schema = 'shop'
            AND table_name = 'customer_orders_transformed';
        """)
        assert cursor.fetchone()[0] == 11, "Expected 11 columns"


class TestDataQuality:
    """Verify data quality and row counts."""
    def test_row_count(self, cursor):
        cursor.execute("SELECT COUNT(*) FROM shop.customer_orders_transformed;")
        count = cursor.fetchone()[0]
        assert count == 10, f"Expected 10 rows, got {count}"

    """Verify that the transformed table contains no NULL customer_ids."""
    def test_no_null_customer_ids(self, cursor):
        cursor.execute("""
            SELECT COUNT(*) FROM shop.customer_orders_transformed
            WHERE customer_id IS NULL;
        """)
        assert cursor.fetchone()[0] == 0, "Found NULL customer_ids"

    """Verify that the transformed table contains no NULL order_ids."""
    def test_no_null_order_ids(self, cursor):
        cursor.execute("""
            SELECT COUNT(*) FROM shop.customer_orders_transformed
            WHERE order_id IS NULL;
        """)
        assert cursor.fetchone()[0] == 0, "Found NULL order_ids"


class TestTransformations:
    """Verify that ETL transformations were applied correctly."""
    """Verify that the names are uppercase."""
    def test_names_are_uppercase(self, cursor):
        cursor.execute("""
            SELECT COUNT(*) FROM shop.customer_orders_transformed
            WHERE first_name != UPPER(first_name)
               OR last_name != UPPER(last_name);
        """)
        assert cursor.fetchone()[0] == 0, "Found names that are not uppercase"

    """Verify that the total_amount is calculated correctly."""
    def test_total_amount_calculation(self, cursor):
        cursor.execute("""
            SELECT COUNT(*) FROM shop.customer_orders_transformed
            WHERE ROUND((quantity * price)::numeric, 2) != ROUND(total_amount::numeric, 2);
        """)
        assert cursor.fetchone()[0] == 0, "Found incorrect total_amount calculations"

    """Verify that all customers are joined."""
    def test_all_customers_joined(self, cursor):
        cursor.execute("""
            SELECT DISTINCT customer_id
            FROM shop.customer_orders_transformed
            ORDER BY customer_id;
        """)
        customer_ids = [row[0] for row in cursor.fetchall()]
        assert customer_ids == [1, 2, 3, 4, 5], (
            f"Expected customers 1-5, got {customer_ids}"
        )