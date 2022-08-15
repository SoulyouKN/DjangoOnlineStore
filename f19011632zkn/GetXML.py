#coding:utf-8


from xml.dom import minidom

class GetXML:
    def getxmldata(xmlfile):
    #从XML中读取数据

        dom =minidom.parse (xmlfile)
        root =dom.documentElement
        TestTds = root.getElementsByTagName('TestId')
        Titles = root.getElementsByTagName('Title')
        Methods = root.getElementsByTagName('Method')
        Deses = root.getElementsByTagName('Desc')
        Urls = root.getElementsByTagName('Url')
        InptArgs = root.getElementsByTagName('InptArg')
        Results = root.getElementsByTagName('Result')
        CheckWords = root.getElementsByTagName('CheckWord')
        i=0
        mylists=[]
        for TestId in TestIds:
            mydicts={}
            #获取每个数据,形成字典
            mydicts ["TestId"] = (TestIds[i].firstchild.data).strip()
            mydicts["Title"] =(Titles[i].firstchild.data).strip()
            mydicts ["Method"]=(Methods[i].firstChild.data).strip()
            mydictst["Desc"]=(Descs[i].firstChild.data).strip()
            mydicts ["Url"] =(Uris[i].firstChild.data).strip()
            if((InptArgs[i].firstChild)is None):
                mydicts [ "InptArg"]=""
            else:
                mydicts["InptArg"] =(InptArgs[i].firstChild.data).strip()
            mydicts ["Result"] =(Results[i].firstChild.data).strip()
            mydicts["CheckWord"] = (CheckWords[i].firstChild.data).strip()
            mylists.append(mydicts)
            i = i + 1
        return mylists