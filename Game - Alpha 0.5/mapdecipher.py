""" mapfile decipherer """

## the purpose of this will be to take a tilemap that has not been split into
## an array and turn it into one.

def decipher(original, width, height):
    index_width     = 0
    index_height    = 0
    output          = []
    row             = []
    index_original  = 0
    while index_height < height:
        while index_width < width:
            row.append(original[index_original])
            index_width += 1
            index_original += 1
        output.append(row)
        row = []
        index_width = 0
        index_height +=1
    return output

map1 = [489,489,489,489,489,489,489,489,489,489,489,489,489,489,489,489,489,489,489,489,489,489,489,489,489,489,489,489,489,489,489,489,489,489,489,489,489,489,489,489,489,489,489,489,489,489,489,489,489,489,489,489,489,489,489,489,489,489,489,489,
489,489,489,489,489,489,489,489,489,489,489,489,489,489,489,489,489,489,489,489,489,489,489,489,489,489,489,489,489,489,489,489,489,489,489,489,489,489,489,489,489,489,489,489,489,489,489,489,489,489,489,489,489,489,489,489,489,489,489,489,
489,489,371,422,422,422,422,422,422,422,422,422,422,422,422,422,422,422,422,422,422,422,422,422,422,422,422,422,422,422,422,422,422,422,422,422,422,422,422,422,422,422,422,422,422,422,422,422,422,422,422,422,422,422,422,422,422,372,489,489,
489,489,400,487,487,487,487,487,487,487,487,487,487,487,487,487,487,487,487,487,487,487,487,487,487,487,487,487,487,487,487,487,487,487,487,487,487,487,487,487,487,487,487,487,487,487,487,487,487,487,487,487,487,487,487,487,487,398,489,489,
489,489,400,487,444,445,445,445,445,445,445,445,445,445,445,445,445,445,445,445,445,445,445,445,445,445,445,445,445,445,445,445,445,445,445,445,445,445,445,445,445,445,445,445,445,445,445,445,445,445,445,445,445,445,445,446,487,398,489,489,
489,489,400,487,604,166,309,143,143,143,143,143,143,143,192,192,192,192,287,192,192,192,192,192,192,192,192,192,192,192,192,192,192,192,192,192,192,192,192,192,192,192,192,192,192,192,192,192,192,192,192,192,192,193,124,533,487,398,489,489,
489,489,400,487,536,48,328,166,166,166,166,166,166,167,48,48,48,48,144,48,48,48,48,48,48,48,31,57,57,57,57,57,57,57,57,57,57,33,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,142,147,469,487,398,489,489,
489,489,400,487,536,48,188,48,48,48,48,48,48,48,48,48,48,48,144,48,48,48,48,48,48,48,34,48,48,48,48,48,48,48,48,48,48,34,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,142,147,469,487,398,489,489,
489,489,400,487,536,48,188,48,48,48,48,48,48,48,48,48,48,48,144,48,48,48,48,48,48,48,34,48,48,48,48,48,48,48,48,48,48,34,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,142,147,469,487,398,489,489,
489,489,400,487,536,48,188,48,48,48,48,48,48,48,171,190,190,190,167,48,48,48,48,48,48,48,34,48,48,48,48,48,48,48,48,48,48,34,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,142,147,469,487,398,489,489,
489,489,400,487,536,48,188,48,48,48,48,48,48,48,188,48,48,48,48,48,48,48,48,48,48,48,34,48,48,48,48,48,48,48,48,48,48,34,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,142,147,469,487,398,489,489,
489,489,400,487,536,48,194,190,190,190,190,190,190,190,195,48,48,48,48,48,48,48,48,48,48,48,77,57,57,57,57,33,48,48,48,48,48,34,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,142,147,469,487,398,489,489,
489,489,400,487,536,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,77,57,57,57,57,57,79,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,142,147,469,487,398,489,489,
489,489,400,487,536,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,34,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,142,147,469,487,398,489,489,
489,489,400,487,536,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,34,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,142,147,469,487,398,489,489,
489,489,400,487,536,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,34,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,142,147,469,487,398,489,489,
489,489,400,487,536,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,31,31,31,31,48,48,48,34,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,142,147,469,487,398,489,489,
489,489,400,487,536,48,48,48,48,48,48,48,48,48,48,48,31,57,57,57,57,57,33,48,48,48,48,31,48,48,31,57,57,57,79,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,142,147,469,487,398,489,489,
489,489,400,487,536,48,48,48,48,48,48,48,48,48,48,48,34,48,48,48,48,48,34,48,48,48,48,31,48,48,31,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,142,147,469,487,398,489,489,
489,489,400,487,536,48,48,48,48,48,48,48,48,48,48,48,34,48,48,48,48,48,34,48,48,48,48,31,31,31,31,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,142,147,469,487,398,489,489,
489,489,400,487,536,48,48,48,48,48,48,48,48,48,48,48,34,48,48,48,48,48,34,48,48,48,48,34,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,142,147,469,487,398,489,489,
489,489,400,487,536,48,48,48,48,48,48,48,48,48,48,48,77,57,57,57,57,57,79,48,48,48,48,34,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,142,147,469,487,398,489,489,
489,489,400,487,536,48,48,48,48,48,48,48,48,48,48,48,48,48,34,48,48,48,48,48,48,48,48,34,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,142,147,469,487,398,489,489,
489,489,400,487,536,48,48,48,48,48,48,48,48,48,48,48,48,48,34,48,48,48,48,48,48,48,48,34,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,142,147,469,487,398,489,489,
489,489,400,487,536,48,48,48,48,48,48,48,48,48,48,48,48,48,34,48,48,48,48,48,48,48,48,34,48,48,48,48,48,48,48,48,31,57,57,57,57,57,57,57,57,57,57,57,57,57,57,57,33,142,147,469,487,398,489,489,
489,489,400,487,536,48,48,48,48,48,48,48,48,48,48,48,48,48,77,57,57,57,57,57,57,57,57,78,57,57,57,57,57,57,57,57,34,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,34,142,147,469,487,398,489,489,
489,371,423,487,536,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,34,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,34,142,147,469,487,398,489,489,
489,400,487,513,555,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,34,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,34,142,147,469,487,398,489,489,
489,400,487,559,509,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,34,48,48,48,48,48,31,57,57,57,33,48,48,48,48,48,34,142,147,469,487,398,489,489,
489,369,377,487,559,579,578,560,560,560,560,560,560,560,579,121,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,34,48,48,48,48,48,34,48,48,48,34,48,48,48,48,48,34,142,147,469,487,398,489,489,
489,489,400,487,487,535,533,487,487,487,487,487,487,487,535,144,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,77,57,57,57,57,57,79,48,48,48,34,48,48,48,48,48,34,142,147,469,487,398,489,489,
489,489,400,487,487,535,533,487,487,487,487,487,487,487,535,144,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,77,57,57,57,57,57,79,142,147,469,487,398,489,489,
489,489,400,487,487,535,533,487,487,487,487,487,487,487,535,168,121,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,142,147,469,487,398,489,489,
489,489,400,487,487,535,533,487,487,487,487,487,487,487,490,512,168,120,120,120,121,48,119,120,120,120,120,120,120,120,120,120,120,120,120,120,120,120,120,120,120,120,120,120,120,120,120,120,120,120,120,120,120,239,147,469,487,398,489,489,
489,489,400,487,444,558,556,445,446,487,487,487,487,487,487,490,511,511,511,512,237,120,239,169,169,169,169,169,169,169,169,169,169,169,169,169,169,169,169,169,169,169,169,169,169,169,169,169,169,169,169,169,169,169,170,469,487,398,489,489,
489,489,400,487,490,511,511,627,492,487,487,487,487,487,487,487,487,487,487,490,511,511,511,511,511,511,511,511,511,511,511,511,511,511,511,511,511,511,511,511,511,511,511,511,511,511,511,511,511,511,511,511,511,511,511,492,487,398,489,489,
489,489,400,487,487,487,487,487,487,487,487,487,487,487,487,487,487,487,487,487,487,487,487,487,487,487,487,487,487,487,487,487,487,487,487,487,487,487,487,487,487,487,487,487,487,487,487,487,487,487,487,487,487,487,487,487,487,398,489,489,
489,489,369,376,376,376,376,376,376,376,376,376,376,376,376,376,376,376,376,376,376,376,376,376,376,376,376,376,376,376,376,376,376,376,376,376,376,376,376,376,376,376,376,376,376,376,376,376,376,376,376,376,376,376,376,376,376,370,489,489,
489,489,489,489,489,489,489,489,489,489,489,489,489,489,489,489,489,489,489,489,489,489,489,489,489,489,489,489,489,489,489,489,489,489,489,489,489,489,489,489,489,489,489,489,489,489,489,489,489,489,489,489,489,489,489,489,489,489,489,489,
489,489,489,489,489,489,489,489,489,489,489,489,489,489,489,489,489,489,489,489,489,489,489,489,489,489,489,489,489,489,489,489,489,489,489,489,489,489,489,489,489,489,489,489,489,489,489,489,489,489,489,489,489,489,489,489,489,489,489,489]

newmap = decipher(map1, 60, 40)
