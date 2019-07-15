# commercial_ownership

## Description of the objective

This project is about address data in England

Some addresses need to be modified, i.e divide the addresses to have only one.
The script only modiies addresses with keywords or without keywords but which contains several address numbers.

There are three type of addresses:
- Correct address, ie: 40 Broad Street, Barry (CF62 7AD)
- Address containing keywords (even, odd, inclusive), i.e: 5,24 to 33 (inclusive) Clos Yr Ardd, Cardiff (CF14 6HZ)
- Address without keywords but which must be divided into several addressses, i.e: 36, 36A, 38 and 38A Countisbury Avenue, Cardiff

## Example of address that the script returns:

#### Example: address with inclusive keyword

input: 
5,24 to 33 (inclusive) Clos Yr Ardd, Cardiff (CF14 6HZ)
output: 
5, Clos Yr Ardd, Cardiff (CF14 6HZ)
24, Clos Yr Ardd, Cardiff (CF14 6HZ)
25, Clos Yr Ardd, Cardiff (CF14 6HZ)
26, Clos Yr Ardd, Cardiff (CF14 6HZ)
27, Clos Yr Ardd, Cardiff (CF14 6HZ)
28, Clos Yr Ardd, Cardiff (CF14 6HZ)
29, Clos Yr Ardd, Cardiff (CF14 6HZ)
30, Clos Yr Ardd, Cardiff (CF14 6HZ)
31, Clos Yr Ardd, Cardiff (CF14 6HZ)
32, Clos Yr Ardd, Cardiff (CF14 6HZ)
33, Clos Yr Ardd, Cardiff (CF14 6HZ)

#### Example: address without keyword but need to be divided

input:
36, 36A, 38 and 38A Countisbury Avenue, Cardiff
output:
36, Countisbury Avenue, Cardiff
36A, Countisbury Avenue, Cardiff
38, Countisbury Avenue, Cardiff
38A, Countisbury Avenue, Cardiff

#### Example: More complex address
- 1, 2, 7, 8 and 10 Blackbirds Way, St Mellons, Cardiff (CF3 5RE), 8, 9, 10, 14 and 15 Bluebell Drive, St Mellons, Cardiff (CF3 5RA), 2, 14 and 16 Drawlings Close, St Mellons, Cardiff (CF3 5RB), 1, 2, 4, 6, 8, 10, 11, 12, 13, 14, 16, 17, 18, 20, 22, 24, 25, 26 and 27 Arcon House, Blackbirds Way, St Mellons, Cardiff (CF3 5RF), 13-37 (Odds) St Mellons House, Blackbirds Way, St Mellons, Cardiff (CF3 5RE), 36-45 Avenue House, Bluebell Drive, St Mellons, Cardiff (CF3 5RA), 20-35 Mill House, Bluebell Drive, St Mellons, Cardiff (CF3 5RA), 1-47 (Odds) Elizabeth House, Drawlings Close, St Mellons, Cardiff (CF3 5RB), 1-10 Prince of Wales House, Eastern Close, St Mellons, Cardiff (CF3 5RD), 11-15 Jubilee House, Eastern Close, St Mellons, Cardiff (CF3 5RD) and 16-25 Ty'r Winch House, Eastern Close, St Mellons, Cardiff (CF3 5RD)

- 2 to 6 even numbers and 12 to 26 (even numbers) Sevenoaks Street, 15, 17, 21, 29 to 35 (odd numbers) 38, 42 and 46 (even numbers) 57 to 59 (consecutive numbers) 61 and 73 Oakley Street, 7 to 13 (odd numbers) 16, 19 to 22 (consecutive numbers) 25, 27, 30, 33 and 35 Knole Street, 7, 9, 17, 19, 29to 33 (odd numbers) Holmesdale Street 4 to 12 (even numbers) 13, 14 17 to 20 (consecutive numbers) 22, 38, 46, 47, 49, 50, 52, 55 to 57 (Consecutive numbers) 59 to 65 consecutive numbers) 67 to 71 (consecutive numbers) 73 and 75 Hewell Street, Grange Town, Cardiff
