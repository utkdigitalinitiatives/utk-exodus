# UTK Exodus :flight_departure:

## About

This application is a complete rewrite of the code used to migrate UTK content from Islandora 7 to Hyku.

Unlike the previous code, this aims to be more flexible, easier to understand, and easier to use as a whole.

## Installing

To install, simply:

```shell
pip install utk_exodus
```

## Using

There are several interfaces for the application.

If you want to get works and files, use:

```shell
exodus works_and_files --path /path/to/metadata -o /path/to/directory/to/store/files
```

If you just want works, use:

```shell
exodus works --path /path/to/metadata
```

If for some reason you need to create a files sheet for  works after the fact, use:

```shell
exodus add_files --sheet path/to/sheet.csv --files_sheet path/to/files_sheet.csv 
```


## Understanding Configs

Exodus uses `yml` files for migration.  By default, exodus treats everything agnostically and relies on the `xpaths` 
section of the base mapping to determine how a concept is mapped. If a property (or properties) have complex rules, a 
class can be written to handle the special case.  When this happens, the `yml` should have a `special` property, and 
it should be defined in `MetadataMapping().__lookup_special_property()`.

An agnostic property should look like this in the `yml`:

```yml
  - name: table_of_contents
    xpaths:
      - 'mods:tableOfContents'
    property: "http://purl.org/dc/terms/tableOfContents"
```

A complex property might look like this:

```yml
  - name: title_and_alternative_title
    xpaths:
      - 'mods:titleInfo[not(@supplied)]/mods:title'
      - 'mods:titleInfo[@supplied="yes"]/mods:title'
    properties:
      - "http://purl.org/dc/terms/title"
      - "http://purl.org/dc/terms/alternative"
    special: "TitleProperty"
```

An agnostic property must always have the `property` property while a complex property may have `property` or 
`properties`.
