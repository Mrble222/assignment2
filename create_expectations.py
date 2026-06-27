import great_expectations as gx

context = gx.get_context(mode="file")

# load suite, datasource and batch
suite = context.suites.get("customer_data_expectations")

data_source = context.data_sources.get("customer_data_source")
data_asset = data_source.get_asset("customer_data")
batch_def = data_asset.get_batch_definition("customer_data_batch")
batch = batch_def.get_batch()


suite.add_expectation(gx.expectations.ExpectColumnValuesToBeUnique(column="customer_id"))
suite.add_expectation(gx.expectations.ExpectColumnValuesToNotBeNull(column="customer_id"))

suite.add_expectation(gx.expectations.ExpectColumnValuesToBeBetween(column="age", min_value=0, max_value=120))

suite.add_expectation(gx.expectations.ExpectColumnValuesToMatchRegex(
    column="email",
    regex=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
))

suite.add_expectation(gx.expectations.ExpectColumnValuesToNotBeNull(column="salary", mostly=0.95))

suite.add_expectation(gx.expectations.ExpectColumnValuesToBeInSet(
    column="country",
    value_set=["USA", "Canada", "UK", "Australia"]
))

suite.add_expectation(gx.expectations.ExpectColumnValuesToMatchRegex(
    column="signup_date",
    regex=r"^\d{4}-\d{2}-\d{2}.*$"
))

suite.add_expectation(gx.expectations.ExpectTableRowCountToBeBetween(min_value=500, max_value=1000))

suite.save()
print("expectations created and saved!")