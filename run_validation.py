import great_expectations as gx

context = gx.get_context(mode="file")

suite = context.suites.get("customer_data_expectations")
data_source = context.data_sources.get("customer_data_source")
data_asset = data_source.get_asset("customer_data")
batch_def = data_asset.get_batch_definition("customer_data_batch")

validation_def = context.validation_definitions.get("customer_data_validation")

results = validation_def.run()

print("\n===== VALIDATION RESULTS =====")
print(f"Overall Success: {results.success}\n")

for result in results.results:
    status = "PASSED" if result.success else "FAILED"
    config = result.expectation_config
    kwargs = config.kwargs if hasattr(config, "kwargs") else {}
    column = kwargs.get("column", "TABLE-LEVEL")
    expectation = config.type

    print(f"{status} | {expectation} | Column: {column}")

    # Print failure details
    if not result.success:
        stats = result.result
        if "unexpected_count" in stats:
            print(f"         → Unexpected (failing) rows: {stats['unexpected_count']}")
            print(f"         → Unexpected percent: {stats.get('unexpected_percent', 'N/A'):.2f}%")
        if "observed_value" in stats:
            print(f"         → Observed value: {stats['observed_value']}")

# Build HTML docs
context.build_data_docs()