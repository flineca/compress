import time
import csv
import os
import lzo
import pyhuffman
# Other python lib for huffman:
# import huffmanfile // huffmanfile.compress() # 压缩率不理想
# import huffpress // from huffpress.press.compress import * // compress_bytes() # 压缩率也不理想，耗时也非常长，可能需要配置


TYPE = r'sound' # text, image, sound
ALGORITHM = r'comb' # lzo, huffman, or comb(combination)


csvlist = []
filenames=os.listdir(TYPE)
for filename in filenames:
    input_path = TYPE+'/'+filename
    output_path = TYPE+'/'+ALGORITHM+'_'+filename
    
    # Extracte bytes from files
    with open(TYPE+'/'+filename,'rb+') as f: # open in form of bits
        data_in = f.read()

    start = time.time()
    
    if ALGORITHM == 'comb':
        data_out = pyhuffman.encode(lzo.compress(data_in,2))
    else:
        if ALGORITHM == 'lzo':
            data_out = lzo.compress(data_in,2)
        else:
            data_out = pyhuffman.encode(data_in)

    end = time.time()

    # Save bytes into files
    # with open(output_path,'wb') as f:
    #     f.write(data_out)

    # Calculate
    original_size = len(data_in) # os.path.getsize(input_path)
    compressed_size = len(data_out) # os.path.getsize(output_path)
    ratio = compressed_size/original_size
    time_cost = end - start
    csvlist.append([filename, TYPE, original_size, ALGORITHM, time_cost, compressed_size, ratio])


# Write data into csv
with open(ALGORITHM+"_"+TYPE+"_"+"results.csv","w") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["filename","type","original_size(byte)","algorithm","time_cost(s)","compressed_size(byte)","ratio"])
    writer.writerows(csvlist)