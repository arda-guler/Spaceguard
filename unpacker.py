def unpack_designation(packed):
    year_prefix = {'I': '18', 'J': '19', 'K': '20'}
    year_prefix_code = packed[0]
    if year_prefix_code in year_prefix:
        year_prefix_value = year_prefix[year_prefix_code]
    else:
        return "Invalid year prefix"

    year_suffix = packed[1:3]
    half_month = packed[3]
    second_letter = packed[6]

    cycle_count_code = packed[4:6]
    if cycle_count_code.isdigit():
        cycle_count_str = cycle_count_code.lstrip("0")
    else:
        cycle_count_fc = cycle_count_code[0]
        cycle_count_sc = cycle_count_code[1]

        if cycle_count_fc.isupper():
            lb = (ord(cycle_count_fc) - ord('A')) * 10 + 99 + 1
        else:
            lb = (ord(cycle_count_fc) - ord('a') + (ord('Z') - ord('A'))) * 10 + 99 + 1 + 10

        cynum = lb + int(cycle_count_sc)
        cycle_count_str = str(cynum)

    unpacked = year_prefix_value + year_suffix + " " + half_month + second_letter
    if cycle_count_str != "0":
        unpacked += cycle_count_str

    return unpacked

# examples from the following url:
# https://www.minorplanetcenter.net/iau/info/PackedDes.html
print(unpack_designation("J95X00A")) # 1995 XA
print(unpack_designation("J95X01L")) # 1995 Xl1
print(unpack_designation("J95F13B")) # 1995 FB13
print(unpack_designation("J98SA8Q")) # 1998 SQ108
print(unpack_designation("J98SC7V")) # 1998 SV127
print(unpack_designation("J98SG2S")) # 1998 SS162
print(unpack_designation("K99AJ3Z")) # 2099 AZ193
print(unpack_designation("K08Aa0A")) # 2008 AA360
print(unpack_designation("K07Tf8A")) # 2007 TA418
