import argparse
import xml.etree.ElementTree as ET
import json
import os
import sys


class ARXMLHandler:
    def __init__(self, input_file_path: str):
        if not os.path.exists(input_file_path):
            raise FileNotFoundError(f"Input ARXML file not found: {input_file_path}")

        try:
            self.arxml_tree = ET.parse(input_file_path)
            self.arxml_root = self.arxml_tree.getroot()
            self.autosar_namespace = {"a": "http://autosar.org/schema/r4.0"}
        except ET.ParseError as parse_error:
            raise ValueError(f"Error parsing ARXML file: {parse_error}")

    def find_element(self, xpath_expression: str):
        """Find first element matching XPath (namespace-aware)."""
        return self.arxml_root.find(xpath_expression, self.autosar_namespace)

    def add_attribute(
        self, xpath_expression: str, attribute_name: str, attribute_value: str
    ):
        element = self.find_element(xpath_expression)
        if element is None:
            raise ValueError(f"Element not found for XPath: {xpath_expression}")
        element.set(attribute_name, attribute_value)

    def edit_attribute(
        self, xpath_expression: str, attribute_name: str, new_value: str
    ):
        element = self.find_element(xpath_expression)
        if element is None:
            raise ValueError(f"Element not found for XPath: {xpath_expression}")
        if attribute_name not in element.attrib:
            raise ValueError(
                f"Attribute '{attribute_name}' not found in element {xpath_expression}"
            )
        element.set(attribute_name, new_value)

    def delete_attribute(self, xpath_expression: str, attribute_name: str):
        element = self.find_element(xpath_expression)
        if element is None:
            raise ValueError(f"Element not found for XPath: {xpath_expression}")
        if attribute_name not in element.attrib:
            raise ValueError(
                f"Attribute '{attribute_name}' not found in element {xpath_expression}"
            )
        del element.attrib[attribute_name]

    def save_arxml(self, output_file_path: str):
        self.arxml_tree.write(output_file_path, encoding="utf-8", xml_declaration=True)

    def export_to_json(self, output_file_path: str):
        def element_to_dict(element):
            element_dict = {}
            element_dict.update(element.attrib)
            for child in element:
                element_dict[child.tag.split("}")[-1]] = element_to_dict(child)
            if element.text and element.text.strip():
                element_dict["text"] = element.text.strip()
            return element_dict

        json_data = {
            self.arxml_root.tag.split("}")[-1]: element_to_dict(self.arxml_root)
        }

        with open(output_file_path, "w", encoding="utf-8") as json_file:
            json.dump(json_data, json_file, indent=4, ensure_ascii=False)


def main():
    parser = argparse.ArgumentParser(description="ARXML Attribute Handler")
    parser.add_argument("input", help="Input ARXML file path")
    parser.add_argument(
        "--action",
        choices=["add", "edit", "delete"],
        required=True,
        help="Action to perform",
    )
    parser.add_argument(
        "--xpath", required=True, help="XPath to element (e.g. .//a:I-SIGNAL-I-PDU)"
    )
    parser.add_argument("--attr", required=True, help="Attribute name")
    parser.add_argument("--value", help="Attribute value (required for add/edit)")
    parser.add_argument(
        "--output_arxml",
        default="SOUND_Short_eHorizon_Pdu_updated.arxml",
        help="Output ARXML filename",
    )
    parser.add_argument(
        "--output_json",
        default="SOUND_Short_eHorizon_Pdu.json",
        help="Output JSON filename",
    )

    args = parser.parse_args()

    try:
        # ---- Centralized validation ----
        if args.action in ("add", "edit") and not args.value:
            raise ValueError(f"{args.action.capitalize()} action requires --value")

        if not args.attr:
            raise ValueError("--attr is required for all actions")

        handler = ARXMLHandler(args.input)

        # ---- Perform the requested action ----
        if args.action == "add":
            handler.add_attribute(args.xpath, args.attr, args.value)
        elif args.action == "edit":
            handler.edit_attribute(args.xpath, args.attr, args.value)
        elif args.action == "delete":
            handler.delete_attribute(args.xpath, args.attr)

        handler.save_arxml(args.output_arxml)
        handler.export_to_json(args.output_json)
        print(
            f"Done! ARXML saved to {args.output_arxml}, JSON saved to {args.output_json}"
        )

    except Exception as error:
        print(f"Error: {error}")
        sys.exit(1)


if __name__ == "__main__":
    main()
