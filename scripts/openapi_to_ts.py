from main import app


def generate_ts_types(openapi_json):
    components = openapi_json["components"]["schemas"]
    ts_types = []
    mapping = {
        "string": "string",
        "integer": "number",
        "boolean": "boolean",
    }

    def resolve_ref(ref):
        return ref.split("/")[-1]

    def json_type_to_ts(json_type, prop_details=None):

        if json_type == "array" and prop_details:
            if "items" in prop_details:
                item_type = "any"
                if "type" in prop_details["items"]:
                    item_type = prop_details["items"]["type"]
                    item_type = mapping.get(
                        item_type, item_type
                    )  # Use direct type or map
                if "$ref" in prop_details["items"]:
                    item_type = resolve_ref(prop_details["items"]["$ref"])
                if "anyOf" in prop_details["items"]:
                    item_types = [p.get("type") for p in prop_details["items"]["anyOf"]]
                    item_types = [mapping.get(t, t) for t in item_types]  # Map types
                    item_type = " | ".join(item_types)
                return f"({item_type})[]"
            else:
                return "any[]"

        return mapping.get(json_type, "any")

    for name, schema in components.items():
        if schema.get("type") == "object":
            ts_type = f"export type {name} = {{\n"
            for prop_name, prop_details in schema.get("properties", {}).items():
                is_required = prop_name in schema.get("required", [])
                prop_type = "any"
                if "$ref" in prop_details:
                    prop_type = resolve_ref(prop_details["$ref"])
                elif "anyOf" in prop_details:
                    types = [p.get("type") for p in prop_details["anyOf"]]
                    types = [
                        mapping.get(t, t) for t in types if t is not None
                    ]  # Map and filter None
                    prop_type = " | ".join(types)
                else:
                    prop_type = json_type_to_ts(prop_details.get("type"), prop_details)
                ts_type += f"  {prop_name}{'' if is_required else '?'}: {prop_type};\n"
            ts_type += "};\n"
            ts_types.append(ts_type)
        elif schema.get("type") == "string" and "enum" in schema:
            enum_values = " | ".join([f"'{value}'" for value in schema["enum"]])
            ts_type = f"export type {name} = {enum_values};\n"
            ts_types.append(ts_type)

    return "\n".join(ts_types)


if __name__ == "__main__":
    openapi_json = app.openapi()
    ts_types = generate_ts_types(openapi_json)
    with open("api.d.ts", "w") as f:
        f.write(ts_types)
