# Global variables to control max recursion depth.  This is intended to
# limit memory blow-up attacks
MAX_DEPTH=4096
UNLIMITED_DEPTH=False

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
                if (len(left_split[0]) > 0): 
                    ret_val.append(left_split[0])
# Do a right split to see if there's text after the tag.
                right_split = left_split[1].split(">", 1)
# Append the tag to ret_val.
                tag = right_split[0]
                ret_val.append(tag)
# If there's left over text append it.
                if (len(right_split[1]) > 0):
                    ret_val.append(right_split[1])
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