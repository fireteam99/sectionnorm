# Code Review
## Structure
### General
The majority of the source code resides within the Normalizer class as methods. There are also a few util functions for string manipulation defined at the module level. 
### Storing Manifest
The method `read_manifest` reads in the manifest csv file and stores it in an instance variable `manifest_dict` as a dictionary. The key in the dictionary is the `section_name` and the value is another dictionary called section data`. Section data contains the corresponding section id as well as a dictionary that contains all of the rows belonging to the section. The keys in the rows dictionary are the normalized row names, and the values are the row ids.
## Normalization
### Section
Normalizing sections was the more challenging when compared to normalizing rows. My approach relied on extracting various features out of a section name such as the preceding words, prefix, digits, suffix, and following words, to determine if two section names are actually describing the same section - just in a different format.
### Row
Being that the majority of the rows followed the format of either being numeric `1-10` or alphanumeric `A-Z, ZZ-DD`, it was simpler to just normalize the manifest row name to a standard form and store it as the  key. To check to see if a row exists, the pass row name is normalized the same way, and checked against the rows dictionary.
## Performance
My normalizer works fairly well with the Mets and Dodgers test cases, but struggles with the Red sox test cases. In particular my implementation struggles when there are multiple differences between two corresponding sections. One example would be the insertion of completely different words and/or differences in formatting: `Infield Grandstand 33` should equal `Outfield Grandstand GS33`. Unfortunately, I was unable to find a way to reduce these false negatives without also increasing the number of false positives.

## Testing
I followed a test driven development approach for my solution. This helped me identify and fix errors efficiently, and gave me insight on adjustments to my code increased or decreased accuracy. The unit tests are found in `python/normalization/test.py`.