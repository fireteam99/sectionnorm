# Section Normalization

## Problem Statement

SeatGeek is a marketplace for tickets to live events. We aggregate listings from a number of different sellers and allow our customers to comparison shop.

One of the subtle challenges with this business concerns labeling in structured data. Suppose you have three sellers, who each have two tickets for sale for an upcoming Mets game.

One of them sends us this document:

```
quantity: 2,
price: 50,
section: "133",
row: "C"
```

One of them sends us this:

```
quantity: 4
price: 55
section: "S133",
row : "f"
```

And one of them sends us this:

```
quantity: 1,
price: 45,
section: "Field Level 133",
row: "Row C"
```

The challenge lies in deciphering which of these listings are the same, and where should we draw them on our [seating charts](http://cl.ly/1Z0j2L1k3N2G).

We call this problem "Section Normalization." The goal is to "normalize" the naming conventions applied by the various sellers and map the listings to a *canonical* list of sections and rows that we know to actually exist in the stadium. The canonical list is typically called a *manifest*. The challenge is that the sellers don't know about our manifest; they just type descriptions of the ticket into a text field somewhere and we have to use rules and heuristics to normalize their descriptions on our end.

An additional wrinkle comes from the fact that we can't trust brokers to be accurate. You might notice, from looking at the screenshot, that there *is not* a row 'f' in section 133 at Citi Field. When we see listings that don't map to a section/row in the manifest, we generally hide it by marking it as 'invalid'.

## Your Task

Your task is to implement a section normalizer that works on two venues with a high degree of accuracy. You will do this by implementing two stub methods in the provided file (Python: [`normalizer.py`](python/normalization/normalizer.py), Java: [`Normalizer.java`](java/src/main/java/Normalizer.java), Ruby: [`normalizer.rb`](ruby/normalizer.rb), PHP: [`normalizer.php`](php/normalizer.php), C#: [`Normalizer.cs`](csharp/src/Normalizer.cs)). Additional detail is provided below about the implementation.

You will also be asked to submit a short (maybe 2 paragraph) README detailing your approach.

## Manifest Data

You are provided with two example "manifest" files, one for Citi Field (home of the New York Mets) and one for Dodger Stadium (home of the Los Angeles Dodgers). These examples are available in [`manifests/`](manifests).

The sample file format is excerpted below.

| section_id | section_name     | row_id | row_name |
|------------|------------------|--------|----------|
| 1          | 133              | 0      | A        |
| 1          | 133              | 2      | C        |
| 1          | 133              | 1      | B        |
| 1          | 133              | 4      | E        |
| 1          | 133              | 3      | D        |
| 215        | 432              | 0      | 1        |
| 215        | 432              | 2      | 3        |
| 215        | 432              | 1      | 2        |
| 215        | 432              | 4      | 5        |
| 215        | 432              | 3      | 4        |
| 216        | Empire Suite 241 |        |          |

As you can see, each distinct section has an identifier `section_id`; what we'd like to do is match a listing to a `(section_id, row_id)` so we can render it on our map, or decide whether the listing is 'garbage' and hide it from our customers.

**Notes:**

* `section_id` is unique within a stadium.
* `section_id`'s start at 1.
* `row_id` is unique within a section.
* `row_id`'s are actually ordinal and start at 0, meaning row_id 0 is "closer to the front" than `row_id` 1.
* Some sections may have numerical row names (1-10) and some may have alphanumeric row names (A-Z, AA-DD). Your code should support both.
* Some sections are not subdivided into rows. For example, Empire Suite 241 in the above example has no row information. This is represented in the manifest as a single row with null `row_id`/`row_name`.
    * If someone were to buy this ticket it would just be to "the suite" and there would be no row information on the ticket.

## Training Data

You are provided with two input datasets. Each dataset is a CSV file with the following format:

| section           | row | n_section_id | n_row_id | valid |
|-------------------|-----|--------------|----------|-------|
| Section 432       | 1   | 215          | 0        | TRUE  |
| Section 432       | 2   | 215          | 1        | TRUE  |
| Section 432       | 99  | 215          |          | FALSE |
| Promenade Box 432 | 1   | 215          | 0        | TRUE  |
| sdlkjsdflksjdf    | 1   |              |          | FALSE |
| 432               | 1-5 | 215          |          | FALSE |

Each row contains an input section and row, as well as the 'true' normalized section/row id from the manifest. You can use this to test your implementation, to ensure that your normalization strategy is coming up with the right answers. The sample data sets can be found in [`samples/`](samples).

**Notes:**

* A normalization is considered `VALID` if it can be matched to exactly one section/row combination in the stadium. In this case, we would render the ticket confidently on SeatGeek.
* If the section matches correctly but the row appears to not exist, the `row_id` should be left blank and normalization is considered `INVALID` (except for in the case of suite sections, where this is okay).
* If the section does not match, both `section_id` and `row_id` should be left blank, and normalization is considered `INVALID`.
* Sometimes sellers will attempt to pass a 'range' in the row field, as in (this is somewhere in rows 1-5). In this case, the `row_id` should be left blank and the normalization should be considered `INVALID`.

## Implementing Your Code

For the moment, this test must be solved in one of the following languages:

* Python 3
* Java
* Ruby
* PHP
* C#

The grading script is written in python, and if you'd like to use it during development (this is optional, but suggested) you will need to have python available.

### Instructions For All Languages

Find the starter files for your language of choice. Your task is to implement two stub methods, `read_manifest(self, path)` and `normalize(self, section, row)` (with slight variations depending on language of choice).

Your code will be graded by a python script that has been provided to you. It can be called as follows:

```bash
python genericgrader.py --manifest /path/to/manifest.csv --input /path/to/input.csv --lang [python|ruby|java|php|csharp]
> ...
```

For example:

```bash
python genericgrader.py --manifest manifests/citifield_sections.csv --input samples/metstest.csv --lang python
```

You may create additional modules, packages, classes etc within the project structure as you wish; however, the grading script must run as specified.

Starter files can be found in either [`/python`](python), [`/ruby`](ruby), [`/java`](java), [`/php`](php), or [`/csharp`](csharp). Each directory should have a bash script called `normalize` that will be run by the grading script.

The following command can be used to run the full script; the output should be json documents, one per line, that will be consumed by the grader script.

```bash
./normalize --manifest ../manifests/citifield_sections.csv --input ../samples/metstest.csv
```

The following command can be used to test a single section/row pair on the command line. Note that Java, C#, and Ruby have a different command. See below for details.

```bash
./normalize --manifest ../manifests/citifield_sections.csv --input ../samples/metstest.csv --section 101 --row a
```

For Java, C#, and Ruby, please use the following command for a single section/row pair:
```bash
./normalize --manifest ../manifests/citifield_sections.csv --section 101 --row a
```

**Note:** We strongly encourage you to use whatever testing methodology you would typically use for this type of project instead of or in addition to the provided script.

#### Python-Specific Instructions

For this test, you must use python 3. We recommend python 3.8, specifically.

Please limit yourself to the python standard library.

You may create additional modules or packages within the project structure if you wish; as long as the provided grading script (see below) runs as specified.

Your code will be executed by a bash script at [`python/normalize`](python/normalize).

#### Ruby-Specific Instructions

Please limit yourself to the ruby standard library.

You may create additional modules or packages within the project structure if you wish; as long as the provided grading script (see below) runs as specified.

#### Java-Specific Instructions

The Java project uses gradle to build so any ide that supports gradle projects can be used to work on the solution with a little bit of configuration to reference the input files correctly. If you prefer a text editor, you can go that route as well, the source 
root is [`java/src/main/java`](java/src/main/java).

The starter files contain two external dependencies: `argparse4j` and `gson`, already configured in the `build.gradle`.  If you must pull in any additional dependencies, please modify the `build.gradle` and ensure that your code compiles correctly by running the `normalize` script.

Your code will be tested using a Java 11 runtime.

#### PHP-Specific Instructions

Please limit yourself to the standard php library.

You may create additional modules or packages within the project structure if you wish; as long as the provided grading script (see below) runs as specified.

#### C#-Specific Instructions

Please limit yourself to the C# standard library.

You may create additional modules or packages within the project structure if you wish; as long as the provided grading script (see below) runs as specified. 

## Grading

Our automatic grader works as follows:

1. We will attempt to normalize 1000 tickets using your script. Some of these records are *normalizable* and some of them are *not normalizable*. In other words, in some cases the correct answer is a section/row, and in others the correct answer is `INVALID`.

2. Scoring:

    Correct normalization for normalizable ticket = 1 point
    Invalid normalization for normalizable ticket = 0 points
    Wrong normalization for normalizable ticket = -5 points

    Correct non-normalization for non-normalizable ticket = 1 point
    Wrong normalization for non-normalizable ticket = -5 points

    In other words, it is better to be safe than sorry.

**Additional Note:** We will use a **DIFFERENT** input file than the ones provided to you as training data. This is to ensure that you do not overfit or otherwise 'hack' the program to operation. However you can assume that the inputs are substantially similar to the ones provided to you as a sample.

## README / Code Review

In addition to seeing whether you solved the problem (and how accurately you normalized the listings), we're very interested to see *how* you attempted to solve it, and what kind of decomposition and code organization you used to implement the solution. On the first point, please submit a short (maybe 2 paragraph) README detailing your approach. Note that there are many different possibilities, and there are no bonus points for *complexity for its own sake*.

We are also interested in how you write, organize, and structure your code. You don't have to spend hours formatting and commenting your code as though it is going to be published in a book, but please at least try to make your code clear, concise, and easy for our engineers to understand.

## A Note On Correctness

The training and test sets for this code test were generated using SeatGeek's own normalization algorithm and live data. However, this problem is just as hard for us as it is for you. That means it's entirely possible (if not probable) that there are small issues with the training set.

If you notice any egregious errors, feel free to bring them to our attention, but in general if you find yourself annoyed that one or two cases don't seem to make any sense, feel free to chalk it up to a bug in our own implementation of this "test" and move on with your life. We are much more interested in your overall approach to the problem than whether you managed to find every bug and edge case.


## Submitting Your Solution

Please package everything in the [`/sectionnorm`](.) directory, including your additional code and solution readme. When you're satisfied with your solution, you can submit it to our team via the Greenhouse link. We are simply going to unzip your solution and then run the grader over it, so make sure that the ZIP file contains everything that your code needs to run, import statements are correctly defined, etc.

Good luck! 💫
