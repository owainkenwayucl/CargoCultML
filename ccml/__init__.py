# Global variables to control max recursion depth.  This is intended to
# limit memory blow-up attacks
MAX_DEPTH=4096
UNLIMITED_DEPTH=False
TAG_NAME="CCML_TAG_NAME"
CONTENTS_NAME="CCML_TAG_CONTENTS"

# Check to see if current depth is OK.
def depth_ok(depth): 
    return (UNLIMITED_DEPTH or (MAX_DEPTH >= depth))

# Grab the next tag from a string and return:
# [text before tag, tag, text after tag]
def split_out_tag(s, depth=1):
    ret_val=[]
    if (depth_ok(depth)):
# Check to see if this string contanins a tag:
        if (("<" in s) and (">" in s)):
            if (s.index("<") < s.index(">")):
# If it does do a left split to see if there's text before the tag.
# If there is, append it to ret_val.
                left_split = s.split("<", 1)
                if (len(left_split[0].strip('\n')) > 0): 
                    ret_val.append(left_split[0].strip('\n'))
# Do a right split to see if there's text after the tag.
                right_split = left_split[1].split(">", 1)
# Use close_tag to work out what's inside thet tag.
                tag = process_tag(right_split[0])
                temp = close_tag(tag[TAG_NAME], right_split[1], depth)
                tag[CONTENTS_NAME] = temp[0]
                right_split[1] = temp[1]
# Append the tag to ret_val.
                ret_val.append(tag)
# If there's left over text append it.
                if (len(right_split[1].strip('\n')) > 0):
                    ret_val.append(right_split[1].strip('\n'))
# If there's no tag return a list with just the text as a single item.
            else:
                ret_val.append(s)
        else:
            ret_val.append(s)
# If we've reached max dept don't parse.
    else:
        print("CCML: Not parsing as MAX_DEPTH exceeded.")
        ret_val.append(s)
    return ret_val

# Convert the string representaton of the contents of a tag into a dict
# with:
# TAG_NAME = tag 
# subsequent fields as in the xml
def process_tag(t):
    ret_val = {}
# Default to tag = t (for tags with no fields)
    tag = t
# If it has spaces, it has fields.
    if " " in t:
        tag = t.split(" ", 1)[0]
        rest = t.split(" ",1)[1]
# If there are = there are still fields left to process in the rest.
        while "=" in rest:
            var = rest.split("=", 1)[0].strip()
# if a field name is the same as TAG_NAME/CONTENTS_NAME append a _
            if (var == TAG_NAME):
                var = TAG_NAME + "_"
            if (var == CONTENTS_NAME):
                var = CONTENTS_NAME + "_"
            rest = rest.split("=",1)[1].strip()
# Default to val of var is the rest of the text.
            val = rest
# Check to see if that's not true:
            if (len(val) > 0):
                if (val[0] == "'"):
                    val = rest.split("'",2)[1]
                    rest = rest.split("'",2)[2].strip()
                elif (val[0] == '"'):
                    val = rest.split('"',2)[1]
                    rest = rest.split('"',2)[2].strip()
                elif (" ") in rest:
                    val = rest.split(" ",1)[0]
                    rest = rest.split(" ",1)[1].strip()
            ret_val[var] = val
    ret_val[TAG_NAME] = tag
    return ret_val

# Attempt to generate list for a tage which looks like:
# [contents, rest of text]
# If the next detected tag is not the closing tag split out the tag.
# This ends up being recursive across the two functions.
# This function is a mess because I've had too much coffee and not enough
# thought.
def close_tag(tag, rest, depth):
    ret_val = []
    parts = rest.split("<",1)
    contents = parts[0]
    parts = parts[1].split(">",1)
    remains = ""
    next_tag = ""
    if (len(parts) > 1):
        remains = parts[1]
    next_tag = parts[0]

    if (next_tag != "/" + tag):
        temp = split_out_tag(rest, depth+1)
        contents = temp[:-1]
        remains = temp[-1]
        temp2 = close_tag(tag, remains, depth + 1)
        contents = [contents ,temp2[0]]
        remains = temp2[1]

    ret_val=[contents,remains]

    return ret_val

# The main function for parsing a string.  
# Loop over string running split_out_tag until we run out of string.
def process_ccml(s):
    ret_val = []

    remainder = s

    while (remainder != ""):
        temp = split_out_tag(remainder)
        if len(temp) > 1:
            for a in temp[:-1]:
                ret_val.append(a)
            remainder = temp[-1]
        else:
            ret_val.append(temp)
            remainder = ""
    return ret_val
