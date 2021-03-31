# Simple Benford's Law Checker

This is a simple python-based web application for checking if the numbers in specified column in user submitted file are following the Benford's Law. 

# Current state
This is a very first draft. The app has limited functionality - for now it only draws a bar plot of distribution of first significant digits in user submitted data vs. distribution of fist first significant according to Benford's Law. It doesn't have any automated testing nor config other than development config yet. 

## Getting Started

In order to tun the app you need to build a Docker image
```
docker build --tag simple-blc .
```
run it
```
docker run --publish 5000:5000 simple-blc
```

and open http://127.0.0.1:5000/ in your browser.

## Examples

### The Brightest Stars

Let's check whether the distance of the 300 brightest stars from Earth (in light years) follows the Beanford's Law.

1. Download the data. 
   
   There are TSV and CSV files in the test directory containing relevant data:
    + https://github.com/lltw/simple-blc/blob/main/tests/test_flat_files/300_brightest_stars.tsv
    + https://github.com/lltw/simple-blc/blob/main/tests/test_flat_files/300_brightest_stars.csv
    
   Download one of them. The source of the data is http://www.atlasoftheuniverse.com/stars.html. 
   
2. Run the docker image and go to http://127.0.0.1:5000/ in your browser.
3. Upload the file:
   + select the downloaded file
   + set column number to 13
   + set delimiter to comma or tab (depending on which file you downloaded)
   + set the header presence field to 'yes'
   + click 'Submit'!
    
If you are curious what else to check, the 11th column - The Hipparcos parallax of the star - is a good pick. 
For more info go to http://www.atlasoftheuniverse.com/stars.html or see the info file:
 + https://github.com/lltw/simple-blc/blob/main/tests/test_flat_files/300_brightest_stars.info





