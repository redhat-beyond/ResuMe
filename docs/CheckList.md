# Commit check list
## Coding Conventions 
### Django app
- [ ] An app's name should be short, all-lowercase and not include numbers, dashes, periods, spaces, or special characters. It also, in general, should be the plural of an app's main model, so our  `posts`  app would have a main model called  `Post`.
### Files(Modules)
- [ ] Modules should have short, all-lowercase names. Underscores can be used in the module name if it improves readability(E.g `test_model.py`)
- [ ] Imports are always put at the top of the file.
- [ ] Imports form the same module should be separated with ' , ' (E.g `from secondery_model import item1, item 2`).
### Models(Classes)
 - [ ] Models name should be in CapWords(E.g `MyModel` )
 - [ ] **Be careful not to choose a similar name to Django's default models names like `User`**
 - [ ] **Variables** and **functions** names should be lowercase, with words separated by underscores(i.e `first_name` and `calc_average`)
 - [ ] functions names should be significant.
 - [ ] Instance methods should always receive `self` as first argument
 - [ ] Class methods should always receive `cls` as first argument
 - [ ] Constants should be defined in the module level and be written in capital letters with underscores separating words(E.g `MAX_LENGTH`)
 - [ ] Strings should be consistent when using quotes. Use quote or double quote, not both.
### Blank lines
- [ ]  Surround top-level function and class definitions with two blank lines.
- [ ] Method definitions inside a class are surrounded by a single blank line.
### Tests
- [ ] Above each test should have a comment that describes what the test is meant for.
- [ ] If the test expect `Exception` use `pytest.rise`
- [ ] To test several invalid value test cases use `parametrize`.
## Run Pytest and flake8 
Inside the vagrant Virtual machine and inside the `/vagrant` folder
- [ ] pipenv run python -m pytest -v
- [ ] pipenv run flake8 --max-line-length 120