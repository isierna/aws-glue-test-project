EXPECTED_COLUMNS = {
    "order_id", "customer_id", "first_name", "last_name",
    "email", "country", "product", "quantity", "price",
    "total_amount", "order_date"
}

class TestSchema:
    def test_column_names(self, df):
        assert set(df.columns) == EXPECTED_COLUMNS

    def test_column_count(self, df):
        assert len(df.columns) == 11

class TestDataQuality:
    def test_row_count(self, df):
        assert len(df) == 10

    def test_no_null_customer_ids(self, df):
        assert df["customer_id"].isnull().sum() == 0

    def test_no_null_order_ids(self, df):
        assert df["order_id"].isnull().sum() == 0

class TestTransformations:
    def test_names_are_uppercase(self, df):
        assert (df["first_name"] == df["first_name"].str.upper()).all()
        assert (df["last_name"] == df["last_name"].str.upper()).all()

    def test_total_amount_calculation(self, df):
        expected = (df["quantity"] * df["price"]).round(2)
        assert (df["total_amount"].round(2) == expected).all()

    def test_all_customers_joined(self, df):
        customer_ids = sorted(df["customer_id"].unique().tolist())
        expected = ['C001', 'C002', 'C003', 'C004', 'C005', 'C006', 'C007', 'C008']
        assert set(customer_ids) == set(expected)