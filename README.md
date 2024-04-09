## Project Summary

This project features the creation of a simple database query system that interprets a subset of SQL commands and manipulates student records stored in a CSV file named "students.csv". The initial step involves loading the CSV file and sorting the records by index. The system accepts and processes queries in a simplified SQL format, allowing for the selection, insertion, deletion of records, and sorting the results. The valid query operations include comparisons and logical connectors with a limitation of using at most two conditions combined with AND or OR. The processed query results are then output as a JSON file.

The implementation of this system is in Python, with the use of libraries covered in the course for reading CSV and writing JSON files. Query parsing is to be handled without the aid of specialized libraries for this purpose. The code will be contained in a single `.py` file.

Queries are case-insensitive and the system waits for user input, continuing to process new queries or exiting upon the 'exit' command. The project emphasizes the importance of proper coding practices including inline comments, and the student information is expected to be included in the comments at the beginning of the code. All queries that do not conform to the specified format will raise an error.

This system is designed as an educational tool to demonstrate basic database operations through a user-friendly command-line interface, while also reinforcing best coding practices.
