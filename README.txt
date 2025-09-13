# ARXML Attribute Handler

A Python command-line tool to **add**, **edit**, or **delete**
attributes in an AUTOSAR ARXML file\
and optionally export the file as JSON.

------------------------------------------------------------------------

## 📦 Requirements

-   Python 3.8+
-   No extra libraries beyond the Python standard library

------------------------------------------------------------------------

## ⚙️ Installation

Clone or copy the project files, then (optional) create a virtual
environment:

``` bash
python -m venv .venv
source .venv/bin/activate   # Linux / macOS
# OR
.venv\Scripts\activate      # Windows
```

------------------------------------------------------------------------

## ▶️ Usage

    python arxml_handler.py <input_file> --action {add|edit|delete} --xpath <XPath> --attr <AttributeName> [--value <AttributeValue>] [--output_arxml <filename>] [--output_json <filename>]

### Arguments

  -----------------------------------------------------------------------
  Argument                         Description
  -------------------------------- --------------------------------------
  `input_file`                     Path to the ARXML file you want to
                                   modify

  `--action`                       What to do: `add`, `edit`, or `delete`

  `--xpath`                        Namespace-aware XPath to target
                                   element (e.g. `.//a:I-SIGNAL-I-PDU`)

  `--attr`                         Attribute name to add/edit/delete

  `--value`                        New value (required for `add` and
                                   `edit`)

  `--output_arxml`                 Optional name for updated ARXML file
                                   (default: `EcuExtract_updated.arxml`)

  `--output_json`                  Optional name for JSON export
                                   (default: `filename_updated.json`)
  -----------------------------------------------------------------------

------------------------------------------------------------------------

## 📝 Examples

### 1. Add a new attribute

``` bash
python arxml_handler.py SOUND_Short_eHorizon_Pdu.arxml   --action add   --xpath ".//a:I-SIGNAL-I-PDU"   --attr Manufacturer   --value Bosch
```

### 2. Edit an existing attribute

``` bash
python arxml_handler.py SOUND_Short_eHorizon_Pdu.arxml   --action edit   --xpath ".//a:I-SIGNAL-I-PDU"   --attr Manufacturer   --value Continental
```

### 3. Delete an attribute

``` bash
python arxml_handler.py SOUND_Short_eHorizon_Pdu.arxml   --action delete   --xpath ".//a:I-SIGNAL-I-PDU"   --attr Manufacturer
```

Each command: \* Updates the ARXML file (default output:
`EcuExtract_updated.arxml`) \* Generates a JSON version of the same data
(default: `filename_updated.json`)
