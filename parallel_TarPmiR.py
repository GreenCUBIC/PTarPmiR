import threading
import sys
import getopt
import subprocess
from subprocess import call


TarPMir = "TarPmiR.py"
class FastaOperations:
    def __init__(self, file_path):
        fasta_file = open(file_path, 'r')
        self.lines = fasta_file.readlines()
        fasta_file.close()
        self.__set_sequence_dict__()

    def __set_sequence_dict__(self):
        self.sequence_dict = {}
        sequence = ''
        name = ''
        for line in self.lines:
            if '>' in line:
                if sequence != '':
                    self.sequence_dict[name] = sequence
                name = line[1:]
                if name[-1] == "\n":
                    name = name[:-1]
                sequence = ''
            else:
                sequence = sequence + line[:-1]
        if sequence != '':
            self.sequence_dict[name] = sequence

    def get_sequence_dict(self):
        return self.sequence_dict.copy()

def fix_csv(lines,miRNA_fa,mRNA_fa):
    out_lines = []
    for line in lines:
        data = line.split(",")
        if len(data)> 10:
            match = [item[13:].upper() for item in data[7:10]]
            match[1] = match[1].replace(" ",".") + '...'
            out_lines.append(",".join(data[:2]) + "," + ",".join(match)+ "," + ",".join(data[2:6]) + "," + miRNA_fa[data[0]][int(data[2][1:])+1:int(data[3][:-1])+1] + "," + mRNA_fa[data[1]][int(data[4][1:])+1:int(data[5][:-1])+1] + "," + data[6] + "\n")
    out_lines.sort(key= lambda x: float(x.split(",")[-1]), reverse=True)
    return out_lines

def fix_bp(file,f_out):
    lines = open(file).readlines()
    for line1 in lines:
        data1 = line1.split("\t")
        if len(data1) > 20:
            count = 0
            for item in data1:
                if "," in item:
                    item = '"' + item + '"'
                if item[-1] == "\n":
                    f_out.write(f'{item}')
                    count = 0
                else:
                    if count <=19:
                        f_out.write(f'{item},')
                        count += 1
                    else:
                        f_out.write(f'{item[0]}\n{item[1:]},')
                        count = 1
        else:
            data = line1.split("\t")
            for part in data:
                if "," in part:
                    part = '"' + part + '"'
            f_out.write(",".join(data))
            if line1[-1] != "\n":
                f_out.write("\n")


def remove_newlines(inPath, outPath):
    b = ''
    with open(inPath, 'r') as inFile:
        with open(outPath, 'w') as outFile:
            for line in inFile:
                if line[0] == '>':
                    if b != '':
                        outFile.write(b.strip() + '\n')
                    outFile.write(line)
                    b = ''
                else:
                    b += line.strip()
            if b != '\n':
                outFile.write(b.strip())


def split_fasta(inPath, numOut):
    # Set lineCount to the number of lines in the input file
    remove_newlines(inPath, inPath+'.tmp_fixed')

    with open(inPath+'.tmp_fixed', 'r') as inFile:
        lineCount = 0
        for line in inFile:
            lineCount += 1
    inFile.close()
    with open(inPath+'.tmp_fixed', 'r') as inFile:
        for i in range(numOut-1):
            # Build path of outgoing file
            outPath = ""
            for text in inPath.split('.')[:-1]:
                outPath += text
                outPath += '.'
            outPath += str(i)
            outPath += '.'
            outPath += inPath.split('.')[-1]
            with open(outPath, 'w') as outFile:
                title = 'X'
                seq = 'X'
                for lineNum in range(int(lineCount/numOut/2)):
                    while title[0] != '>':
                        title = inFile.readline()
                    while seq[0] not in 'AGTCUNagtcun':
                        seq = inFile.readline()
                    outFile.write(title)
                    outFile.write(seq)
                    title = 'X'
                    seq = 'X'
        # Build path of final outgoing file
        outPath = ""
        for text in inPath.split('.')[:-1]:
            outPath += text
            outPath += '.'
        outPath += str(numOut-1)
        outPath += '.'
        outPath += inPath.split('.')[-1]
        # Write end of incoming file to final outgoing file
        with open(outPath, 'w') as outFile:
            for line in inFile:
                outFile.write(line)
    inFile.close()
    call('rm '+inPath+'.tmp_fixed', shell=True)


