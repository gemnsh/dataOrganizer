from tqdm import tqdm
import pdfplumber
import os
folder_path='./data/'
with open('./result/result.txt','w',encoding='utf-8') as f:
    for filename in os.listdir(folder_path):
        data=[]
        file_path = os.path.join(folder_path, filename)
        dict_ls=dict()
        if filename.lower().endswith(('pdf')):
            obj=[]
            with open('./data/search.txt') as file:
                ls=file.readlines()
            for l in ls:
                obj.append(l.strip())
                dict_ls[l.strip()]=[]
            result=[]
            with pdfplumber.open(folder_path+filename) as pdf:
                text = ""
                i=1
                for page in tqdm(pdf.pages):
                    try :
                        tmp=page.extract_text()
                    except:
                        continue
                    for ob in obj:
                        if ob in tmp:
                            result.append([folder_path+filename,i,ob])
                            dict_ls[ob].append(i)
                    i+=1
                print(filename,file=f)
                print('-----',file=f)
                for k,v in dict_ls.items():
                    if len(v)>0:
                        print(k,v,file=f)
                print('-----\n',file=f)
f.close()