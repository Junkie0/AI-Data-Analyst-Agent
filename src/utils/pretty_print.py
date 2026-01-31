def print_schema(schema: dict) -> None:
    print("\n" + "=" * 30)
    print("Dataset Overview")
    print("=" * 30)

    print(f"Rows : {schema['rows']}")
    print(f"Columns : {schema['columns']}")
    print(f"Memory : {schema['memory_usage_kb']}")

    print("\n" + "-" * 30)
    print("Column Details")
    print("-" * 30)

    for col, info in schema["columns_detail"].items():
        print(f"\n🔹 {col}")
        print(f" Type : {info['dtype']}")
        print(f" Non-null : {info['non_null_count']}")
        print(f" Null : {info['null_count']}")
        print(f" Unique Values : {info['unique_values']}")