def tarpmir(miRNA_path,mRNA_path,model_path,conf):
    pp = subprocess.Popen(f'python3.7 {TarPMir} -a {miRNA_path} -b {mRNA_path} -m {model_path} -p {conf}',shell = True)
    pp.communicate()

opts, extraparams = getopt.getopt(sys.argv[1:], 'a:b:c:p:n:')
for o,p in opts:
    if o == '-a':
        miRNAPath = p
    if o == '-b':
        mRNAPath = p
    if o == '-c':
        modelPath = p
    if o == '-p':
        conf = p
    if o == '-n':
        numThreads = int(p)


for i in range(numThreads):
    call('cp '+miRNAPath+' tmp/'+".".join(miRNAPath.split("/")[-1].split(".")[:-1]) + f'.{i}.'+miRNAPath.split("/")[-1].split(".")[-1], shell=True)
call('cp '+mRNAPath+' tmp/'+mRNAPath.split("/")[-1], shell=True)

split_fasta('tmp/'+mRNAPath.split("/")[-1], numThreads)

threads = []

for i in range(numThreads):
    miRNA_path = 'tmp/'+".".join(miRNAPath.split("/")[-1].split(".")[:-1]) + f'.{i}.'+miRNAPath.split("/")[-1].split(".")[-1]
    mRNA_path = 'tmp/'+".".join(mRNAPath.split("/")[-1].split(".")[:-1]) + f'.{i}.' + mRNAPath.split("/")[-1].split(".")[-1]
    thread = threading.Thread(target=tarpmir, args=(miRNA_path,mRNA_path,modelPath,conf))
    thread.start()
    threads.append(thread)

for thread in threads:
    thread.join()

for i in range(numThreads):
    miRNA_path = ".".join(miRNAPath.split("/")[-1].split(".")[:-1]) + f'.{i}.'+miRNAPath.split("/")[-1].split(".")[-1]
    mRNA_path = ".".join(mRNAPath.split("/")[-1].split(".")[:-1]) + f'.{i}.' + mRNAPath.split("/")[-1].split(".")[-1]
    fix_bp(f"tmp/{miRNA_path}_{mRNA_path}.bp",open(f"tmp/{miRNA_path}_{mRNA_path}.csv", "w+"))
    
f_out = open(f'{"/".join(miRNAPath.split("/")[:-1])}/{miRNAPath.split("/")[-1]}_{mRNAPath.split("/")[-1]}.csv',"w+")
f_out.write("miRNA,mRNA,miranda1,miranda2,miranda3,miRNA seed index,mRNA seed index,miRNA seed sequence,mRNA seed sequence,Prediction Confidence\n")
for i in range(numThreads):
    miRNA_path = ".".join(miRNAPath.split("/")[-1].split(".")[:-1]) + f'.{i}.'+miRNAPath.split("/")[-1].split(".")[-1]
    mRNA_path = ".".join(mRNAPath.split("/")[-1].split(".")[:-1]) + f'.{i}.' + mRNAPath.split("/")[-1].split(".")[-1]
    f_out.writelines(fix_csv(open(f'tmp/{miRNA_path}_{mRNA_path}.csv').readlines(),FastaOperations(f'tmp/{miRNA_path}').get_sequence_dict(),FastaOperations(f'tmp/{mRNA_path}').get_sequence_dict()))

f_out.close()
mRNA_path = 'tmp/'+ mRNAPath.split("/")[-1].split("_")[0] + "*"
subprocess.Popen(f"rm {mRNA_path}", shell=True)
