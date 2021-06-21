# Simple Benford's Law Checker

A simple web app for checking if the numbers in specified column in user submitted delimited text file are following the Benford's Law. This is a play project, created for the purpose of learning Python library Flask, Java Script framework Vue3 and some basic web-dev concepts.

## Current state

For now, the app can draw the bar plot of distribution of first significant digits and present the results of Chi-squared Goodness of Fit Test. It handles only upload form related errors, does not handel the errors emerging from the contents of an analyzed file yet.

## Getting Started

Required: **docker-compose** and **npm**

To run the app you need to:

1. clone the repository
2. checkout to this branch
3. run the following commands from the top directory of cloned repository:

   ```
   docker-compose up -d
   ```

   if you want to see logs, you can run:

   ```
   docker-compode logs -f
   ```

4. open new terminal and run:

   ```
   cd client
   npm run serve
   ```

5. open http://127.0.0.1:8080/ in your browser.

## Examples

### The Brightest Stars

Let's check whether the distance of the 300 brightest stars from Earth (in light years) follows the Beanford's Law.

1. Download the data.

   There are TSV and CSV files in the test directory containing relevant data:

   - https://github.com/lltw/simple-blc/blob/main/tests/test_flat_files/300_brightest_stars.tsv
   - https://github.com/lltw/simple-blc/blob/main/tests/test_flat_files/300_brightest_stars.csv

   Download one of them. The source of the data is http://www.atlasoftheuniverse.com/stars.html.

2. Start the app following the intructions above (**Getting started**) and go to http://127.0.0.1:8080/ in your browser.
3. Upload the file:
   - select the downloaded file
   - set column number to 13
   - set delimiter to comma or tab (depending on which file you downloaded)
   - set the header presence field to 'yes'
   - click 'Submit'!

If you are curious what else to check, the 11th column - The Hipparcos parallax of the star - is a good pick.
For more info go to http://www.atlasoftheuniverse.com/stars.html or see the info file:

- https://github.com/lltw/simple-blc/blob/main/tests/test_flat_files/300_brightest_stars.info
