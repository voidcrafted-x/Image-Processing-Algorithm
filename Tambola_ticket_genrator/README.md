# Tambola Ticket Generator

A command-line Python program that generates and prints one Tambola (Housie) ticket.

## Rules Implemented

- Three rows and nine columns
- Exactly five numbers in each row
- At least one and at most three numbers in each column
- Fifteen numbers in total
- Numbers are unique within their column range
- Numbers in each column are sorted from top to bottom

The column ranges are `1-9`, `10-19`, `20-29`, and so on, with the final column using `80-90`.

## Requirements

Python 3. No external packages are required.

## Run

From the repository root:

```bash
python Tambola_ticket_genrator/Tambola_Ticket_Generator.py
```

The program prints a newly generated ticket in the terminal each time it runs.

## Project Structure

```text
Tambola_ticket_genrator/
|-- Tambola_Ticket_Generator.py
`-- README.md
```
