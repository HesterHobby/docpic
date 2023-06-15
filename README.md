# docpic

A selenium framework for adding screenshots to documentation.

## What is it?

docpic is a lightweight markdown processor for adding screenshots of web apps to your markdown documentation.

## Why do I want it?

If you are maintaining markdown documentation alongside your web app, docpic will ensure the screenshots 
of different parts or states of the app are up to date, 
removing the overhead of having to manually update screenshots for every change in your app.  

## How does it work?

docpic uses simple YAML configuration to drive a series of selenium steps to get the web app into the 
desired state, and then takes a screenshot that is saved to a location specified in the config.
The config is added between [docpic]..[/docpic] tags in your markdown documents. 

After the screenshot is taken, docpic either saves a changed markdown file with the image embedded to a 
new location, or overwrites the existing YAML section with a markdown link to the image.

## How do I call it?

docpic can be run in two ways:
* From within the IDE it can be run through `main.py`. An example is set up that should run on all platforms.
* From the command line docpic can be run using `python docpic.py --infile [input_file] --outfile [output_file] 
--img-dir [output_folder]`. For example, the following will run docpic on the included example yaml file and
save the output into a folder called "assets": `python docpic.py --infile concept_md_config.md --img-dir assets/`.
If no output name is specified and the optional `--overwrite-existing` flag is not set, like in this example, the output 
markdown file will be saved in the format `[input_name].generated.[YYMMDD_hhmm].md` using the system date.

## YAML structure

WIP, trying to make this look nice / useful. The raw schema is in `yaml_validator.py`. 

## Command line options
* `--infile`: Required. The location of your infile, relative to the current folder.
* `--outfile`: Optional. Output file, relative to the current folder. If not specified, 
`[input_name].generated.[YYMMDD_hhmm].md` will be used.
* `--img-dir`: Optional. Output folder, relative to the current folder. Defaults to `assets`.
* `--overwrite-existing`: Optional flag. When specified, this overwrites the `[docpic]..[/docpic]` 
sections in your input file.