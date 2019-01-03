# Figma Export

Exports components from any Figma document and saves them to files that can be easily imported to other applications.

Can export any Figma document as:

- Image files (```png```, ```jpg```, ```svg```).
- Xcode Asset Catalog (```imageset``` files).
- Iconic font (```otf```, ```ttf```, ```woff```).
- Cooming soon...

## Installation

- Install **Python >=3.7**.

- Mac users must install Certificates for the ssl module (execute command script included in /Applications/Python).

- Install Figma Export package:

```
$ python3 -m pip install --upgrade figma_export
```

- Set an environment variable ```FIGMA_ACCESS_TOKEN``` to your [personal access token](https://www.figma.com/developers/docs#auth).

- (Optional) ```otf```, ```ttf``` and ```woff``` commands require the FontForge command-line interface. Run this command ```$ fontforge -c "print('FontForge is ready')"``` to test FontForge installation on your local machine:


## Usage examples

Export all components as PNG files:

```
$ figma_export png DOCUMENT_ID
```

Export all components as Xcode Asset Catalog:

```
$ figma_export imageset DOCUMENT_ID
```

Export specific components:

```
$ figma_export png DOCUMENT_ID -select "/Document/Page 1"
```

Export components as iconic font:

```
$ figma_export otf DOCUMENT_ID
```

Each font glyph is coded by first char from the name of the corresponding component. 

```DOCUMENT_ID``` - can be parsed from any Figma document url: ```https://www.figma.com/file/DOCUMENT_ID/...```

