import great_expectations as gx

context = gx.get_context(mode="file")

data_source = context.data_sources.add_pandas_filesystem(
    name="customer_data_source",
    base_directory="."
)

data_asset = data_source.add_csv_asset(
    name="customer_data"
)

batch_def = data_asset.add_batch_definition_path(
    name="customer_data_batch",
    path="customer_data.csv"
)

suite = context.suites.add(
    gx.ExpectationSuite(name="customer_data_expectations")
)

print("Setup complete!")
print("Suites:", [s.name for s in context.suites.all()])